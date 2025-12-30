# AgentFlow v0.2.0 Architecture Plan

## Metadata

```
PLAN_ID: 000-initial-implementation
SPEC_REF: .specify/specs/000-initial-implementation/spec.md
VERSION: v1.0.0
STATUS: Implemented
CREATED: 2025-12-30
AUTHOR: AgentFlow Team
```

## Architecture Overview

AgentFlow uses a layered architecture with phase-gated workflow management:

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   │
│  │ /health │ │ /phases │ │/analysis│ │   /workflows    │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Phase Manager                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ SPECIFY  │→│  PLAN    │→│  TASKS   │→│  IMPLEMENT   │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
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
│  │  Phases  │ │  Tools   │ │  State   │ │    Tasks     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Technical Approach

### Selected: Layered Architecture with Phase Gates

**Description:** Four-layer architecture (API, Phase Manager, Agents, Core) with explicit phase transitions and validation gates.

**Rationale:**
- Clear separation of concerns
- Phase gates enforce discipline
- Agents remain modular and testable
- Core components are reusable

## Design Details

### Data Models

```python
class Phase(str, Enum):
    SPECIFY = "specify"
    PLAN = "plan"
    TASKS = "tasks"
    IMPLEMENT = "implement"

class PhaseResult(BaseModel):
    phase: Phase
    status: PhaseStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    artifacts: Dict[str, Any]

class ProjectState(BaseModel):
    project_id: str
    current_phase: Phase
    phases: Dict[str, PhaseResult]
    specification: Optional[Dict]
    plan: Optional[Dict]
    tasks: List[Dict]

class AgentContext:
    task_id: str
    workspace_path: str
    current_phase: Optional[str]
    project_id: Optional[str]
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/project/create | Create SDD project |
| GET | /api/v1/project/{id}/status | Get project status |
| POST | /api/v1/phases/specify | Start specification |
| POST | /api/v1/phases/plan | Generate plan |
| POST | /api/v1/phases/tasks | Break into tasks |
| POST | /api/v1/phases/implement | Run implementation |
| GET | /health | Health check |

### Directory Structure

```
agentflow/
├── .specify/               # SDD artifacts
│   ├── memory/            # Constitution, context
│   ├── templates/         # Spec/plan/task templates
│   └── specs/             # Feature specifications
├── src/
│   ├── agents/            # Agent implementations
│   ├── api/               # FastAPI application
│   ├── core/              # Core (phases, state, tools)
│   └── utils/             # Utilities
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Security Considerations

- Input validation via Pydantic on all endpoints
- Shell command timeout (60s default)
- Workspace path validation (no traversal)
- No secrets in logs

## Testing Strategy

| Test Type | Scope | Files |
|-----------|-------|-------|
| Unit | Phase management | tests/unit/core/test_phases.py |
| Unit | Agents | tests/unit/agents/*.py |
| Integration | API | tests/integration/*.py |

## Dependencies

| Package | Purpose |
|---------|---------|
| FastAPI | REST API |
| Pydantic | Validation |
| structlog | Logging |
| pytest | Testing |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0.0 | 2025-12-30 | AgentFlow Team | Initial plan |
