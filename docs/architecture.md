# AgentFlow Architecture

## Overview

AgentFlow is a production-ready demonstration of agentic AI systems. It showcases how specialized AI agents can collaborate to automate complex development workflows using real tools.

## System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                   │
│  /health  /api/v1/workflows  /api/v1/analysis           │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│               Orchestrator Agent                         │
│  • Coordinates workflows                                 │
│  • Manages agent collaboration                           │
│  • Tracks execution state                                │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
┌────────▼─────┐ ┌───▼────┐ ┌────▼──────┐
│ Code Analyzer│ │Builder │ │GitHub     │
│   Agent      │ │ Agent  │ │Agent      │
│              │ │        │ │(Future)   │
│• Find TODOs  │ │• Tests │ │• PR mgmt  │
│• Security    │ │• Lint  │ │• Issues   │
│• Stats       │ │• Build │ │• Search   │
└────────┬─────┘ └───┬────┘ └────┬──────┘
         │           │           │
         └───────────┴───────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│              Core Infrastructure                        │
│  • Task Queue     • State Manager    • Tool Registry   │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. API Layer

**Technology**: FastAPI with Pydantic validation

**Responsibilities**:
- HTTP endpoints for workflows and analysis
- Request/response validation
- Health checks
- Error handling
- CORS and middleware

**Endpoints**:
- `GET /health` - Health check
- `POST /api/v1/workflows/execute` - Start a workflow
- `GET /api/v1/workflows/{id}/status` - Get workflow status
- `POST /api/v1/analysis/code` - Analyze code
- `POST /api/v1/analysis/build` - Run build/tests

### 2. Agent Layer

#### Base Agent (`BaseAgent`)

Abstract base class providing:
- Execution framework with retry logic
- Error handling and timeout management
- Status tracking and statistics
- Context validation

All specialized agents inherit from this.

#### Code Analyzer Agent

**Tools Used**: `grep`, `glob`, `file_system`

**Capabilities**:
- Find TODOs, FIXMEs, HACKs
- Detect security issues (hardcoded secrets, SQL injection patterns)
- Calculate code statistics (files, lines, test coverage)
- Generate actionable summary

#### Builder Agent

**Tools Used**: `shell` (bash)

**Capabilities**:
- Run linters (ruff, black)
- Execute test suites (pytest)
- Type checking (mypy)
- Build packages
- Dependency management

#### Orchestrator Agent

**Responsibilities**:
- Coordinate multiple agents
- Manage workflow state
- Handle agent dependencies
- Generate comprehensive reports

**Workflows**:
- `code_review` - Full code analysis + build
- `pr_check` - Validate pull request
- `dependency_audit` - Check dependencies

### 3. Core Infrastructure

#### Task Queue (`TaskQueue`)

**Features**:
- Priority-based scheduling
- Dependency management
- Retry logic
- Concurrent execution control

**Design**:
- Async/await based
- Thread-safe with locks
- Configurable concurrency limits

#### State Manager (`StateManager`)

**Features**:
- Workflow state persistence
- Agent state tracking
- Progress monitoring
- Cleanup of old states

**Storage**: File-based (JSON) in `.agentflow_state/`

#### Tool Registry (`ToolRegistry`)

**Features**:
- Centralized tool management
- Tool discovery and execution
- Result standardization

**Available Tools**:
- `FileSystemTool` - Read/write/list files
- `ShellTool` - Execute shell commands
- `GrepTool` - Search file contents

### 4. Utilities

#### Logging (`src/utils/logging.py`)

- Structured logging with `structlog`
- JSON output for production
- Pretty console for development
- Context binding for tracing

#### Configuration (`src/utils/config.py`)

- Environment-based settings
- Pydantic validation
- Type-safe configuration
- Defaults for all environments

## Data Flow

### Workflow Execution Flow

```
1. API Request
   ↓
2. Create AgentContext
   ↓
3. Orchestrator.run(context)
   ↓
4. Create WorkflowState
   ↓
5. Execute Agents in Sequence/Parallel
   │
   ├─→ Code Analyzer
   │   ├─→ Find TODOs (grep)
   │   ├─→ Security scan (grep)
   │   └─→ Code stats (glob + file_system)
   │
   └─→ Builder
       ├─→ Run linting (shell: ruff, black)
       ├─→ Run tests (shell: pytest)
       └─→ Type check (shell: mypy)
   ↓
6. Update WorkflowState
   ↓
7. Generate Summary
   ↓
8. Return WorkflowResponse
```

## Design Patterns

### 1. Agent Pattern

Each agent is self-contained with:
- Configuration
- Execution logic
- Error handling
- Result generation

### 2. Strategy Pattern

Tools are interchangeable implementations:
```python
tool = registry.get_tool("shell")
result = await tool.execute(command="pytest")
```

### 3. Observer Pattern

State manager tracks workflow progress:
```python
await state_manager.update_agent_state(
    workflow_id=wf_id,
    agent_name="builder",
    agent_data=result.dict()
)
```

### 4. Command Pattern

Tasks encapsulate operations:
```python
task = Task(
    name="analyze",
    agent_name="code_analyzer",
    input_data={...}
)
```

## Scalability Considerations

### Current Design

- Async/await for I/O operations
- Configurable concurrency limits
- File-based state (simple, portable)

### Future Enhancements

1. **Distributed Task Queue**
   - Redis/RabbitMQ for task queue
   - Multiple worker processes

2. **Database State Management**
   - PostgreSQL for workflow state
   - Better querying and analytics

3. **Caching Layer**
   - Redis for agent results
   - Reduce duplicate work

4. **Horizontal Scaling**
   - Multiple API instances
   - Load balancer (nginx/traefik)

## Security

### Current Measures

- No execution of untrusted code
- Workspace isolation
- Configurable timeouts
- Input validation (Pydantic)

### Best Practices

- Run in containers (Docker)
- Non-root user
- Read-only file system (where possible)
- Network isolation

## Monitoring & Observability

### Logging

- Structured JSON logs
- Request tracing
- Error tracking
- Performance metrics

### Health Checks

- `/health` - Basic liveness
- `/health/ready` - Readiness probe
- `/health/live` - Liveness probe

### Metrics (Future)

- Prometheus metrics
- Grafana dashboards
- Alert rules

## Testing Strategy

### Unit Tests

- Individual agent logic
- Core infrastructure
- Tool implementations

### Integration Tests

- Full workflow execution
- API endpoint testing
- Agent collaboration

### Coverage Goals

- >80% line coverage
- Critical paths at 100%

## Deployment

### Docker

```bash
docker build -t agentflow .
docker run -p 8000:8000 agentflow
```

### Docker Compose

```bash
docker-compose up -d
```

### Kubernetes (Future)

- Deployment manifests
- Service definitions
- Ingress configuration
- ConfigMaps and Secrets
