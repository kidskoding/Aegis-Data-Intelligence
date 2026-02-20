# Aegis `.claude/` Skills & Agents Design

**Date:** 2026-02-19
**Status:** Approved

## Goal

Create a self-contained `aegis/.claude/` directory with:
1. **Portable skills** (PR review, issue fixing) — reusable across any project
2. **Project-specific skills** (Aegis debugging, testing) — tailored to the Aegis data intelligence platform
3. **Domain-aware sub-agents** — deep knowledge of the Aegis agent pipeline

## Approach

**Flat per-project** — everything lives inside `aegis/.claude/`. No symlinks, submodules, or external dependencies. Claude Code discovers skills automatically when working in the `aegis/` directory.

## Directory Structure

```
aegis/.claude/
├── skills/
│   ├── pr-review/
│   │   └── SKILL.md              # Portable: review GitHub PRs
│   ├── issue-fix/
│   │   └── SKILL.md              # Portable: triage + fix GitHub issues
│   ├── aegis-debug/
│   │   └── SKILL.md              # Project: debug Aegis agent pipeline
│   └── aegis-test/
│       └── SKILL.md              # Project: run tests, check coverage
├── agents/
│   ├── pipeline-expert.md        # Knows sentinel→orchestrator→architect→executor
│   ├── aegis-tester.md           # Runs pytest, understands fixture infra
│   └── connector-debugger.md     # Debugs warehouse connectors + discovery
└── settings.local.json           # Aegis-specific Claude settings
```

## Portable Skills

### `pr-review`

**Trigger:** "review this PR", "check PR #N", PR URL shared

**Workflow:**
1. Fetch PR diff + metadata via `gh pr view` and `gh pr diff`
2. Analyze changes against project conventions (reads CLAUDE.md)
3. Check for: security issues, test coverage, plan alignment, code quality
4. Produce structured review with severity-classified findings (CRITICAL/HIGH/MEDIUM/LOW)
5. Optionally post review comments via `gh pr review`

**Difference from existing `code-reviewer`:** `code-reviewer` reviews local code against a plan. `pr-review` targets GitHub PRs — fetches remote diffs, understands PR context (description, linked issues), and posts comments to GitHub.

### `issue-fix`

**Trigger:** "fix issue #N", "work on this issue", GitHub issue reference

**Workflow:**
1. Fetch issue details via `gh issue view`
2. Triage: bug report, feature request, or unclear
3. Explore codebase to locate relevant code
4. Create fix plan (files, changes, success criteria)
5. Implement fix (TDD: test first, then code)
6. Run verification, present results

**Difference from existing `bug-fix`:** `bug-fix` assumes the user identified the problem. `issue-fix` starts from a GitHub issue number — reads the issue, triages, handles full lifecycle including branch creation and verification.

## Project-Specific Skills

### `aegis-debug`

**Trigger:** "debug the scanner", "why isn't the investigator working", "sentinel not detecting"

**Workflow:**
1. Identify which agent in the pipeline is failing
2. Understand the agent chain and data flow
3. Check common Aegis issues (async/sync bridge, mock patterns, connector state)
4. Spawn `pipeline-expert` agent for deep investigation
5. Propose targeted fixes using Aegis conventions

### `aegis-test`

**Trigger:** "run tests", "check coverage", "validate before commit"

**Workflow:**
1. Run `cd aegis/backend && python -m pytest tests/ -v --tb=short`
2. Parse results, categorize failures
3. Know fixture dependencies (`sample_table` requires `sample_connection`)
4. For new code, check that tests exist and cover key paths
5. Report test count against baseline (68 passing)

## Sub-Agents

### `pipeline-expert`

**Purpose:** Deep knowledge of the Aegis agent pipeline

**Domain knowledge:**
- Full agent chain: Investigator → Sentinels → Orchestrator → Architect → Executor
- Async/sync bridging pattern (AsyncSession vs SyncSessionLocal)
- LangChain tool binding via `make_tools()` closures
- Deterministic fallback in Investigator
- Scanner cadences (5min/1hr/24hr)
- All ORM models + Pydantic schemas in `core/models.py`

**Used when:** Debugging agent behavior, extending agents, understanding data flow between pipeline stages.

### `aegis-tester`

**Purpose:** Test infrastructure expertise

**Domain knowledge:**
- conftest.py fixtures: `db`, `sample_connection`, `sample_table`, `sample_snapshot`, etc.
- Temp-file SQLite for async test isolation (test_api.py, test_discovery_api.py)
- In-memory SQLite for sync tests (all others)
- Mock patterns: `side_effect` vs `return_value` gotcha
- Lazy import patch locations (`aegis.services.notifier.notifier`)

**Used when:** Running tests, interpreting failures, creating new test fixtures.

### `connector-debugger`

**Purpose:** Warehouse connector + discovery specialist

**Domain knowledge:**
- `WarehouseConnector` class and its methods (schema, freshness, discovery)
- Investigator discovery flow (LangChain AgentExecutor → 5 tools → classification)
- Connection parameter validation
- Discovery API async/sync bridge via `asyncio.to_thread`

**Used when:** Connection failures, discovery not returning results, connector configuration issues.

## Settings

`aegis/.claude/settings.local.json` will be minimal — primarily ensuring the skills and agents directory is recognized. No overly permissive allow rules.
