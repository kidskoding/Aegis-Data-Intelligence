"""Tests for incident report Pydantic schemas."""

from datetime import datetime, timezone

from aegis.core.models import (
    AnomalyDetail,
    BlastRadiusDetail,
    IncidentReport,
    RecommendedAction,
    RootCauseDetail,
    TimelineEvent,
)


def test_incident_report_creation():
    report = IncidentReport(
        incident_id=1,
        title="Schema Drift on public.orders",
        severity="critical",
        status="pending_review",
        generated_at=datetime.now(timezone.utc),
        summary="Column 'price' was deleted from public.orders.",
        anomaly_details=AnomalyDetail(
            type="schema_drift",
            table="public.orders",
            detected_at=datetime.now(timezone.utc),
            changes=[{"change": "column_deleted", "column": "price"}],
        ),
        root_cause=RootCauseDetail(
            explanation="Column deleted upstream",
            source_table="staging.orders",
            confidence=0.85,
        ),
        blast_radius=BlastRadiusDetail(
            total_affected=2,
            affected_tables=["analytics.daily_revenue", "analytics.customer_ltv"],
        ),
        recommended_actions=[
            RecommendedAction(
                action="revert_schema",
                description="Revert column deletion",
                priority=1,
                status="pending_approval",
            ),
        ],
        timeline=[
            TimelineEvent(
                timestamp=datetime.now(timezone.utc),
                event="Anomaly detected: schema_drift on public.orders",
            ),
        ],
    )
    assert report.incident_id == 1
    assert report.severity == "critical"
    assert report.blast_radius.total_affected == 2
    assert len(report.recommended_actions) == 1
    assert len(report.timeline) == 1


def test_incident_report_empty_blast_radius():
    report = IncidentReport(
        incident_id=2,
        title="Freshness Breach on public.users",
        severity="medium",
        status="pending_review",
        generated_at=datetime.now(timezone.utc),
        summary="Table public.users is 30 minutes overdue.",
        anomaly_details=AnomalyDetail(
            type="freshness_breach",
            table="public.users",
            detected_at=datetime.now(timezone.utc),
            changes=[{"sla_minutes": 60, "minutes_overdue": 30}],
        ),
        root_cause=RootCauseDetail(
            explanation="Manual investigation required.",
            source_table="public.users",
            confidence=0.0,
        ),
        blast_radius=BlastRadiusDetail(
            total_affected=0,
            affected_tables=[],
        ),
        recommended_actions=[],
        timeline=[],
    )
    assert report.blast_radius.total_affected == 0
    assert report.recommended_actions == []
