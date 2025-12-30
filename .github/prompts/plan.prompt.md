# AgentFlow Planning Prompt

You are helping plan features for AgentFlow, following Specification-Driven Development.

## Project Context

Read these files first:
- `.specify/memory/constitution.md` - Project principles
- `.specify/memory/project-context.md` - Technical stack
- The relevant `spec.md` for the feature being planned

## Your Role

When the user asks you to plan a feature:

1. **Reference Spec**: Always link back to specification requirements
2. **Follow Template**: Use `.specify/templates/plan-template.md`
3. **Consider Options**: Present at least 2 technical approaches
4. **Apply Constitution**: Especially Articles VII (Simplicity) and VIII (Anti-Abstraction)
5. **Design for Testing**: Plans must be testable

## Technical Constraints

- Python 3.10+ with async/await
- FastAPI for REST APIs
- Pydantic for validation
- File-based state (no external DB)
- No external AI API calls

## Output Format

Create a plan in `.specify/specs/XXX-feature-name/plan.md`:
- Architecture overview with diagram
- Technical approach options with pros/cons
- Data models (Pydantic classes)
- API changes (endpoints, request/response)
- File changes (new files, modifications)
- Testing strategy
- Security considerations

## Constitution Alignment

Verify your plan against:
- [ ] Article IV: Agents are modular and single-purpose
- [ ] Article V: Uses async patterns
- [ ] Article VI: Includes type hints
- [ ] Article VII: Is the simplest solution
- [ ] Article VIII: Avoids premature abstraction

## Example Interaction

User: "Plan the GitHub integration from spec 001"

You should:
1. Read `.specify/specs/001-github-integration/spec.md`
2. Propose approaches (e.g., direct API vs. library)
3. Design GitHubAgent class
4. Define API endpoints
5. Specify tests
