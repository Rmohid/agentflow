# 🎓 Learning Tool Guide

## Interactive Learning Script

The `learn.py` script provides an **interactive, step-by-step tutorial** to learn how to use AgentFlow's agentic AI workflows.

## Features

- ✅ **Guided Tutorial**: Step-by-step walkthrough of each agent
- ✅ **Sample Workspace**: Automatically creates code with intentional issues
- ✅ **Interactive Prompts**: Learn at your own pace
- ✅ **Colorful Output**: Easy-to-read terminal output
- ✅ **Reset Capability**: Run the tutorial multiple times
- ✅ **Auto Cleanup**: Removes workspace when done

## Quick Start

```bash
# From the agentflow directory
python learn.py
```

## What You'll Learn

### Step 0: Setup
- Creating a sample workspace
- Understanding the project structure
- Seeing intentional code issues

### Step 1: Code Analyzer Agent
- Finding TODOs and FIXMEs
- Detecting security issues
- Getting code statistics
- Interpreting results

### Step 2: Builder Agent
- Running linters (ruff, black)
- Executing tests (pytest)
- Type checking (mypy)
- Understanding build reports

### Step 3: Orchestrator
- Coordinating multiple agents
- Running complete workflows
- Combining agent results

### Step 4: REST API
- Using the API endpoints
- Integration examples
- Interactive documentation

## Sample Workspace

The tutorial creates a workspace with intentional issues:

```
learning_workspace/
├── src/
│   ├── main.py      ← TODOs, hardcoded passwords, eval() usage
│   └── utils.py     ← Clean code for comparison
├── tests/
│   └── test_main.py ← Basic tests
└── pyproject.toml   ← Project config
```

### Intentional Issues Included

**Security Issues:**
- Hardcoded password: `password = "admin123"`
- Hardcoded API key: `self.api_key = "sk-1234567890"`
- Unsafe eval: `result = eval(data)`

**Code Quality Issues:**
- Multiple TODO comments
- FIXME markers
- HACK comments
- Missing documentation

**Testing:**
- Basic test structure
- Example test cases

## Usage Examples

### Basic Tutorial Run

```bash
$ python learn.py

🎓 AgentFlow Interactive Learning Tutorial
═══════════════════════════════════════════

Welcome to the AgentFlow Learning Tool!

This interactive tutorial will teach you how to use agentic AI workflows.
You'll learn by running actual agents on a sample codebase.

ℹ  What you'll learn:
  1. How to use the Code Analyzer Agent
  2. How to use the Builder Agent
  3. How to orchestrate multiple agents
  4. How to interpret agent results

▶ Ready to start? Press Enter...
```

### Reset and Repeat

At the end of the tutorial, you can:
1. **Run again** - Resets workspace and restarts
2. **Reset workspace** - Clears and recreates workspace
3. **Clean up** - Removes workspace and exits

### Manual Reset

If you need to reset manually:

```python
from pathlib import Path
from learn import LearningWorkspace

workspace = LearningWorkspace(Path("./learning_workspace"))
workspace.reset()
```

## Command Line Options

```bash
# Run the interactive tutorial
python learn.py

# The script will guide you through each step
# Press Enter to advance through the tutorial
# Ctrl+C to exit (auto-cleanup)
```

## What Gets Created

### During Tutorial

```
./learning_workspace/
├── src/
│   ├── main.py           # Sample code with issues
│   └── utils.py          # Clean utility code
├── tests/
│   └── test_main.py      # Sample tests
├── docs/
│   └── README.md         # Sample documentation
└── pyproject.toml        # Project configuration
```

### After Cleanup

The `learning_workspace` directory is automatically removed when you:
- Complete the tutorial and choose "Clean up and exit"
- Press Ctrl+C during the tutorial
- Encounter an error (auto-cleanup on exception)

## Example Output

### Code Analyzer Results

```
✓ Analysis complete!

📝 TODOs Found (5):
  1. TODO: Implement proper error handling
     File: src/main.py:4
  2. FIXME: This needs refactoring
     File: src/main.py:5
  ...

🔒 Security Issues Found (3):
  1. Hardcoded password
     File: src/main.py:8
  2. Unsafe eval usage
     File: src/main.py:15
  ...

📊 Code Statistics:
  • Python files: 2
  • Total lines: 45
  • Test files: 1

Execution time: 125ms
```

### Builder Results

```
✓ Build complete!

Build Results:
  Linting: ○ SKIPPED
  Testing: ✓ PASSED
  Type Checking: ○ SKIPPED

Summary:
Build Summary:
○ Linting: SKIPPED
✓ Testing: PASSED
○ Type Checking: SKIPPED

Execution time: 2500ms
```

### Orchestrator Results

```
✓ Workflow complete!

Workflow Summary:
──────────────────────────────────────────────────
Code Review Summary:

Code Analysis:
Code Analysis Summary:
- Total Python files: 2
- Total lines of code: 45
- Test files: 1
- TODOs found: 5
- Security issues: 3

Build & Tests:
Build Summary:
✓ Testing: PASSED

✓ Overall: Code review PASSED - Ready for merge
──────────────────────────────────────────────────

Total execution time: 2850ms
```

## Troubleshooting

### "Please run this script from the agentflow directory!"

Make sure you're in the agentflow project directory:

```bash
cd agentflow
python learn.py
```

### Import Errors

Ensure dependencies are installed:

```bash
pip install -e ".[dev]"
```

### Workspace Already Exists

The script will automatically reset the workspace. If you want to manually clean:

```bash
rm -rf learning_workspace
```

### Color Output Not Working

If colors don't display correctly in your terminal:
- Windows: Use Windows Terminal or WSL
- Mac/Linux: Most terminals support ANSI colors
- If issues persist, the script will still work (just without colors)

## Advanced Usage

### Use Workspace for Your Own Testing

```python
from pathlib import Path
from learn import LearningWorkspace

# Create workspace
workspace = LearningWorkspace(Path("./my_test_workspace"))
workspace.create()

# Use with agents
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.base import AgentContext

agent = CodeAnalyzerAgent()
context = AgentContext(
    task_id="my-test",
    workspace_path=str(workspace.workspace_dir)
)

result = await agent.run(context)

# Cleanup when done
workspace.cleanup()
```

### Modify Sample Code

Edit the `_create_sample_files()` method in `learn.py` to customize the sample workspace with different code patterns.

## Educational Benefits

### Hands-On Learning
- **See It In Action**: Watch agents analyze real code
- **Immediate Feedback**: See results instantly
- **Safe Environment**: Sample workspace, no risk to real code

### Progressive Complexity
1. **Simple**: Start with single agent (Code Analyzer)
2. **Medium**: Add build automation (Builder)
3. **Advanced**: Combine with orchestration

### Repeatable
- Reset and try again
- Experiment with different approaches
- Build muscle memory

## Integration with Main Tutorial

This learning script complements the main `demo.py`:

- **demo.py**: Quick demonstration on actual project
- **learn.py**: Interactive, step-by-step learning

Use both for complete understanding!

## Next Steps After Tutorial

1. **Run on Real Code**: Try agents on your own projects
2. **Customize Agents**: Modify agent configurations
3. **Create Workflows**: Build custom orchestration
4. **Extend**: Add new agent types
5. **Integrate**: Use in CI/CD pipelines

## Tips for Best Learning Experience

1. **Read Each Step**: Don't rush through prompts
2. **Examine Sample Code**: Look at the workspace files
3. **Compare Results**: Note what each agent finds
4. **Run Multiple Times**: Repetition builds understanding
5. **Experiment**: Modify the sample code between runs

## Support

- Questions? Check `docs/architecture.md`
- API Reference: `docs/api.md`
- Quick Start: `QUICKSTART.md`
- Issues: Open an issue on GitHub

---

**Happy Learning!** 🚀
