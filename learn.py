#!/usr/bin/env python3
"""
AgentFlow Learning Tool - Interactive Tutorial
================================================

This script provides an interactive, step-by-step tutorial to learn
how to use agentic AI workflows. Includes:

- Guided walkthrough of each agent
- Interactive prompts and explanations
- Sample workspace for testing
- Reset capability for repeated learning
- Colorful output for better engagement
"""

import asyncio
import shutil
from pathlib import Path
from typing import Optional
import sys

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print a colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")


def print_step(step: int, title: str) -> None:
    """Print a step header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Step {step}: {title}{Colors.END}")
    print(f"{Colors.CYAN}{'─'*70}{Colors.END}")


def print_info(text: str) -> None:
    """Print info text"""
    print(f"{Colors.BLUE}ℹ  {text}{Colors.END}")


def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠  {text}{Colors.END}")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_code(code: str, language: str = "python") -> None:
    """Print code block"""
    print(f"\n{Colors.CYAN}```{language}")
    print(f"{Colors.END}{code}")
    print(f"{Colors.CYAN}```{Colors.END}\n")


def wait_for_user(prompt: str = "Press Enter to continue...") -> None:
    """Wait for user input"""
    input(f"\n{Colors.YELLOW}▶ {prompt}{Colors.END}")


class LearningWorkspace:
    """Manages the learning workspace"""
    
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        
    def create(self) -> None:
        """Create sample workspace for learning"""
        print_info("Creating sample workspace...")
        
        # Create directories
        (self.workspace_dir / "src").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "tests").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "docs").mkdir(parents=True, exist_ok=True)
        
        # Create sample files with intentional issues for learning
        self._create_sample_files()
        
        print_success(f"Sample workspace created at: {self.workspace_dir}")
    
    def _create_sample_files(self) -> None:
        """Create sample files with various issues for agents to find"""
        
        # src/main.py - with TODO and security issue
        (self.workspace_dir / "src" / "main.py").write_text("""
\"\"\"Main application file\"\"\"

# TODO: Implement proper error handling
# FIXME: This needs refactoring

def connect_to_database():
    # Security issue: hardcoded password
    password = "admin123"
    db_host = "localhost"
    return f"Connecting to {db_host} with password {password}"


def process_data(data):
    # TODO: Add input validation
    result = eval(data)  # Security issue: using eval
    return result


class DataProcessor:
    def __init__(self):
        self.api_key = "sk-1234567890"  # Security issue: hardcoded API key
    
    def process(self, items):
        # HACK: Quick fix, needs proper implementation
        return [item.upper() for item in items]


if __name__ == "__main__":
    print("Application started")
    # TODO: Add main logic
""")
        
        # src/utils.py - clean file
        (self.workspace_dir / "src" / "utils.py").write_text("""
\"\"\"Utility functions\"\"\"

def format_output(data: dict) -> str:
    \"\"\"Format data for output\"\"\"
    return str(data)


def validate_input(value: str) -> bool:
    \"\"\"Validate input string\"\"\"
    return len(value) > 0
""")
        
        # tests/test_main.py - basic test
        (self.workspace_dir / "tests" / "test_main.py").write_text("""
\"\"\"Tests for main module\"\"\"

def test_example():
    \"\"\"Example test\"\"\"
    assert True


def test_format():
    \"\"\"Test formatting\"\"\"
    result = "test"
    assert result == "test"
""")
        
        # pyproject.toml
        (self.workspace_dir / "pyproject.toml").write_text("""
[project]
name = "learning-project"
version = "0.1.0"
description = "Sample project for learning AgentFlow"

[tool.pytest.ini_options]
testpaths = ["tests"]
""")
        
        # README.md
        (self.workspace_dir / "docs" / "README.md").write_text("""
# Learning Project

This is a sample project created for learning AgentFlow.

## Features

- TODO: List features
- FIXME: Add more documentation
""")
    
    def reset(self) -> None:
        """Reset the workspace to initial state"""
        print_info("Resetting workspace...")
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
        self.create()
        print_success("Workspace reset complete!")
    
    def cleanup(self) -> None:
        """Remove the workspace"""
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
            print_success("Workspace cleaned up!")


class InteractiveTutorial:
    """Interactive tutorial for learning AgentFlow"""
    
    def __init__(self):
        self.workspace = LearningWorkspace(Path("./learning_workspace"))
    
    async def run(self) -> None:
        """Run the interactive tutorial"""
        print_header("🎓 AgentFlow Interactive Learning Tutorial")
        
        print(f"{Colors.BOLD}Welcome to the AgentFlow Learning Tool!{Colors.END}")
        print("\nThis interactive tutorial will teach you how to use agentic AI workflows.")
        print("You'll learn by running actual agents on a sample codebase.\n")
        
        print_info("What you'll learn:")
        print("  1. How to use the Code Analyzer Agent")
        print("  2. How to use the Builder Agent")
        print("  3. How to orchestrate multiple agents")
        print("  4. How to interpret agent results")
        
        wait_for_user("Ready to start? Press Enter...")
        
        # Setup workspace
        await self._tutorial_setup()
        
        # Tutorial steps
        await self._tutorial_code_analyzer()
        await self._tutorial_builder()
        await self._tutorial_orchestrator()
        await self._tutorial_api()
        
        # Completion
        await self._tutorial_complete()
    
    async def _tutorial_setup(self) -> None:
        """Setup the learning workspace"""
        print_step(0, "Setting Up Learning Environment")
        
        print_info("First, we need to create a sample workspace with code to analyze.")
        print_info("This workspace will contain intentional issues for learning purposes.")
        
        wait_for_user()
        
        self.workspace.create()
        
        print("\n" + f"{Colors.BOLD}Workspace Structure:{Colors.END}")
        print_code("""
learning_workspace/
├── src/
│   ├── main.py      (with TODOs and security issues)
│   └── utils.py     (clean code)
├── tests/
│   └── test_main.py (basic tests)
├── docs/
│   └── README.md
└── pyproject.toml
""", "text")
        
        print_info("This workspace contains several intentional issues:")
        print("  • TODO and FIXME comments")
        print("  • Hardcoded passwords and API keys")
        print("  • Unsafe eval() usage")
        print("  • Missing documentation")
        
        wait_for_user("Workspace ready! Press Enter to continue...")
    
    async def _tutorial_code_analyzer(self) -> None:
        """Tutorial for Code Analyzer Agent"""
        print_step(1, "Using the Code Analyzer Agent")
        
        print_info("The Code Analyzer Agent scans your code for:")
        print("  • TODO, FIXME, HACK comments")
        print("  • Security issues (hardcoded secrets, unsafe patterns)")
        print("  • Code statistics (files, lines, etc.)")
        
        wait_for_user("Let's run the Code Analyzer...")
        
        print("\n" + f"{Colors.BOLD}Running Code Analyzer...{Colors.END}\n")
        
        # Import and run agent
        from src.agents.code_analyzer import CodeAnalyzerAgent
        from src.agents.base import AgentContext
        
        agent = CodeAnalyzerAgent()
        context = AgentContext(
            task_id="tutorial-analyzer",
            workspace_path=str(self.workspace.workspace_dir)
        )
        
        result = await agent.run(context)
        
        # Display results
        if result.is_success():
            print_success("Analysis complete!\n")
            
            # Show TODOs
            todos = result.data.get("todos", [])
            if todos:
                print(f"{Colors.BOLD}📝 TODOs Found ({len(todos)}):{Colors.END}")
                for i, todo in enumerate(todos[:5], 1):
                    print(f"  {i}. {todo['type']}: {todo['content'][:60]}...")
                    print(f"     File: {todo['file']}:{todo['line']}")
            
            # Show security issues
            security = result.data.get("security_issues", [])
            if security:
                print(f"\n{Colors.BOLD}🔒 Security Issues Found ({len(security)}):{Colors.END}")
                for i, issue in enumerate(security[:5], 1):
                    print(f"  {i}. {issue['description']}")
                    print(f"     File: {issue['file']}:{issue['line']}")
            
            # Show stats
            stats = result.data.get("code_stats", {})
            print(f"\n{Colors.BOLD}📊 Code Statistics:{Colors.END}")
            print(f"  • Python files: {stats.get('python_files', 0)}")
            print(f"  • Total lines: {stats.get('total_lines', 0)}")
            print(f"  • Test files: {stats.get('test_files', 0)}")
            
            print(f"\n{Colors.BOLD}Summary:{Colors.END}")
            print(result.data.get("summary", ""))
            
            print(f"\n{Colors.CYAN}Execution time: {result.execution_time_ms}ms{Colors.END}")
        else:
            print_error("Analysis failed!")
            for error in result.errors:
                print_error(error)
        
        print("\n" + f"{Colors.BOLD}💡 Key Takeaway:{Colors.END}")
        print("The Code Analyzer helps you identify issues in your codebase")
        print("automatically, making code reviews faster and more thorough.")
        
        wait_for_user()
    
    async def _tutorial_builder(self) -> None:
        """Tutorial for Builder Agent"""
        print_step(2, "Using the Builder Agent")
        
        print_info("The Builder Agent runs quality checks:")
        print("  • Linting (code style)")
        print("  • Tests (functionality)")
        print("  • Type checking (safety)")
        
        wait_for_user("Let's run the Builder Agent...")
        
        print("\n" + f"{Colors.BOLD}Running Builder Agent...{Colors.END}\n")
        
        # Import and run agent
        from src.agents.builder import BuilderAgent
        from src.agents.base import AgentContext
        
        agent = BuilderAgent()
        context = AgentContext(
            task_id="tutorial-builder",
            workspace_path=str(self.workspace.workspace_dir)
        )
        
        result = await agent.run(context)
        
        # Display results
        if result.is_success():
            print_success("Build complete!\n")
            
            lint_results = result.data.get("linting", {})
            test_results = result.data.get("testing", {})
            type_results = result.data.get("type_checking", {})
            
            print(f"{Colors.BOLD}Build Results:{Colors.END}")
            
            # Linting
            lint_status = "✓ PASSED" if lint_results.get("passed") else "✗ FAILED"
            color = Colors.GREEN if lint_results.get("passed") else Colors.RED
            print(f"  Linting: {color}{lint_status}{Colors.END}")
            
            # Testing
            if test_results.get("skipped"):
                print(f"  Testing: {Colors.YELLOW}○ SKIPPED{Colors.END}")
            else:
                test_status = "✓ PASSED" if test_results.get("passed") else "✗ FAILED"
                color = Colors.GREEN if test_results.get("passed") else Colors.RED
                print(f"  Testing: {color}{test_status}{Colors.END}")
            
            # Type checking
            if type_results.get("skipped"):
                print(f"  Type Checking: {Colors.YELLOW}○ SKIPPED{Colors.END}")
            else:
                type_status = "✓ PASSED" if type_results.get("passed") else "✗ FAILED"
                color = Colors.GREEN if type_results.get("passed") else Colors.RED
                print(f"  Type Checking: {color}{type_status}{Colors.END}")
            
            print(f"\n{Colors.BOLD}Summary:{Colors.END}")
            print(result.data.get("summary", ""))
            
            if result.warnings:
                print(f"\n{Colors.BOLD}Warnings:{Colors.END}")
                for warning in result.warnings:
                    print_warning(warning)
            
            print(f"\n{Colors.CYAN}Execution time: {result.execution_time_ms}ms{Colors.END}")
        else:
            print_error("Build failed!")
            for error in result.errors:
                print_error(error)
        
        print("\n" + f"{Colors.BOLD}💡 Key Takeaway:{Colors.END}")
        print("The Builder Agent automates quality checks, ensuring your")
        print("code meets standards before it goes to production.")
        
        wait_for_user()
    
    async def _tutorial_orchestrator(self) -> None:
        """Tutorial for Orchestrator Agent"""
        print_step(3, "Orchestrating Multiple Agents")
        
        print_info("The Orchestrator coordinates multiple agents to complete")
        print_info("complex workflows. It runs agents in sequence or parallel.")
        
        wait_for_user("Let's run a complete code review workflow...")
        
        print("\n" + f"{Colors.BOLD}Running Code Review Workflow...{Colors.END}")
        print_info("This will run both Code Analyzer AND Builder agents\n")
        
        # Import and run orchestrator
        from src.agents.orchestrator import OrchestratorAgent
        from src.agents.code_analyzer import CodeAnalyzerAgent
        from src.agents.builder import BuilderAgent
        from src.agents.base import AgentContext
        
        orchestrator = OrchestratorAgent()
        orchestrator.register_agent(CodeAnalyzerAgent())
        orchestrator.register_agent(BuilderAgent())
        
        context = AgentContext(
            task_id="tutorial-orchestrator",
            workspace_path=str(self.workspace.workspace_dir),
            config={"workflow_type": "code_review"}
        )
        
        result = await orchestrator.run(context)
        
        # Display results
        if result.is_success():
            print_success("Workflow complete!\n")
            
            print(f"{Colors.BOLD}Workflow Summary:{Colors.END}")
            print("─" * 70)
            print(result.data.get("summary", "No summary available"))
            print("─" * 70)
            
            print(f"\n{Colors.CYAN}Total execution time: {result.execution_time_ms}ms{Colors.END}")
            
            # Show agent results
            agent_results = result.data.get("agent_results", {})
            if agent_results:
                print(f"\n{Colors.BOLD}Individual Agent Results:{Colors.END}")
                for agent_name, agent_data in agent_results.items():
                    status = agent_data.get("status", "unknown")
                    color = Colors.GREEN if status == "success" else Colors.RED
                    print(f"  • {agent_name}: {color}{status.upper()}{Colors.END}")
        else:
            print_error("Workflow failed!")
            for error in result.errors:
                print_error(error)
        
        print("\n" + f"{Colors.BOLD}💡 Key Takeaway:{Colors.END}")
        print("The Orchestrator lets you combine multiple agents into powerful")
        print("workflows, automating complex multi-step processes.")
        
        wait_for_user()
    
    async def _tutorial_api(self) -> None:
        """Tutorial for API usage"""
        print_step(4, "Using the REST API")
        
        print_info("AgentFlow also provides a REST API for integration.")
        print_info("You can start the API server and call it from any language.")
        
        print("\n" + f"{Colors.BOLD}Example API Usage:{Colors.END}")
        
        print_code("""
# Start the API server
uvicorn src.api.main:app --reload

# Then in another terminal or from any HTTP client:
curl -X POST http://localhost:8000/api/v1/analysis/code \\
  -H "Content-Type: application/json" \\
  -d '{"workspace_path": "./learning_workspace"}'
""", "bash")
        
        print_code("""
# Python example
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/workflows/execute",
    json={
        "workflow_type": "code_review",
        "workspace_path": "./learning_workspace"
    }
)

result = response.json()
print(result["data"]["summary"])
""", "python")
        
        print_info("Visit http://localhost:8000/docs for interactive API documentation")
        
        wait_for_user()
    
    async def _tutorial_complete(self) -> None:
        """Tutorial completion"""
        print_header("🎉 Tutorial Complete!")
        
        print(f"{Colors.GREEN}{Colors.BOLD}Congratulations!{Colors.END}")
        print("You've learned how to use AgentFlow's agentic AI workflows!\n")
        
        print(f"{Colors.BOLD}What you learned:{Colors.END}")
        print("  ✓ How to use the Code Analyzer Agent")
        print("  ✓ How to use the Builder Agent")
        print("  ✓ How to orchestrate multiple agents")
        print("  ✓ How to use the REST API")
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
        print("  1. Try running agents on your own codebase")
        print("  2. Customize agent configurations")
        print("  3. Create your own custom agents")
        print("  4. Build custom workflows")
        print("  5. Integrate with CI/CD pipelines")
        
        print(f"\n{Colors.BOLD}Resources:{Colors.END}")
        print("  • Documentation: docs/architecture.md")
        print("  • API Reference: docs/api.md")
        print("  • Quick Start: QUICKSTART.md")
        print("  • Source Code: src/agents/")
        
        print("\n" + f"{Colors.YELLOW}Would you like to:{Colors.END}")
        print("  1. Run the tutorial again")
        print("  2. Reset the workspace")
        print("  3. Clean up and exit")
        
        choice = input(f"\n{Colors.YELLOW}Enter choice (1/2/3): {Colors.END}").strip()
        
        if choice == "1":
            self.workspace.reset()
            await self.run()
        elif choice == "2":
            self.workspace.reset()
            print_success("Workspace reset! You can run the tutorial again anytime.")
        else:
            self.workspace.cleanup()
            print_success("Thanks for learning with AgentFlow! 🚀")


async def main():
    """Main entry point"""
    try:
        tutorial = InteractiveTutorial()
        await tutorial.run()
    except KeyboardInterrupt:
        print("\n\n" + f"{Colors.YELLOW}Tutorial interrupted by user.{Colors.END}")
        print_info("Cleaning up...")
        workspace = LearningWorkspace(Path("./learning_workspace"))
        workspace.cleanup()
    except Exception as e:
        print_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check if running from correct directory
    if not Path("src/agents/base.py").exists():
        print_error("Please run this script from the agentflow directory!")
        print_info("Usage: cd agentflow && python learn.py")
        sys.exit(1)
    
    asyncio.run(main())
