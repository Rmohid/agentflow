"""Code Analyzer Agent - Analyzes codebases for patterns, issues, and improvements"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from src.agents.base import BaseAgent, AgentConfig, AgentContext, AgentResult, AgentStatus
from src.core.tools import ToolRegistry
from src.utils.logging import get_logger

logger = get_logger(__name__)


class CodeAnalyzerAgent(BaseAgent):
    """
    Agent that analyzes code for:
    - TODOs and FIXMEs
    - Security issues (hardcoded secrets, SQL injection patterns)
    - Code complexity
    - Dead code
    - Import issues
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="code_analyzer",
                description="Analyzes codebases for patterns, issues, and improvements",
                tags=["analysis", "code-quality"]
            )
        super().__init__(config)
        self.tools = ToolRegistry()
        
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute code analysis on the workspace"""
        logger.info("Starting code analysis", task_id=context.task_id)
        
        result = AgentResult(
            agent_name=self.name,
            status=AgentStatus.RUNNING
        )
        
        try:
            workspace = Path(context.workspace_path)
            if not workspace.exists():
                raise FileNotFoundError(f"Workspace not found: {workspace}")
            
            # Run all analysis checks
            todos = await self._find_todos(workspace)
            security_issues = await self._find_security_issues(workspace)
            code_stats = await self._analyze_code_stats(workspace)
            
            # Compile results
            result.data = {
                "todos": todos,
                "security_issues": security_issues,
                "code_stats": code_stats,
                "summary": self._generate_summary(todos, security_issues, code_stats)
            }
            
            # Add warnings if issues found
            if security_issues:
                result.add_warning(
                    f"Found {len(security_issues)} potential security issues"
                )
            
            if len(todos) > 10:
                result.add_warning(f"Found {len(todos)} TODOs in codebase")
            
            result.status = AgentStatus.SUCCESS
            logger.info(
                "Code analysis completed",
                task_id=context.task_id,
                todos=len(todos),
                security_issues=len(security_issues)
            )
            
        except Exception as e:
            logger.error("Code analysis failed", task_id=context.task_id, error=str(e))
            result.status = AgentStatus.FAILED
            result.add_error(str(e))
        
        return result
    
    async def _find_todos(self, workspace: Path) -> List[Dict[str, Any]]:
        """Find TODO and FIXME comments"""
        todos = []
        
        # Search for TODO patterns
        for pattern in ["TODO", "FIXME", "HACK", "XXX"]:
            grep_result = await self.tools.execute_tool(
                "grep",
                pattern=pattern,
                path=str(workspace),
                file_pattern="*.py",
                ignore_case=True
            )
            
            if grep_result.success and grep_result.output:
                for match in grep_result.output.get("matches", []):
                    # Parse grep output: filename:line:content
                    parts = match.split(":", 2)
                    if len(parts) >= 3:
                        todos.append({
                            "type": pattern,
                            "file": parts[0],
                            "line": parts[1],
                            "content": parts[2].strip()
                        })
        
        return todos
    
    async def _find_security_issues(self, workspace: Path) -> List[Dict[str, Any]]:
        """Find potential security issues"""
        issues = []
        
        # Patterns that might indicate security issues
        security_patterns = [
            ("password\\s*=\\s*['\"]", "Hardcoded password"),
            ("api_key\\s*=\\s*['\"]", "Hardcoded API key"),
            ("secret\\s*=\\s*['\"]", "Hardcoded secret"),
            ("SELECT.*\\+.*FROM", "Potential SQL injection"),
            ("eval\\(", "Unsafe eval usage"),
            ("exec\\(", "Unsafe exec usage"),
        ]
        
        for pattern, description in security_patterns:
            grep_result = await self.tools.execute_tool(
                "grep",
                pattern=pattern,
                path=str(workspace),
                file_pattern="*.py",
                ignore_case=True
            )
            
            if grep_result.success and grep_result.output:
                for match in grep_result.output.get("matches", []):
                    parts = match.split(":", 2)
                    if len(parts) >= 3:
                        issues.append({
                            "type": "security",
                            "description": description,
                            "file": parts[0],
                            "line": parts[1],
                            "content": parts[2].strip()
                        })
        
        return issues
    
    async def _analyze_code_stats(self, workspace: Path) -> Dict[str, Any]:
        """Analyze code statistics"""
        stats = {
            "total_files": 0,
            "total_lines": 0,
            "python_files": 0,
            "test_files": 0,
        }
        
        # Find all Python files
        glob_result = await self.tools.execute_tool(
            "file_system",
            operation="glob",
            pattern="**/*.py",
            path=str(workspace)
        )
        
        if glob_result.success and glob_result.output:
            files = glob_result.output
            stats["python_files"] = len(files)
            stats["total_files"] = len(files)
            
            # Count test files
            stats["test_files"] = sum(1 for f in files if "test_" in f or "_test.py" in f)
            
            # Count total lines
            for file_path in files:
                try:
                    read_result = await self.tools.execute_tool(
                        "file_system",
                        operation="read",
                        path=file_path
                    )
                    if read_result.success:
                        lines = read_result.output.count("\n")
                        stats["total_lines"] += lines
                except Exception:
                    pass
        
        return stats
    
    def _generate_summary(
        self,
        todos: List[Dict[str, Any]],
        security_issues: List[Dict[str, Any]],
        code_stats: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary"""
        summary_parts = [
            f"Code Analysis Summary:",
            f"- Total Python files: {code_stats.get('python_files', 0)}",
            f"- Total lines of code: {code_stats.get('total_lines', 0)}",
            f"- Test files: {code_stats.get('test_files', 0)}",
            f"- TODOs found: {len(todos)}",
            f"- Security issues: {len(security_issues)}",
        ]
        
        if security_issues:
            summary_parts.append("\nSecurity Issues:")
            for issue in security_issues[:5]:  # Top 5
                summary_parts.append(
                    f"  - {issue['description']} in {issue['file']}:{issue['line']}"
                )
        
        return "\n".join(summary_parts)
