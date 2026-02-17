"""LangChain tools for the Investigator agent — closure-bound per invocation."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from langchain_core.tools import tool

from aegis.core.connectors import WarehouseConnector

logger = logging.getLogger("aegis.investigator.tools")


def make_tools(
    connector: WarehouseConnector,
    db: Any,
    lineage_graph: Any = None,
) -> list:
    """Create Investigator tools with connector/db bound via closure."""

    @tool
    def list_warehouse_schemas() -> list[str]:
        """List all user-accessible schemas in the warehouse.
        Excludes system schemas (information_schema, pg_catalog, etc.).
        Call this first to discover what schemas exist."""
        try:
            return connector.list_schemas()
        except Exception as exc:
            logger.warning("list_schemas failed: %s", exc)
            return []

    @tool
    def list_schema_tables(schema_name: str) -> list[dict]:
        """List all tables and views in a specific schema.
        Returns: [{name, type (BASE TABLE/VIEW), schema}]
        Call this for each schema to see what tables exist."""
        try:
            return connector.list_tables(schema_name)
        except Exception as exc:
            logger.warning("list_tables failed for %s: %s", schema_name, exc)
            return []

    @tool
    def inspect_table_columns(schema_name: str, table_name: str) -> list[dict]:
        """Get detailed column metadata for a specific table.
        Returns: [{name, type, nullable, ordinal}]
        Call this for tables you want to inspect more deeply."""
        try:
            return connector.fetch_schema(schema_name, table_name)
        except Exception as exc:
            logger.warning("fetch_schema failed for %s.%s: %s", schema_name, table_name, exc)
            return []

    @tool
    def check_table_freshness(schema_name: str, table_name: str) -> dict:
        """Check if a table has timestamp columns and when it was last updated.
        Returns: {has_timestamp: bool, last_update: str|null, timestamp_column: str|null}
        Useful for deciding if freshness monitoring is possible."""
        try:
            last_update = connector.fetch_last_update_time(schema_name, table_name)
            if last_update is not None:
                return {
                    "has_timestamp": True,
                    "last_update": last_update.isoformat() if isinstance(last_update, datetime) else str(last_update),
                    "timestamp_column": "detected",
                }
            return {"has_timestamp": False, "last_update": None, "timestamp_column": None}
        except Exception as exc:
            logger.warning("freshness check failed for %s.%s: %s", schema_name, table_name, exc)
            return {"has_timestamp": False, "last_update": None, "timestamp_column": None}

    @tool
    def get_known_lineage(table_name: str) -> dict:
        """Get known upstream and downstream dependencies for a table from the lineage graph.
        Returns: {upstream: [str], downstream: [str]}
        Only available if lineage has been previously refreshed."""
        if lineage_graph is None:
            return {"upstream": [], "downstream": []}
        try:
            upstream = lineage_graph.get_upstream(table_name, depth=3)
            downstream = lineage_graph.get_downstream(table_name, depth=3)
            return {
                "upstream": [n["table"] for n in upstream] if upstream else [],
                "downstream": [n["table"] for n in downstream] if downstream else [],
            }
        except Exception as exc:
            logger.warning("lineage lookup failed for %s: %s", table_name, exc)
            return {"upstream": [], "downstream": []}

    return [
        list_warehouse_schemas,
        list_schema_tables,
        inspect_table_columns,
        check_table_freshness,
        get_known_lineage,
    ]
