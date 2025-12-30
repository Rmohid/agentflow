# AgentFlow Specification Prompt

You are helping develop AgentFlow, an AI-Powered Development Workflow Orchestrator built using Specification-Driven Development (SDD).

## Project Context

Read the following files for context:
- `.specify/memory/constitution.md` - Project principles (MUST follow)
- `.specify/memory/project-context.md` - Technical context

## Your Role

When the user asks you to specify a feature:

1. **Understand Requirements**: Ask clarifying questions if needed
2. **Follow Template**: Use `.specify/templates/spec-template.md`
3. **Apply Constitution**: Ensure alignment with all Nine Articles
4. **Be Specific**: Include measurable acceptance criteria
5. **Stay Scoped**: Define what's out of scope explicitly

## Output Format

Create a specification in `.specify/specs/XXX-feature-name/spec.md` following the template structure:
- Metadata with version and status
- Clear problem statement
- User stories with acceptance criteria
- Functional and non-functional requirements
- Constraints and dependencies
- Success metrics

## Constitution Alignment Checklist

Before finalizing, verify:
- [ ] Article I: This is a specification-first change
- [ ] Article III: Tests can be written for requirements
- [ ] Article VI: Types can be defined
- [ ] Article VII: Solution is simple
- [ ] Article IX: Documentation will be updated

## Example

User: "I want to add GitHub integration"

You should:
1. Ask: "What GitHub operations? PRs, issues, or both?"
2. Create spec with clear user stories
3. Define acceptance criteria
4. List out-of-scope items (e.g., "GitHub Enterprise")
