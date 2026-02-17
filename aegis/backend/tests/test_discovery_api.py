"""Tests for discovery API endpoints."""

import os
import tempfile
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aegis.core.models import DiscoveryReport, TableProposal

# Use a temp file so async and sync engines share the same database
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ.setdefault("AEGIS_DB_PATH", _tmp.name)
os.environ.setdefault("AEGIS_API_KEY", "dev-key")


@pytest.fixture(autouse=True)
def _reset_db():
    """Recreate tables before each test."""
    with patch("aegis.core.database.run_migrations"):
        from aegis.core.database import Base, sync_engine

        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
    yield


@pytest.fixture
def client():
    with patch("aegis.core.database.run_migrations"), \
         patch("aegis.core.database.ensure_db_directory"), \
         patch("aegis.services.scanner.start_scanner", new_callable=AsyncMock, return_value=None):

        from fastapi.testclient import TestClient
        from aegis.main import app

        with TestClient(app) as c:
            yield c


@pytest.fixture
def mock_discovery_report():
    return DiscoveryReport(
        connection_id=1,
        connection_name="test-warehouse",
        schemas_found=["public"],
        total_tables=1,
        proposals=[
            TableProposal(
                schema_name="public",
                table_name="users",
                fully_qualified_name="public.users",
                role="dimension",
                columns=[{"name": "id", "type": "INTEGER", "nullable": False, "ordinal": 1}],
                recommended_checks=["schema", "freshness"],
                suggested_sla_minutes=360,
                reasoning="Core user table",
                skip=False,
            )
        ],
        concerns=[],
        generated_at=datetime.now(timezone.utc),
    )


def test_discover_endpoint(client, mock_discovery_report):
    with patch("aegis.api.discovery.Investigator") as MockInvestigator, \
         patch("aegis.api.discovery.WarehouseConnector") as MockConnector:
        mock_inv = MockInvestigator.return_value
        mock_inv.discover.return_value = mock_discovery_report
        mock_conn = MockConnector.return_value

        # Create connection first
        resp = client.post(
            "/api/v1/connections",
            json={"name": "test-wh", "dialect": "postgresql", "connection_uri": "postgresql://x"},
        )
        conn_id = resp.json()["id"]

        resp = client.post(f"/api/v1/connections/{conn_id}/discover")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_tables"] == 1
        assert data["proposals"][0]["role"] == "dimension"


def test_confirm_endpoint_creates_tables(client):
    # Create connection first
    resp = client.post(
        "/api/v1/connections",
        json={"name": "test-wh2", "dialect": "postgresql", "connection_uri": "postgresql://x"},
    )
    conn_id = resp.json()["id"]

    resp = client.post(
        f"/api/v1/connections/{conn_id}/discover/confirm",
        json={
            "table_selections": [
                {
                    "schema_name": "public",
                    "table_name": "users",
                    "check_types": ["schema", "freshness"],
                    "freshness_sla_minutes": 360,
                }
            ]
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["enrolled"]) == 1
    assert data["enrolled"][0]["table_name"] == "users"


def test_discover_404_for_missing_connection(client):
    resp = client.post("/api/v1/connections/9999/discover")
    assert resp.status_code == 404
