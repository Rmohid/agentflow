# AgentFlow Constitution

```
CONSTITUTION_VERSION: v1.0.0
RATIFICATION_DATE: 2025-12-30
LAST_AMENDED_DATE: 2025-12-30
```

## Purpose

This constitution establishes the immutable architectural principles and governance rules for AgentFlow. All specifications, plans, and implementations must align with these articles. AI agents and human developers reference this document as the source of truth for project direction.

---

## Article I: Specification-First Principle

**All development begins with a specification.**

- No code shall be written without a corresponding specification
- Specifications define the "what" before implementation defines the "how"
- Changes to functionality require specification updates first
- Specifications are living documents that evolve with the codebase

**Rationale:** Specification-first development ensures clarity of intent, reduces ambiguity, and provides traceability from requirements to implementation.

---

## Article II: Phase-Gated Development

**Development follows the four-phase SDD workflow: Specify → Plan → Tasks → Implement.**

- Each phase must produce artifacts before proceeding
- Phase gates validate completeness and quality
- Rollback is permitted for refinement
- Force-bypass is allowed for learning/exploration but discouraged for production

**Rationale:** Gated phases prevent premature implementation and ensure each stage receives proper attention.

---

## Article III: Test-First Implementation

**Tests accompany all implementation work.**

- Unit tests required for new modules
- Test coverage target: >80%
- Tests validate against specification acceptance criteria
- Failing tests block merges to main

**Rationale:** Tests provide confidence, documentation, and regression protection.

---

## Article IV: Agent Modularity

**AI agents are modular, single-purpose, and composable.**

- Each agent has one clear responsibility
- Agents communicate via well-defined interfaces (AgentContext, AgentResult)
- Agents can be registered/unregistered with orchestrators
- Agent failures are isolated and do not cascade

**Rationale:** Modularity enables testing, replacement, and scaling of individual capabilities.

---

## Article V: Async-First Architecture

**All I/O operations use async/await patterns.**

- Agents execute asynchronously
- API endpoints are async
- Blocking operations are wrapped or avoided
- Concurrency is managed via asyncio primitives

**Rationale:** Async architecture enables efficient resource utilization and responsive APIs.

---

## Article VI: Type Safety

**All code uses type hints and validation.**

- Function signatures include type hints
- Pydantic models validate external data
- mypy strict mode enforced in CI
- No `Any` types without explicit justification

**Rationale:** Type safety catches errors early and serves as documentation.

---

## Article VII: Simplicity Gate

**Prefer simple solutions over complex ones.**

- New abstractions require justification
- Favor standard library over external dependencies
- Code should be readable by junior developers
- If a solution requires extensive documentation, simplify it

**Rationale:** Simplicity reduces bugs, improves maintainability, and lowers onboarding cost.

---

## Article VIII: Anti-Abstraction Gate

**Avoid premature abstraction.**

- Wait for three concrete use cases before abstracting
- Duplication is preferable to wrong abstraction
- Extract patterns only when they prove stable
- Configuration over code where appropriate

**Rationale:** Premature abstraction creates rigid, hard-to-change architectures.

---

## Article IX: Documentation-as-Code

**Documentation lives alongside code and is version-controlled.**

- README, API docs, and guides in repository
- Specifications in `.specify/` directory
- Architecture decisions recorded in implementation logs
- Outdated documentation is a bug

**Rationale:** Co-located documentation stays current and is discoverable.

---

## Governance

### Amendment Process

1. Propose amendment via pull request to this file
2. Discuss in PR comments with stakeholders
3. Require approval from project maintainers
4. Update `LAST_AMENDED_DATE` and increment version
5. Document rationale in commit message

### Versioning Policy

- **MAJOR:** Fundamental principle changes
- **MINOR:** New articles or significant clarifications
- **PATCH:** Typos, formatting, minor wording changes

### Compliance Review

- All PRs checked against constitution principles
- CI enforces testable requirements (coverage, types)
- Code reviews verify architectural alignment
- Quarterly constitution review for relevance

---

## Ratification

This constitution was ratified on 2025-12-30 as the foundational governance document for AgentFlow.

Signed: AgentFlow Development Team
