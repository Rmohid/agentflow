# 🤖 AgentFlow

**AI-Powered Development Workflow Orchestrator**

A production-ready demonstration of **Specification-Driven Development (SDD)** using GitHub's Spec Kit methodology, showcasing how agentic AI systems can be built with structured, documented specifications at their core.

---

## 🎯 What is AgentFlow?

AgentFlow demonstrates two key concepts:

### 1. Specification-Driven Development (SDD)
This project itself was built using SDD - a structured workflow where **specifications are the central artifact**:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────────┐
│ SPECIFY │ →  │  PLAN   │ →  │  TASKS  │ →  │ IMPLEMENT │
└─────────┘    └─────────┘    └─────────┘    └───────────┘
```

Explore the `.spec/` directory to see how this project evolved from requirements to code:
- [`.spec/specification.md`](.spec/specification.md) - What we're building
- [`.spec/plan.md`](.spec/plan.md) - How we're building it
- [`.spec/tasks.md`](.spec/tasks.md) - Work breakdown
- [`.spec/implementation.md`](.spec/implementation.md) - Implementation log

### 2. Multi-Agent AI Architecture
AgentFlow showcases how AI agents can collaborate to automate complex development workflows:

- **Code Analyzer Agent**: Scans codebases for patterns, issues, and improvements
- **Builder Agent**: Runs tests, linters, and builds
- **Orchestrator Agent**: Coordinates agent collaboration

## ✨ Features

### SDD Workflow (Spec Kit)
- ✅ Four-phase gated workflow (Specify → Plan → Tasks → Implement)
- ✅ Phase validation gates
- ✅ Living specification documents in `.spec/`
- ✅ Traceability from requirements to code

### Multi-Agent Architecture
- ✅ REST API with FastAPI
- ✅ Comprehensive test suite (>80% coverage)
- ✅ CI/CD with GitHub Actions
- ✅ Structured logging and monitoring
- ✅ Docker containerization
- ✅ Type-safe with Pydantic models

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentflow.git
cd agentflow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Start the API server
uvicorn src.api.main:app --reload
```

### 🎓 Interactive Learning Tool

**New to AgentFlow?** Start with our interactive tutorial!

```bash
# Run the interactive learning script
python learn.py
```

This will:
- Create a sample workspace with code issues
- Guide you through each agent step-by-step
- Show real-time results and explanations
- Let you reset and repeat as many times as needed

See [docs/learning-tool.md](docs/learning-tool.md) for details.

### Docker

```bash
docker build -t agentflow .
docker run -p 8000:8000 agentflow
```

## 📖 Usage Examples

### 1. Interactive Learning (Recommended for Beginners)

```bash
# Start the interactive tutorial
python learn.py
```

### 2. Quick Demo

```bash
# Run all agents on the current project
python demo.py
```

### 3. Direct Agent Usage

```python
import asyncio
from pathlib import Path
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.base import AgentContext

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

### 4. Orchestrated Workflow

```python
from src.agents.orchestrator import OrchestratorAgent
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.builder import BuilderAgent

# Create and configure orchestrator
orchestrator = OrchestratorAgent()
orchestrator.register_agent(CodeAnalyzerAgent())
orchestrator.register_agent(BuilderAgent())

# Run code review workflow
context = AgentContext(
    task_id="code-review",
    workspace_path="./my-project",
    config={"workflow_type": "code_review"}
)
result = await orchestrator.run(context)
print(result.data["summary"])
```

### 5. SDD Phase API (New!)

```bash
# Create an SDD project
curl -X POST http://localhost:8000/api/v1/project/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "my-project", "project_name": "My SDD Project"}'

# Complete specification phase
curl -X POST http://localhost:8000/api/v1/phases/specify \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "my-project",
    "specification": {"title": "My App", "description": "..."}
  }'

# Move through phases: plan → tasks → implement
curl -X POST http://localhost:8000/api/v1/phases/plan \
  -H "Content-Type: application/json" \
  -d '{"project_id": "my-project", "plan": {"architecture": "layered"}}'

# Check project status
curl http://localhost:8000/api/v1/project/my-project/status
```

### 6. API Usage

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST http://localhost:8000/api/v1/analysis/code \
  -H "Content-Type: application/json" \
  -d '{"workspace_path": "/path/to/repo"}'

# Execute workflow
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "code_review",
    "workspace_path": "/path/to/repo"
  }'
```

For more examples, see [QUICKSTART.md](QUICKSTART.md)

## 🏗️ Architecture

### SDD Phase Flow
```
┌─────────────────────────────────────────────────────────────┐
│                      SDD Phases                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ SPECIFY  │→│  PLAN    │→│  TASKS   │→│  IMPLEMENT   │   │
│  │ .spec/   │ │ .spec/   │ │ .spec/   │ │  src/        │   │
│  │ spec.md  │ │ plan.md  │ │ tasks.md │ │  code        │   │
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
│  │  Phases  │ │  Tools   │ │  State   │ │    Tasks     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for detailed design.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/agents/test_code_analyzer.py

# Run integration tests only
pytest tests/integration/
```

## 📚 Documentation

- [**SDD Guide**](docs/sdd-guide.md) - Learn Specification-Driven Development
- [Architecture Overview](docs/architecture.md) - System design and patterns
- [API Documentation](docs/api.md) - REST API reference
- [Learning Tool](docs/learning-tool.md) - Interactive tutorial guide
- [Quick Start](QUICKSTART.md) - Installation and first steps

## 🎪 Demo Scenarios

### 1. Interactive Learning (Best for First-Time Users)
```bash
python learn.py
# Interactive step-by-step tutorial with sample workspace
```

### 2. Quick Demo on Current Project
```bash
python demo.py
# Runs all agents on the agentflow project itself
```

### 3. Code Review Workflow
```bash
# Start API server
uvicorn src.api.main:app --reload

# In another terminal
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "code_review", "workspace_path": "."}'
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run linters
ruff check src/
black src/

# Type checking
mypy src/
```

### Project Structure

```
agentflow/
├── .spec/               # SDD Specification Artifacts
│   ├── specification.md # Requirements & user stories
│   ├── plan.md         # Architecture & tech decisions
│   ├── tasks.md        # Work breakdown
│   └── implementation.md # Implementation log
├── src/
│   ├── agents/          # Agent implementations
│   ├── api/             # FastAPI application
│   ├── core/            # Core functionality (phases, state, tools)
│   └── utils/           # Utilities
├── tests/               # Test suite
├── docs/                # Documentation
└── .github/workflows/   # CI/CD
```

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built to demonstrate:
- **GitHub Spec Kit** - Specification-Driven Development methodology
- **Agentic AI patterns** - Multi-agent orchestration
- **Modern Python** - Async patterns, type hints, Pydantic
- **Production practices** - Testing, CI/CD, Docker

---

**Built with ❤️ as a demonstration of Specification-Driven Development with agentic AI**
