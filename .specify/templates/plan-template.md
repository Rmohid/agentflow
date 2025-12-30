# Feature Plan

## Metadata

```
PLAN_ID: [XXX-feature-name]
SPEC_REF: [Link to specification]
VERSION: v1.0.0
STATUS: [Draft | In Review | Approved]
CREATED: [YYYY-MM-DD]
AUTHOR: [Name]
```

## Architecture Overview

[High-level description of how this feature fits into the system]

### Component Diagram

```
[ASCII or description of component relationships]
```

## Technical Approach

### Option 1: [Name]
**Description:** [How this approach works]

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

### Option 2: [Name]
**Description:** [How this approach works]

**Pros:**
- Pro 1

**Cons:**
- Con 1

### Selected Approach
[Which option and why]

## Design Details

### Data Models

```python
class ExampleModel(BaseModel):
    field1: str
    field2: int
```

### API Changes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/example | Creates example |
| GET | /api/v1/example/{id} | Gets example |

### File Changes

| File | Change Type | Description |
|------|-------------|-------------|
| src/example.py | New | New module |
| src/api/routes/example.py | New | API routes |

## Security Considerations

- [Security consideration 1]
- [Security consideration 2]

## Testing Strategy

| Test Type | Scope | Description |
|-----------|-------|-------------|
| Unit | ExampleClass | Test core logic |
| Integration | API | Test endpoints |

## Migration Plan

[If applicable, how to migrate existing data/users]

## Rollback Plan

[How to revert if something goes wrong]

## Dependencies

- [External library or service]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation] |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0.0 | YYYY-MM-DD | [Name] | Initial plan |
