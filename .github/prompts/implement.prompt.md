# AgentFlow Implementation Prompt

You are implementing features for AgentFlow following Specification-Driven Development.

## Project Context

Read these files in order:
1. `.specify/memory/constitution.md` - MUST follow all articles
2. The feature's `spec.md` - Requirements to implement
3. The feature's `plan.md` - Architecture to follow
4. The feature's `tasks.md` - Current task to work on

## Your Role

When implementing:

1. **Follow the Plan**: Don't deviate without updating plan first
2. **One Task at a Time**: Complete current task before moving on
3. **Test First**: Write or update tests with implementation
4. **Type Everything**: Full type hints, Pydantic models
5. **Update Tasks**: Mark completed, note any blockers

## Code Standards

```python
# Good: Type hints, docstrings, async
async def analyze_code(self, context: AgentContext) -> AgentResult:
    """
    Analyze code in the workspace.
    
    Args:
        context: Agent execution context
        
    Returns:
        AgentResult with analysis data
    """
    ...

# Bad: No types, no docs
def analyze(ctx):
    ...
```

## Constitution Compliance

Every implementation must:
- [ ] Article I: Have a specification first
- [ ] Article II: Go through proper phases
- [ ] Article III: Include tests
- [ ] Article VI: Use type hints
- [ ] Article VII: Be simple
- [ ] Article IX: Update docs if needed

## File Organization

```
src/
├── agents/      # New agents go here
├── api/routes/  # New endpoints go here
├── core/        # Core infrastructure
└── utils/       # Utilities
tests/
├── unit/        # Unit tests mirror src/
└── integration/ # API/workflow tests
```

## After Implementation

1. Run tests: `pytest tests/`
2. Run linter: `ruff check src/`
3. Type check: `mypy src/`
4. Update task status in `tasks.md`
5. Commit with reference to task ID
