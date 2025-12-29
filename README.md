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

### Docker

```bash
docker build -t agentflow .
docker run -p 8000:8000 agentflow
```

## 📖 Usage Examples

### Analyze a Codebase

```python
from src.agents.code_analyzer import CodeAnalyzerAgent

agent = CodeAnalyzerAgent()
results = await agent.analyze_codebase("/path/to/repo")
print(results.summary)
```

### Automated PR Review

```python
from src.agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()
await orchestrator.review_pull_request(
    owner="user",
    repo="project",
    pr_number=123
)
```

### API Usage

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/repo"}'

# Review PR
curl -X POST http://localhost:8000/api/v1/github/review-pr \
  -H "Content-Type: application/json" \
  -d '{"owner": "user", "repo": "project", "pr_number": 123}'
```

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

- [Architecture Overview](docs/architecture.md)
- [Agent Design](docs/agents.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)

## 🎪 Demo Scenarios

### 1. Intelligent Code Review
```bash
python -m src.cli analyze --repo /path/to/repo --full-report
```

### 2. PR Preparation
```bash
python -m src.cli github review-pr --owner user --repo project --pr 123
```

### 3. Dependency Audit
```bash
python -m src.cli audit --check-security --check-updates
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
