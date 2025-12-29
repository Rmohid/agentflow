"""Tool wrappers for agents to interact with file system, shell, GitHub, etc."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import subprocess
import asyncio


class ToolType(str, Enum):
    """Types of tools available"""
    FILE_SYSTEM = "file_system"
    SHELL = "shell"
    GITHUB = "github"
    WEB_SEARCH = "web_search"
    CODE_ANALYSIS = "code_analysis"


@dataclass
class ToolResult:
    """Result from a tool execution"""
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_ms: int = 0
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class BaseTool(ABC):
    """Base class for all tools"""

    def __init__(self, name: str, tool_type: ToolType):
        self.name = name
        self.tool_type = tool_type

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with given parameters"""
        pass


class FileSystemTool(BaseTool):
    """Tool for file system operations"""

    def __init__(self):
        super().__init__("file_system", ToolType.FILE_SYSTEM)

    async def execute(self, operation: str, **kwargs: Any) -> ToolResult:
        """
        Execute file system operation.
        
        Operations:
        - read: path -> content
        - write: path, content -> success
        - exists: path -> bool
        - list: path -> list of files
        - glob: pattern -> list of matching files
        """
        start = datetime.utcnow()
        
        try:
            if operation == "read":
                result = await self._read_file(kwargs["path"])
            elif operation == "write":
                result = await self._write_file(kwargs["path"], kwargs["content"])
            elif operation == "exists":
                result = await self._exists(kwargs["path"])
            elif operation == "list":
                result = await self._list_dir(kwargs["path"])
            elif operation == "glob":
                result = await self._glob(kwargs["pattern"], kwargs.get("path", "."))
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                output=result,
                execution_time_ms=elapsed
            )
            
        except Exception as e:
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                execution_time_ms=elapsed
            )

    async def _read_file(self, path: str) -> str:
        """Read file contents"""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return file_path.read_text()

    async def _write_file(self, path: str, content: str) -> bool:
        """Write content to file"""
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return True

    async def _exists(self, path: str) -> bool:
        """Check if path exists"""
        return Path(path).exists()

    async def _list_dir(self, path: str) -> List[str]:
        """List directory contents"""
        dir_path = Path(path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        return [str(p.name) for p in dir_path.iterdir()]

    async def _glob(self, pattern: str, path: str = ".") -> List[str]:
        """Find files matching glob pattern"""
        base_path = Path(path)
        return [str(p) for p in base_path.glob(pattern)]


class ShellTool(BaseTool):
    """Tool for executing shell commands"""

    def __init__(self):
        super().__init__("shell", ToolType.SHELL)

    async def execute(self, command: str, **kwargs: Any) -> ToolResult:
        """
        Execute a shell command.
        
        Args:
            command: Shell command to execute
            cwd: Working directory (optional)
            timeout: Timeout in seconds (default: 300)
        """
        start = datetime.utcnow()
        cwd = kwargs.get("cwd")
        timeout = kwargs.get("timeout", 300)
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                raise TimeoutError(f"Command timed out after {timeout}s")
            
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            
            return ToolResult(
                tool_name=self.name,
                success=process.returncode == 0,
                output={
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode(),
                    "returncode": process.returncode
                },
                error=stderr.decode() if process.returncode != 0 else None,
                execution_time_ms=elapsed,
                metadata={"command": command}
            )
            
        except Exception as e:
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                execution_time_ms=elapsed,
                metadata={"command": command}
            )


class GrepTool(BaseTool):
    """Tool for searching file contents"""

    def __init__(self):
        super().__init__("grep", ToolType.CODE_ANALYSIS)

    async def execute(self, pattern: str, **kwargs: Any) -> ToolResult:
        """
        Search for pattern in files.
        
        Args:
            pattern: Search pattern (regex)
            path: Path to search in (default: ".")
            file_pattern: File glob pattern (e.g., "*.py")
            ignore_case: Case insensitive search
        """
        start = datetime.utcnow()
        path = kwargs.get("path", ".")
        file_pattern = kwargs.get("file_pattern", "*")
        ignore_case = kwargs.get("ignore_case", False)
        
        try:
            # Build grep command
            cmd_parts = ["grep", "-r"]
            if ignore_case:
                cmd_parts.append("-i")
            cmd_parts.extend(["-n", pattern, path])
            
            if file_pattern != "*":
                cmd_parts.extend(["--include", file_pattern])
            
            process = await asyncio.create_subprocess_exec(
                *cmd_parts,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Parse grep output
            matches = []
            for line in stdout.decode().split("\n"):
                if line.strip():
                    matches.append(line)
            
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                output={"matches": matches, "count": len(matches)},
                execution_time_ms=elapsed,
                metadata={"pattern": pattern}
            )
            
        except Exception as e:
            elapsed = int((datetime.utcnow() - start).total_seconds() * 1000)
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                execution_time_ms=elapsed
            )


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register default tools"""
        self.register(FileSystemTool())
        self.register(ShellTool())
        self.register(GrepTool())

    def register(self, tool: BaseTool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools"""
        return list(self._tools.keys())

    def get_tools_by_type(self, tool_type: ToolType) -> List[BaseTool]:
        """Get all tools of a specific type"""
        return [
            tool for tool in self._tools.values()
            if tool.tool_type == tool_type
        ]

    async def execute_tool(
        self, 
        tool_name: str, 
        **kwargs: Any
    ) -> ToolResult:
        """Execute a tool by name"""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output=None,
                error=f"Tool not found: {tool_name}"
            )
        
        return await tool.execute(**kwargs)
