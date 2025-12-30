# Specification-Driven Development (SDD) Guide

## Overview

This guide explains how AgentFlow demonstrates **Specification-Driven Development (SDD)** using GitHub's Spec Kit methodology.

SDD is a structured approach where **specifications are the central artifact** that drive all development activities.

---

## The Four Phases

SDD follows a gated workflow with four distinct phases:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────────┐
│ SPECIFY │ →  │  PLAN   │ →  │  TASKS  │ →  │ IMPLEMENT │
└─────────┘    └─────────┘    └─────────┘    └───────────┘
     ↑                                              │
     └──────────────────────────────────────────────┘
                    (Feedback Loop)
```

### Phase 1: SPECIFY

**Goal:** Define *what* to build in plain language.

**Artifacts:** `.spec/specification.md`

**Contains:**
- Problem statement
- User stories with acceptance criteria
- Core concepts and terminology
- Non-functional requirements
- Success metrics
- Out of scope items

**Example:**
```markdown
## User Stories

### 3.1 Developer Workflow Automation
> As a developer, I want to automate code analysis so that I can focus on higher-value work.

**Acceptance Criteria:**
- [ ] Can analyze code for issues and TODOs
- [ ] Can run builds and tests automatically
- [ ] Generates actionable reports
```

### Phase 2: PLAN

**Goal:** Define *how* to build it.

**Artifacts:** `.spec/plan.md`

**Contains:**
- High-level architecture
- Technology stack decisions
- Directory structure
- Data models
- API design
- Security considerations
- Testing strategy

**Example:**
```markdown
## Technology Stack

| Dependency | Purpose | Version |
|------------|---------|---------|
| FastAPI | REST API framework | >=0.109.0 |
| Pydantic | Data validation | >=2.5.0 |
| structlog | Structured logging | >=24.1.0 |
```

### Phase 3: TASKS

**Goal:** Break the plan into actionable work units.

**Artifacts:** `.spec/tasks.md`

**Contains:**
- Epics (major feature areas)
- Individual tasks with:
  - Status (🔴 Not Started, 🟡 In Progress, 🟢 Completed)
  - Estimate
  - Target file(s)
  - Description
  - Acceptance criteria
- Progress tracking

**Example:**
```markdown
### Task 1.1: Create Phase Models
**Status:** 🟢 Completed
**Estimate:** 30 min
**File:** `src/core/phases.py`

**Acceptance Criteria:**
- [x] Phase enum with SPECIFY, PLAN, TASKS, IMPLEMENT values
- [x] PhaseStatus enum
- [x] Unit tests pass
```

### Phase 4: IMPLEMENT

**Goal:** Execute tasks and validate against specifications.

**Artifacts:** `.spec/implementation.md` + actual code

**Contains:**
- Session logs
- Key decisions made during implementation
- Deviations from plan
- Lessons learned
- Metrics

---

## Navigating the `.spec/` Directory

```
.spec/
├── specification.md   # Start here - understand the "what"
├── plan.md           # Next - understand the "how"
├── tasks.md          # Then - see the work breakdown
└── implementation.md # Finally - track progress and decisions
```

### Reading Order for New Contributors

1. **specification.md** - Understand the problem and requirements
2. **plan.md** - Understand technical decisions
3. **tasks.md** - See what's done and what's remaining
4. **implementation.md** - Understand why things were done a certain way

---

## Using the Phase API

AgentFlow exposes phase management via REST API:

### Create a Project
```bash
curl -X POST http://localhost:8000/api/v1/project/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "my-project", "project_name": "My SDD Project"}'
```

### Start Specification Phase
```bash
curl -X POST http://localhost:8000/api/v1/phases/specify \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "my-project",
    "specification": {
      "title": "My Project",
      "description": "A demonstration project",
      "user_stories": ["As a user, I want..."]
    }
  }'
```

### Move to Plan Phase
```bash
curl -X POST http://localhost:8000/api/v1/phases/plan \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "my-project",
    "plan": {
      "architecture": "Layered",
      "stack": ["Python", "FastAPI", "Pydantic"]
    }
  }'
```

### Check Project Status
```bash
curl http://localhost:8000/api/v1/project/my-project/status
```

### Get Workflow Info
```bash
curl http://localhost:8000/api/v1/phases/workflow
```

---

## Phase Gates

Each phase transition has **validation gates** that ensure quality:

| Transition | Requirements |
|------------|-------------|
| SPECIFY → PLAN | Specification document exists |
| PLAN → TASKS | Plan document exists |
| TASKS → IMPLEMENT | Task breakdown exists |

Gates can be bypassed with `force=true` for learning/exploration.

---

## Why SDD?

### Problems with "Vibe Coding"

Traditional AI-assisted coding often involves:
- Vague prompts → unpredictable results
- No documentation → hard to maintain
- No traceability → unclear why decisions were made
- Scope creep → projects grow without bounds

### Benefits of SDD

1. **Clarity** - Everyone knows what's being built
2. **Traceability** - Every line of code traces to a requirement
3. **Quality Gates** - Prevents moving forward without validation
4. **Documentation** - Specs become living documentation
5. **Predictability** - AI produces more consistent results

---

## Applying SDD to Your Projects

### Step 1: Start with a Specification

Before writing code, write a specification:
- What problem are you solving?
- Who are the users?
- What are the acceptance criteria?

### Step 2: Create a Plan

Decide on architecture and technology:
- What's the high-level design?
- What libraries/frameworks?
- What's the directory structure?

### Step 3: Break Down into Tasks

Make tasks small and testable:
- Each task should be completable in 1-2 hours
- Each task should have clear acceptance criteria
- Dependencies should be explicit

### Step 4: Implement Iteratively

Work through tasks systematically:
- Check off acceptance criteria as you go
- Update specs if requirements change
- Log decisions in implementation notes

---

## Example Workflow

```bash
# 1. Initialize project
specify init my-project --ai copilot

# 2. Write specification
/specify "Build a REST API for managing tasks with CRUD operations"

# 3. Generate plan
/plan

# 4. Break into tasks
/tasks

# 5. Implement
/implement
```

---

## Further Reading

- [GitHub Spec Kit Documentation](https://speckit.org/)
- [Spec-Driven Development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [AgentFlow Architecture](./architecture.md)
- [AgentFlow API Reference](./api.md)
