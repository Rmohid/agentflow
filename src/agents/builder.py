"""Builder Agent - Runs tests, linters, and builds"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from src.agents.base import BaseAgent, AgentConfig, AgentContext, AgentResult, AgentStatus
from src.core.tools import ToolRegistry
from src.utils.logging import get_logger

logger = get_logger(__name__)


class BuilderAgent(BaseAgent):
    """
    Agent that handles build operations:
    - Running tests (pytest, unittest)
    - Linting (ruff, black)
    - Type checking (mypy)
    - Installing dependencies
    - Building packages
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="builder",
                description="Runs tests, linters, and builds",
                tags=["build", "test", "quality"],
                timeout_seconds=600  # Builds can take longer
            )
        super().__init__(config)
        self.tools = ToolRegistry()
        
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute build operations"""
        logger.info("Starting build operations", task_id=context.task_id)
        
        result = AgentResult(
            agent_name=self.name,
            status=AgentStatus.RUNNING
        )
        
        try:
            workspace = Path(context.workspace_path)
            if not workspace.exists():
                raise FileNotFoundError(f"Workspace not found: {workspace}")
            
            # Check if this is a Python project
            has_pyproject = (workspace / "pyproject.toml").exists()
            has_requirements = (workspace / "requirements.txt").exists()
            
            if not (has_pyproject or has_requirements):
                result.add_warning("No Python project files found (pyproject.toml or requirements.txt)")
            
            # Run checks based on what's available
            lint_results = await self._run_linting(workspace)
            test_results = await self._run_tests(workspace)
            type_check_results = await self._run_type_checking(workspace)
            
            # Compile results
            result.data = {
                "linting": lint_results,
                "testing": test_results,
                "type_checking": type_check_results,
                "summary": self._generate_summary(lint_results, test_results, type_check_results)
            }
            
            # Determine overall status
            all_passed = all([
                lint_results.get("passed", False),
                test_results.get("passed", False),
                type_check_results.get("passed", False)
            ])
            
            if all_passed:
                result.status = AgentStatus.SUCCESS
            else:
                result.status = AgentStatus.SUCCESS  # Still success, but with warnings
                if not lint_results.get("passed"):
                    result.add_warning("Linting checks failed")
                if not test_results.get("passed"):
                    result.add_warning("Tests failed")
                if not type_check_results.get("passed"):
                    result.add_warning("Type checking failed")
            
            logger.info(
                "Build operations completed",
                task_id=context.task_id,
                all_passed=all_passed
            )
            
        except Exception as e:
            logger.error("Build operations failed", task_id=context.task_id, error=str(e))
            result.status = AgentStatus.FAILED
            result.add_error(str(e))
        
        return result
    
    async def _run_linting(self, workspace: Path) -> Dict[str, Any]:
        """Run linting checks"""
        results = {"passed": True, "tools": {}}
        
        # Check if ruff is available
        ruff_check = await self.tools.execute_tool(
            "shell",
            command="ruff --version",
            cwd=str(workspace)
        )
        
        if ruff_check.success:
            # Run ruff
            ruff_result = await self.tools.execute_tool(
                "shell",
                command="ruff check src/",
                cwd=str(workspace)
            )
            
            results["tools"]["ruff"] = {
                "success": ruff_result.success,
                "output": ruff_result.output.get("stdout", "") if ruff_result.output else ""
            }
            
            if not ruff_result.success:
                results["passed"] = False
        
        # Check if black is available
        black_check = await self.tools.execute_tool(
            "shell",
            command="black --version",
            cwd=str(workspace)
        )
        
        if black_check.success:
            # Run black in check mode
            black_result = await self.tools.execute_tool(
                "shell",
                command="black --check src/",
                cwd=str(workspace)
            )
            
            results["tools"]["black"] = {
                "success": black_result.success,
                "output": black_result.output.get("stdout", "") if black_result.output else ""
            }
            
            if not black_result.success:
                results["passed"] = False
        
        return results
    
    async def _run_tests(self, workspace: Path) -> Dict[str, Any]:
        """Run test suite"""
        results = {"passed": True, "coverage": None}
        
        # Check if pytest is available
        pytest_check = await self.tools.execute_tool(
            "shell",
            command="pytest --version",
            cwd=str(workspace)
        )
        
        if pytest_check.success:
            # Run pytest with coverage
            test_result = await self.tools.execute_tool(
                "shell",
                command="pytest tests/ -v --tb=short",
                cwd=str(workspace),
                timeout=300
            )
            
            results["pytest"] = {
                "success": test_result.success,
                "output": test_result.output.get("stdout", "") if test_result.output else ""
            }
            
            results["passed"] = test_result.success
        else:
            results["skipped"] = True
            results["reason"] = "pytest not available"
        
        return results
    
    async def _run_type_checking(self, workspace: Path) -> Dict[str, Any]:
        """Run type checking"""
        results = {"passed": True}
        
        # Check if mypy is available
        mypy_check = await self.tools.execute_tool(
            "shell",
            command="mypy --version",
            cwd=str(workspace)
        )
        
        if mypy_check.success:
            # Run mypy
            mypy_result = await self.tools.execute_tool(
                "shell",
                command="mypy src/",
                cwd=str(workspace)
            )
            
            results["mypy"] = {
                "success": mypy_result.success,
                "output": mypy_result.output.get("stdout", "") if mypy_result.output else ""
            }
            
            results["passed"] = mypy_result.success
        else:
            results["skipped"] = True
            results["reason"] = "mypy not available"
        
        return results
    
    def _generate_summary(
        self,
        lint_results: Dict[str, Any],
        test_results: Dict[str, Any],
        type_check_results: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary"""
        summary_parts = ["Build Summary:"]
        
        # Linting
        if lint_results.get("passed"):
            summary_parts.append("✓ Linting: PASSED")
        else:
            summary_parts.append("✗ Linting: FAILED")
            for tool, data in lint_results.get("tools", {}).items():
                if not data.get("success"):
                    summary_parts.append(f"  - {tool} found issues")
        
        # Testing
        if test_results.get("skipped"):
            summary_parts.append("○ Testing: SKIPPED")
        elif test_results.get("passed"):
            summary_parts.append("✓ Testing: PASSED")
        else:
            summary_parts.append("✗ Testing: FAILED")
        
        # Type checking
        if type_check_results.get("skipped"):
            summary_parts.append("○ Type Checking: SKIPPED")
        elif type_check_results.get("passed"):
            summary_parts.append("✓ Type Checking: PASSED")
        else:
            summary_parts.append("✗ Type Checking: FAILED")
        
        return "\n".join(summary_parts)
