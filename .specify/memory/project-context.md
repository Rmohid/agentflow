# AgentFlow Project Context

## Overview

AgentFlow is an AI-Powered Development Workflow Orchestrator that demonstrates Specification-Driven Development (SDD) using GitHub's Spec Kit methodology.

## Project Goals

1. **Educational**: Serve as a reference implementation for SDD
2. **Practical**: Provide working agent-based automation
3. **Production-Ready**: Demonstrate real-world best practices

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.10+ |
| Web Framework | FastAPI | >=0.109.0 |
| Validation | Pydantic | >=2.5.0 |
| Logging | structlog | >=24.1.0 |
| Testing | pytest | >=7.4.0 |

## Architecture Principles

- **Phase-Gated Workflow**: Specify → Plan → Tasks → Implement
- **Multi-Agent**: Specialized agents coordinated by orchestrator
- **Async-First**: All I/O operations are asynchronous
- **Type-Safe**: Full type hints with Pydantic validation

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| File-based state | Simplicity, no external DB dependency |
| No real AI API calls | Focus on patterns, not API costs |
| Soft phase gates | Learning-friendly, can be overridden |

## Team Conventions

- Follow PEP 8 with 100-char line limit
- Use Google-style docstrings
- Prefix private methods with underscore
- Tests mirror source structure

## Links

- [Constitution](.specify/memory/constitution.md)
- [Current Specification](.specify/specs/000-initial-implementation/spec.md)
