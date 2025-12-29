# Quick Start Guide

## Installation

1. **Clone and setup**:
```bash
cd agentflow
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

2. **Verify installation**:
```bash
python -c "import src; print('✓ AgentFlow installed successfully')"
```

## Running the Demo

### Option 1: Interactive Demo Script

```bash
python demo.py
```

This will run three demos:
- Code Analyzer scanning the project
- Builder running lints and tests
- Orchestrator coordinating a full workflow

### Option 2: API Server

```bash
# Start the server
uvicorn src.api.main:app --reload

# In another terminal, test the API
curl http://localhost:8000/health

# Analyze this project
curl -X POST http://localhost:8000/api/v1/analysis/code \
  -H "Content-Type: application/json" \
  -d '{"workspace_path": "."}'
```

### Option 3: Direct Python Usage

```python
import asyncio
from pathlib import Path
from src.agents.base import AgentContext
from src.agents.code_analyzer import CodeAnalyzerAgent

async def analyze():
    agent = CodeAnalyzerAgent()
    context = AgentContext(
        task_id="my-analysis",
        workspace_path=str(Path.cwd())
    )
    result = await agent.run(context)
    print(result.data["summary"])

asyncio.run(analyze())
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_code_analyzer.py -v

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

## Docker

```bash
# Build image
docker build -t agentflow .

# Run container
docker run -p 8000:8000 agentflow

# Or use docker-compose
docker-compose up
```

## Project Structure

```
agentflow/
├── src/
│   ├── agents/          # Agent implementations
│   │   ├── base.py              # Base agent class
│   │   ├── code_analyzer.py     # Code analysis agent
│   │   ├── builder.py           # Build/test agent
│   │   └── orchestrator.py      # Workflow orchestrator
│   ├── api/             # FastAPI application
│   │   ├── main.py              # API entrypoint
│   │   └── routes/              # API endpoints
│   ├── core/            # Core infrastructure
│   │   ├── task_queue.py        # Task management
│   │   ├── state.py             # State persistence
│   │   └── tools.py             # Tool wrappers
│   └── utils/           # Utilities
│       ├── config.py            # Configuration
│       └── logging.py           # Logging setup
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
├── Dockerfile           # Container image
└── demo.py              # Demo script
```

## Key Features to Explore

### 1. Code Analysis
```bash
# Find TODOs, security issues, code stats
python -c "
import asyncio
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.base import AgentContext

async def run():
    agent = CodeAnalyzerAgent()
    result = await agent.run(AgentContext('test', '.'))
    print(result.data['summary'])

asyncio.run(run())
"
```

### 2. Build Automation
```bash
# Run linting, tests, type checking
python -c "
import asyncio
from src.agents.builder import BuilderAgent
from src.agents.base import AgentContext

async def run():
    agent = BuilderAgent()
    result = await agent.run(AgentContext('test', '.'))
    print(result.data['summary'])

asyncio.run(run())
"
```

### 3. Workflow Orchestration
```bash
# Coordinate multiple agents
python demo.py
```

## Troubleshooting

### ModuleNotFoundError
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall in editable mode
pip install -e ".[dev]"
```

### Tests Failing
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run tests with verbose output
pytest -vv
```

### API Not Starting
```bash
# Check if port 8000 is available
lsof -i :8000

# Try a different port
uvicorn src.api.main:app --port 8001
```

## Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Read the docs**: `docs/architecture.md` and `docs/api.md`
3. **Add new agents**: Extend `BaseAgent` class
4. **Customize workflows**: Modify `orchestrator.py`
5. **Deploy**: Use Docker or Kubernetes

## Example Workflows

### Code Review Workflow
```bash
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "code_review",
    "workspace_path": "."
  }'
```

### PR Check Workflow
```bash
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "pr_check",
    "workspace_path": "."
  }'
```

## Support

- Documentation: `docs/`
- Issues: Create an issue on GitHub
- Questions: Check `README.md` and `docs/architecture.md`
