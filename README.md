# 🤖 AgentFlow

**AI-Powered Development Workflow Orchestrator**

A production-ready demonstration of agentic AI systems using GitHub Copilot's toolset to autonomously handle real-world development tasks.

---

## 🎯 What is AgentFlow?

AgentFlow showcases how AI agents can collaborate to automate complex development workflows using the same tools available to GitHub Copilot:

- **File Operations**: Read, analyze, and modify code
- **Shell Commands**: Build, test, and deploy applications
- **GitHub APIs**: Manage issues, PRs, and workflows
- **Web Search**: Research best practices and solutions

## ✨ Features

### Multi-Agent Architecture
- **Code Analyzer Agent**: Scans codebases for patterns, issues, and improvements
- **Builder Agent**: Runs tests, linters, and builds
- **GitHub Agent**: Manages GitHub resources (PRs, issues, workflows)
- **Research Agent**: Finds solutions and best practices
- **Orchestrator Agent**: Coordinates agent collaboration

### Production-Ready
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

### 5. API Usage

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

```
┌─────────────┐
│ Orchestrator│  ← Coordinates agent workflow
└──────┬──────┘
       │
       ├──────┬──────┬──────┬──────┐
       ▼      ▼      ▼      ▼      ▼
    ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
    │Code│ │Build│ │Git │ │Res │ │API │
    │Anlz│ │ er │ │Hub │ │earch│ │Svc │
    └────┘ └────┘ └────┘ └────┘ └────┘
       │      │      │      │      │
       └──────┴──────┴──────┴──────┘
                    ▼
              ┌────────────┐
              │Task Queue  │
              │& State Mgmt│
              └────────────┘
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
├── src/
│   ├── agents/          # Agent implementations
│   ├── api/             # FastAPI application
│   ├── core/            # Core functionality
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

Built to demonstrate agentic AI patterns using:
- GitHub Copilot's tool ecosystem
- Modern Python async patterns
- Production-ready software practices

---

**Built with ❤️ as a demonstration of production-ready agentic AI systems**
