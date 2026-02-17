"""Discovery API endpoints — trigger investigation and confirm table enrollment."""

from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aegis.agents.investigator import Investigator
from aegis.api.deps import get_db, verify_api_key
from aegis.core.connectors import WarehouseConnector
from aegis.core.database import SyncSessionLocal
from aegis.core.models import (
    ConnectionModel,
    DiscoveryConfirm,
    MonitoredTableModel,
)

router = APIRouter(dependencies=[Depends(verify_api_key)])


def _run_discover_sync(connection_uri: str, dialect: str, conn_id: int, conn_name: str):
    """Run discovery in a sync context (LangChain and connector are blocking)."""
    connector = WarehouseConnector(connection_uri, dialect)
    try:
        with SyncSessionLocal() as db:
            from aegis.core.models import ConnectionModel as CM

            conn_model = db.get(CM, conn_id)
            investigator = Investigator()
            report = investigator.discover(connector, db, conn_model)
            return report.model_dump(mode="json")
    finally:
        connector.dispose()


@router.post("/{conn_id}/discover")
async def discover_tables(conn_id: int, db: AsyncSession = Depends(get_db)):
    """Trigger warehouse discovery and return classification proposals."""
    conn = await db.get(ConnectionModel, conn_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    return await asyncio.to_thread(
        _run_discover_sync,
        conn.connection_uri,
        conn.dialect,
        conn.id,
        conn.name,
    )


@router.post("/{conn_id}/discover/confirm", status_code=201)
async def confirm_discovery(
    conn_id: int,
    body: DiscoveryConfirm,
    db: AsyncSession = Depends(get_db),
):
    """Enroll selected tables from a discovery report."""
    conn = await db.get(ConnectionModel, conn_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    enrolled = []
    for selection in body.table_selections:
        # Check for duplicates
        stmt = select(MonitoredTableModel).where(
            MonitoredTableModel.connection_id == conn_id,
            MonitoredTableModel.schema_name == selection.schema_name,
            MonitoredTableModel.table_name == selection.table_name,
        )
        existing = (await db.execute(stmt)).scalar_one_or_none()
        if existing:
            continue

        table = MonitoredTableModel(
            connection_id=conn_id,
            schema_name=selection.schema_name,
            table_name=selection.table_name,
            fully_qualified_name=f"{selection.schema_name}.{selection.table_name}",
            check_types=json.dumps(selection.check_types),
            freshness_sla_minutes=selection.freshness_sla_minutes,
        )
        db.add(table)
        enrolled.append({
            "schema_name": selection.schema_name,
            "table_name": selection.table_name,
            "check_types": selection.check_types,
            "freshness_sla_minutes": selection.freshness_sla_minutes,
        })

    await db.commit()
    return {"enrolled": enrolled, "total": len(enrolled)}
