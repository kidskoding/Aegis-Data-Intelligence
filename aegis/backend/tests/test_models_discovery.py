"""Tests for discovery Pydantic schemas."""

from datetime import datetime, timezone

from aegis.core.models import (
    DiscoveryConfirm,
    DiscoveryReport,
    TableDelta,
    TableProposal,
    TableSelectionItem,
)


def test_table_proposal_creation():
    proposal = TableProposal(
        schema_name="public",
        table_name="users",
        fully_qualified_name="public.users",
        role="dimension",
        columns=[{"name": "id", "type": "INTEGER", "nullable": False, "ordinal": 1}],
        recommended_checks=["schema", "freshness"],
        suggested_sla_minutes=360,
        reasoning="Core user table with updated_at",
        skip=False,
    )
    assert proposal.role == "dimension"
    assert proposal.skip is False


def test_table_proposal_skip():
    proposal = TableProposal(
        schema_name="staging",
        table_name="_tmp_dedup",
        fully_qualified_name="staging._tmp_dedup",
        role="system",
        columns=[],
        recommended_checks=[],
        suggested_sla_minutes=None,
        reasoning="Temporary table",
        skip=True,
    )
    assert proposal.skip is True
    assert proposal.recommended_checks == []


def test_discovery_report_creation():
    report = DiscoveryReport(
        connection_id=1,
        connection_name="test-warehouse",
        schemas_found=["public", "staging"],
        total_tables=5,
        proposals=[],
        concerns=["Table X has no timestamps"],
        generated_at=datetime.now(timezone.utc),
    )
    assert report.total_tables == 5
    assert len(report.concerns) == 1


def test_table_delta_new():
    delta = TableDelta(
        action="new",
        schema_name="public",
        table_name="new_table",
        fully_qualified_name="public.new_table",
        proposal=TableProposal(
            schema_name="public",
            table_name="new_table",
            fully_qualified_name="public.new_table",
            role="unknown",
            columns=[],
            recommended_checks=["schema"],
            suggested_sla_minutes=None,
            reasoning="New table detected",
            skip=False,
        ),
    )
    assert delta.action == "new"
    assert delta.proposal is not None


def test_table_delta_dropped():
    delta = TableDelta(
        action="dropped",
        schema_name="public",
        table_name="old_table",
        fully_qualified_name="public.old_table",
        proposal=None,
    )
    assert delta.action == "dropped"
    assert delta.proposal is None


def test_discovery_confirm():
    confirm = DiscoveryConfirm(
        table_selections=[
            TableSelectionItem(
                schema_name="public",
                table_name="users",
                check_types=["schema", "freshness"],
                freshness_sla_minutes=360,
            ),
            TableSelectionItem(
                schema_name="staging",
                table_name="stg_orders",
            ),
        ]
    )
    assert len(confirm.table_selections) == 2
    assert confirm.table_selections[1].check_types == ["schema", "freshness"]
    assert confirm.table_selections[1].freshness_sla_minutes is None
