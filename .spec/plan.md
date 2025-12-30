# AgentFlow Architecture Plan

## Overview

This document defines the technical architecture for AgentFlow, derived from the [specification](./specification.md).

**Phase:** Plan  
**Status:** Approved  
**Last Updated:** 2025-12-30

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   │
│  │ /health │ │ /spec   │ │ /plan   │ │ /tasks /impl    │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Phase Manager                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ SPECIFY  │→│  PLAN    │→│  TASKS   │→│  IMPLEMENT   │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
│                    (Gated Transitions)                      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Agent Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ CodeAnalyzer│ │   Builder   │ │    Orchestrator     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Core Layer                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │  Tools   │ │  State   │ │  Tasks   │ │   Phases     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| API Layer | HTTP endpoints, request/response handling |
| Phase Manager | Workflow phase transitions, validation gates |
| Agent Layer | Specialized task execution |
| Core Layer | Shared infrastructure, tools, state |

---

## 2. Technology Stack

### 2.1 Runtime
- **Language:** Python 3.10+
- **Async Framework:** asyncio
- **Web Framework:** FastAPI

### 2.2 Dependencies
| Dependency | Purpose | Version |
|------------|---------|---------|
| FastAPI | REST API framework | >=0.109.0 |
| Pydantic | Data validation & settings | >=2.5.0 |
| uvicorn | ASGI server | >=0.27.0 |
| structlog | Structured logging | >=24.1.0 |
| rich | Terminal output formatting | >=13.7.0 |
| httpx | HTTP client | >=0.26.0 |

### 2.3 Development Tools
| Tool | Purpose |
|------|---------|
| pytest | Testing framework |
| ruff | Linting |
| black | Code formatting |
| mypy | Type checking |

---

## 3. Directory Structure

```
agentflow/
├── .spec/                    # SDD Artifacts
│   ├── specification.md      # What to build
│   ├── plan.md              # How to build (this file)
│   ├── tasks.md             # Work breakdown
│   └── implementation.md    # Implementation log
│
├── src/
│   ├── __init__.py
│   │
│   ├── agents/              # Agent implementations
│   │   ├── __init__.py
│   │   ├── base.py          # BaseAgent, AgentResult, AgentContext
│   │   ├── code_analyzer.py # Code analysis agent
│   │   ├── builder.py       # Build/test agent
│   │   └── orchestrator.py  # Multi-agent coordination
│   │
│   ├── api/                 # REST API
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py    # Health endpoints
│   │       ├── phases.py    # Phase management (NEW)
│   │       ├── analysis.py  # Analysis endpoints
│   │       └── workflows.py # Workflow execution
│   │
│   ├── core/                # Core infrastructure
│   │   ├── __init__.py
│   │   ├── phases.py        # Phase management (NEW)
│   │   ├── state.py         # State persistence
│   │   ├── task_queue.py    # Task management
│   │   └── tools.py         # Tool implementations
│   │
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── config.py        # Configuration
│       └── logging.py       # Logging setup
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── docs/                    # Documentation
│   ├── architecture.md
│   ├── api.md
│   └── sdd-guide.md        # SDD tutorial (NEW)
│
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── demo.py
├── learn.py
└── README.md
```

---

## 4. Data Models

### 4.1 Phase Management

```python
class Phase(str, Enum):
    SPECIFY = "specify"
    PLAN = "plan"
    TASKS = "tasks"
    IMPLEMENT = "implement"

class PhaseStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class PhaseResult(BaseModel):
    phase: Phase
    status: PhaseStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    artifacts: Dict[str, Any]
    validation_errors: List[str]

class ProjectState(BaseModel):
    project_id: str
    current_phase: Phase
    phases: Dict[Phase, PhaseResult]
    specification: Optional[Dict[str, Any]]
    plan: Optional[Dict[str, Any]]
    tasks: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
```

### 4.2 Agent Models (Existing, Enhanced)

```python
class AgentContext:
    task_id: str
    workspace_path: str
    config: Dict[str, Any]
    shared_data: Dict[str, Any]
    current_phase: Phase        # NEW
    project_state: ProjectState  # NEW

class AgentResult:
    agent_name: str
    status: AgentStatus
    data: Dict[str, Any]
    phase: Phase                # NEW
    artifacts_produced: List[str]  # NEW
```

---

## 5. API Design

### 5.1 Phase Endpoints (New)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/project/status` | Get current project phase status |
| POST | `/api/v1/phases/specify` | Start/update specification phase |
| POST | `/api/v1/phases/plan` | Generate plan from specification |
| POST | `/api/v1/phases/tasks` | Break plan into tasks |
| POST | `/api/v1/phases/implement` | Execute implementation |
| GET | `/api/v1/phases/{phase}/status` | Get specific phase status |
| POST | `/api/v1/phases/{phase}/validate` | Validate phase completion |

### 5.2 Existing Endpoints (Retained)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/ready` | Readiness check |
| GET | `/health/live` | Liveness check |
| POST | `/api/v1/analysis/code` | Run code analysis |
| POST | `/api/v1/workflows/execute` | Execute workflow |

---

## 6. Phase Transition Rules

### 6.1 Gate Conditions

```
SPECIFY → PLAN:
  ✓ Specification document exists
  ✓ All required sections present
  ✓ User stories have acceptance criteria

PLAN → TASKS:
  ✓ Architecture document exists
  ✓ Tech stack defined
  ✓ Directory structure planned

TASKS → IMPLEMENT:
  ✓ Tasks defined with clear scope
  ✓ Dependencies identified
  ✓ Acceptance criteria for each task

IMPLEMENT → COMPLETE:
  ✓ All tasks completed
  ✓ Tests pass
  ✓ Documentation updated
```

### 6.2 Rollback Support

- Any phase can be re-entered for refinement
- Rolling back invalidates downstream phases
- State is preserved for comparison

---

## 7. Error Handling

### 7.1 Strategy

| Error Type | Handling |
|------------|----------|
| Validation Error | Return 400 with details |
| Phase Gate Failure | Return 422 with unmet conditions |
| Agent Failure | Retry with backoff, then fail gracefully |
| System Error | Return 500, log full trace |

### 7.2 Retry Policy

```python
RetryConfig:
  max_retries: 3
  initial_delay: 1.0  # seconds
  max_delay: 30.0
  exponential_base: 2
```

---

## 8. Security Considerations

- Input validation on all endpoints via Pydantic
- Shell command timeout (default 60s)
- Workspace path validation (no path traversal)
- No secrets in logs or responses

---

## 9. Testing Strategy

| Test Type | Scope | Coverage Target |
|-----------|-------|-----------------|
| Unit | Individual functions/classes | >80% |
| Integration | API endpoints | Key flows |
| E2E | Full SDD workflow | Happy path |

---

## 10. Deployment

### 10.1 Docker

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
# ... build steps ...

FROM python:3.11-slim as runtime
# Non-root user, minimal image
```

### 10.2 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENTFLOW_LOG_LEVEL` | Logging verbosity | INFO |
| `AGENTFLOW_TIMEOUT` | Default agent timeout | 300 |
| `AGENTFLOW_STATE_DIR` | State persistence path | .agentflow_state |

---

## Decision Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Keep file-based state | Simplicity for demo, no DB dependency | 2025-12-30 |
| Phase gates are soft | Allow override for learning/demo | 2025-12-30 |
| No real AI integration | Focus on patterns, not API costs | 2025-12-30 |
