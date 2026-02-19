---
name: aegis-debug
description: Debug the Aegis agent pipeline — sentinels, investigator, orchestrator, architect, executor, scanner, and connectors. Use when user says "debug the scanner", "why isn't the investigator working", "sentinel not detecting changes", or any Aegis pipeline issue.
---

# Aegis Debug Skill
**Usage:** /aegis-debug [description of the pipeline issue]

**Trigger this skill when:**
- Scanner not running or misbehaving
- Sentinel not detecting anomalies
- Investigator discovery failing or returning wrong results
- Orchestrator not routing anomalies to incidents
- Architect analysis failing or producing bad recommendations
- Executor not applying remediations
- Any issue in the Aegis agent pipeline

**Skip for:** General Python bugs (use bug-fix), test failures without pipeline context (use aegis-test), new features (use code-implementation)

---

## Aegis Agent Pipeline Reference

```
Investigator (discovery)
    → Sentinels (anomaly detection: SchemaSentinel + FreshnessSentinel)
        → Orchestrator (anomaly → incident routing, deduplication)
            → Architect (LLM root cause analysis + blast radius via lineage)
                → Executor (remediation actions)
```

**Scanner loop** drives sentinels on cadences:
- Scan: every 5 min (`AEGIS_SCAN_INTERVAL`)
- Lineage refresh: every 1 hr (`AEGIS_LINEAGE_REFRESH`)
- Rediscovery: every 24 hr (`AEGIS_REDISCOVERY_INTERVAL`)

### Key Files

| Component | File | Notes |
|-----------|------|-------|
| Investigator | `aegis/backend/aegis/agents/investigator.py` | LangChain AgentExecutor, deterministic fallback |
| Investigator tools | `aegis/backend/aegis/agents/investigator_tools.py` | 5 tools via `make_tools()` closure factory |
| Investigator prompts | `aegis/backend/aegis/agents/investigator_prompts.py` | System + human templates |
| Sentinels | `aegis/backend/aegis/agents/sentinel.py` | SchemaSentinel + FreshnessSentinel |
| Orchestrator | `aegis/backend/aegis/agents/orchestrator.py` | Anomaly → incident routing |
| Architect | `aegis/backend/aegis/agents/architect.py` | LLM-powered root cause analysis |
| Executor | `aegis/backend/aegis/agents/executor.py` | Remediation execution |
| Scanner | `aegis/backend/aegis/services/scanner.py` | Background scan loop |
| Connectors | `aegis/backend/aegis/core/connectors.py` | WarehouseConnector |
| Models | `aegis/backend/aegis/core/models.py` | All ORM + Pydantic schemas |
| Config | `aegis/backend/aegis/config.py` | Pydantic Settings, `AEGIS_` prefix |

---

## Phase 1: Identify the Failing Component

### Step 1.1: Map Symptom to Component

| Symptom | Likely Component | Start Here |
|---------|-----------------|------------|
| Tables not discovered | Investigator | `investigator.py`, connector methods |
| Schema changes not detected | SchemaSentinel | `sentinel.py`, `scanner.py` |
| Stale tables not flagged | FreshnessSentinel | `sentinel.py`, `scanner.py` |
| Anomalies not creating incidents | Orchestrator | `orchestrator.py` |
| No root cause analysis | Architect | `architect.py`, LLM service |
| Remediation not applied | Executor | `executor.py` |
| Nothing running at all | Scanner loop | `scanner.py`, `main.py` lifespan |
| Connection failures | Connector | `connectors.py`, connection params |

### Step 1.2: Read the Component Code

Read the identified file(s) and trace the data flow from input to output.

---

## Phase 2: Check Common Aegis Gotchas

### Async/Sync Bridge Issues
- **API is async** (FastAPI + AsyncSession)
- **Agents are sync** (SQLAlchemy Session via SyncSessionLocal)
- Bridge: `asyncio.to_thread` + `SyncSessionLocal`
- **Gotcha:** Don't pass AsyncSession to agent code — extract what you need first

### Mock Patterns in Tests
- **`side_effect` overrides `return_value`** — if a mock has `side_effect` set, `return_value` is ignored. Clear with `mock.side_effect = None` first.
- **Lazy imports need source patching** — `notifier` is imported inside scanner functions. Patch at `aegis.services.notifier.notifier`, NOT `aegis.services.scanner.notifier`.
- **`sample_connection` vs `sample_table`** — `sample_connection` only creates a ConnectionModel. For a monitored table, also request `sample_table` fixture.

### LangChain Tool Binding
- `make_tools()` is a closure factory — connector, db, lineage_graph are bound per invocation
- If tools fail, check that the closure arguments are valid (not None, not stale sessions)

### Deterministic Fallback
- Investigator uses `_classify_by_rules()` when LangChain agent fails
- If classification is wrong but discovery runs, check the rule-based fallback logic

---

## Phase 3: Deep Investigation

### Step 3.1: Deploy `pipeline-expert` Agent

Use the Task tool to spawn the `pipeline-expert` sub-agent with:
- The identified component and symptom
- Relevant code snippets (20-50 lines max)
- Any error messages or unexpected outputs

### Step 3.2: Review Findings

Evaluate the sub-agent's report:
- Is the root cause specific (file:line)?
- Does evidence support the conclusion?
- Does the fix address root cause, not symptoms?

---

## Phase 4: Present Findings & Fix

Follow the same approval gate pattern as the `investigator` skill:
1. Present findings with root cause, evidence, and proposed fix
2. Wait for user approval
3. Hand off to `/code-implementation` or `/bug-fix` for the actual fix

---

## Quality Guidelines

**ALWAYS:**
- Check the gotchas list before diving deep
- Use the file reference table to find the right code
- Spawn `pipeline-expert` for complex investigations
- Trace data flow through the full pipeline, not just one component

**NEVER:**
- Assume async code works the same as sync
- Forget to check mock patterns when debugging tests
- Skip the connector/session validity check
- Modify pipeline code without understanding upstream/downstream effects
