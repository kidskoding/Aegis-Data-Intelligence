---
name: aegis-test
description: Run and manage Aegis backend tests. Knows the test infrastructure, fixtures, and conventions. Use when user says "run tests", "check coverage", "validate before commit", or any test-related request for the Aegis project.
---

# Aegis Test Skill
**Usage:** /aegis-test [optional: specific test file or pattern]

**Trigger this skill when:**
- User says "run tests", "run the test suite"
- User says "check coverage", "validate before commit"
- Test failures need interpretation
- User is adding new tests and needs fixture guidance
- Before committing Aegis backend changes

**Skip for:** Pipeline debugging (use aegis-debug), general bug investigation (use investigator), non-Aegis tests

---

## Quick Reference

### Run All Tests

```bash
cd aegis/backend && python -m pytest tests/ -v --tb=short
```

**Baseline:** 68 tests passing (as of 2026-02-17)

### Run Specific Test File

```bash
cd aegis/backend && python -m pytest tests/test_<name>.py -v --tb=short
```

### Run Specific Test

```bash
cd aegis/backend && python -m pytest tests/test_<name>.py::test_function -v --tb=short
```

---

## Test Infrastructure

### Test Files (15 files)

Located at `aegis/backend/tests/`. Key files:

| File | What It Tests | Special Setup |
|------|--------------|---------------|
| `conftest.py` | Shared fixtures | In-memory SQLite |
| `test_api.py` | REST API endpoints | Temp-file SQLite, own fixtures |
| `test_discovery_api.py` | Discovery endpoints | Temp-file SQLite, own fixtures |
| `test_sentinel.py` | SchemaSentinel + FreshnessSentinel | conftest fixtures |
| `test_orchestrator.py` | Anomaly -> incident routing | conftest fixtures |
| `test_architect.py` | LLM root cause analysis | Mocked LLM |
| `test_executor.py` | Remediation execution | conftest fixtures |
| `test_investigator.py` | Investigator agent | Mocked LLM + tools |
| `test_scanner.py` | Scanner loop + cadences | Mocked services |
| `test_connectors.py` | WarehouseConnector | Mocked DB connections |
| `test_lineage.py` | SQL parsing + lineage graph | conftest fixtures |
| `test_models.py` | ORM + Pydantic schemas | conftest fixtures |

### Fixture Hierarchy

```
db (in-memory SQLite session)
├── sample_connection (ConnectionModel)
│   └── sample_table (MonitoredTableModel, requires sample_connection)
│       ├── sample_snapshot (SnapshotModel)
│       ├── sample_anomaly (AnomalyModel)
│       │   └── sample_incident (IncidentModel)
│       └── sample_lineage_edges (LineageEdgeModel list)
└── api_client (TestClient for FastAPI)
```

**Gotcha:** `sample_connection` only creates a ConnectionModel. To have a monitored table in the DB, you must also request `sample_table`.

### Two Test Environments

| Environment | Used By | Engine | Why |
|-------------|---------|--------|-----|
| In-memory SQLite | Most tests (via conftest `db`) | `create_engine("sqlite://")` | Fast, isolated |
| Temp-file SQLite | `test_api.py`, `test_discovery_api.py` | `create_engine(f"sqlite:///{tmp.name}")` | Async + sync engines must share state |

---

## Interpreting Failures

### Common Failure Patterns

| Error Pattern | Likely Cause | Fix |
|--------------|-------------|-----|
| `fixture 'sample_table' not found` | Missing fixture request | Add `sample_table` to test function params |
| `side_effect` ignoring `return_value` | Mock has `side_effect` set | Clear with `mock.side_effect = None` first |
| `notifier` mock not working | Wrong patch location | Patch at `aegis.services.notifier.notifier` |
| `async` test hanging | Async/sync bridge issue | Check `asyncio.to_thread` usage |
| Import errors | Missing dependency | Check `requirements.txt` |

### When Tests Fail

1. **Read the error** -- what assertion failed, what was expected vs actual
2. **Check fixtures** -- is the test requesting all needed fixtures?
3. **Check mocks** -- are side_effect/return_value set correctly?
4. **Check imports** -- is the patch location correct?
5. **Run in isolation** -- does the test pass alone? (`-k test_name`)

---

## Adding New Tests

### Template

```python
def test_<component>_<behavior>(db, sample_connection, sample_table):
    """Test that <component> <expected behavior>."""
    # Arrange
    <setup>

    # Act
    result = <function_under_test>(<args>)

    # Assert
    assert result == expected
```

### Conventions
- Test files: `tests/test_<component>.py`
- Test functions: `test_<component>_<behavior>`
- Use conftest fixtures, don't create new DB sessions
- Mock external services (LLM, connectors) -- never call real APIs in tests
- Keep tests focused: one assertion per test when possible

---

## Quality Guidelines

**ALWAYS:**
- Run the full suite before committing (`python -m pytest tests/ -v --tb=short`)
- Check test count against baseline (68)
- Use existing fixtures from conftest
- Mock external dependencies

**NEVER:**
- Skip running tests before commit
- Create new DB engines in individual tests (use fixtures)
- Call real external APIs in tests
- Ignore test count changes (added tests should increase count, not decrease)
