# Incident Report Generator — Design

**Goal:** Generate a structured, human-readable incident report whenever an incident is created, stored on the incident model and served via a dedicated API endpoint.

**Approach:** Dedicated `ReportGenerator` class that transforms existing incident/anomaly/diagnosis/remediation data into a structured `IncidentReport` Pydantic model. No LLM calls — pure deterministic formatting.

---

## Data Model

New Pydantic schemas in `core/models.py`:

```python
class AnomalyDetail(BaseModel):
    type: str                         # "schema_drift" | "freshness_breach"
    table: str                        # fully qualified name
    detected_at: datetime
    changes: list[dict[str, Any]]     # parsed anomaly detail

class RootCauseDetail(BaseModel):
    explanation: str
    source_table: str
    confidence: float

class BlastRadiusDetail(BaseModel):
    total_affected: int
    affected_tables: list[str]

class RecommendedAction(BaseModel):
    action: str
    description: str
    priority: int
    status: str                       # "pending_approval" | "manual"

class TimelineEvent(BaseModel):
    timestamp: datetime
    event: str

class IncidentReport(BaseModel):
    incident_id: int
    title: str
    severity: str
    status: str
    generated_at: datetime
    summary: str
    anomaly_details: AnomalyDetail
    root_cause: RootCauseDetail
    blast_radius: BlastRadiusDetail
    recommended_actions: list[RecommendedAction]
    timeline: list[TimelineEvent]
```

New column on `IncidentModel`:

```python
report: Mapped[str | None] = mapped_column(Text, nullable=True)
```

## Report Generator

New file: `agents/report_generator.py`

Class `ReportGenerator` with a single method:

```python
def generate(
    self,
    incident: IncidentModel,
    anomaly: AnomalyModel,
    table: MonitoredTableModel,
    diagnosis: Diagnosis | None,
    remediation: Remediation | None,
) -> IncidentReport
```

Responsibilities:
- Build title from anomaly type + table name
- Write 2-3 sentence executive summary
- Parse anomaly.detail JSON into AnomalyDetail
- Extract root cause from diagnosis (or fallback text)
- Format blast radius from diagnosis
- Map remediation actions to RecommendedAction list
- Assemble timeline from timestamps (anomaly.detected_at, incident.created_at, etc.)

## Integration

### Orchestrator (step 6.5 — after status update, before notification)

```python
# 6. Generate incident report
try:
    from aegis.agents.report_generator import ReportGenerator
    generator = ReportGenerator()
    report = generator.generate(incident, anomaly, table, diag_obj, remediation_obj)
    incident.report = report.model_dump_json()
except Exception:
    logger.exception("Report generation failed for incident %d", incident.id)
```

### API — New endpoint

`GET /incidents/{id}/report` → returns stored `IncidentReport` JSON.

Returns 404 if incident not found, 204 if report hasn't been generated yet.

### Alembic migration

Add `report` TEXT column to `incidents` table.

## Testing

- `test_report_generator.py`: Unit tests for ReportGenerator with mocked incident/anomaly data
- `test_orchestrator.py`: Verify report is generated and stored during handle_anomaly
- `test_api.py` or `test_incidents_report.py`: Verify GET endpoint returns report
