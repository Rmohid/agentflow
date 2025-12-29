"""Base agent class and core types for all agents"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    name: str
    description: str
    max_retries: int = Field(default=3, ge=0)
    timeout_seconds: int = Field(default=300, ge=1)
    enabled: bool = True
    log_level: str = "INFO"
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    """Result from an agent execution"""
    agent_name: str
    status: AgentStatus
    data: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    execution_time_ms: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def is_success(self) -> bool:
        """Check if execution was successful"""
        return self.status == AgentStatus.SUCCESS

    def is_failed(self) -> bool:
        """Check if execution failed"""
        return self.status == AgentStatus.FAILED

    def add_error(self, error: str) -> None:
        """Add an error message"""
        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        """Add a warning message"""
        self.warnings.append(warning)


@dataclass
class AgentContext:
    """Context passed to agents during execution"""
    task_id: str
    workspace_path: str
    config: Dict[str, Any] = field(default_factory=dict)
    shared_data: Dict[str, Any] = field(default_factory=dict)
    parent_agent: Optional[str] = None


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    
    All agents should inherit from this class and implement
    the execute() method with their specific logic.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self._execution_count = 0
        self._last_result: Optional[AgentResult] = None

    @property
    def name(self) -> str:
        """Get agent name"""
        return self.config.name

    @property
    def is_enabled(self) -> bool:
        """Check if agent is enabled"""
        return self.config.enabled

    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResult:
        """
        Execute the agent's main logic.
        
        Args:
            context: Execution context with task info and shared data
            
        Returns:
            AgentResult with execution status and data
        """
        pass

    async def run(self, context: AgentContext) -> AgentResult:
        """
        Run the agent with retry logic and error handling.
        
        Args:
            context: Execution context
            
        Returns:
            AgentResult with execution outcome
        """
        if not self.is_enabled:
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.CANCELLED,
                errors=["Agent is disabled"],
            )

        start_time = datetime.utcnow()
        self.status = AgentStatus.RUNNING
        
        retries = 0
        last_error = None

        while retries <= self.config.max_retries:
            try:
                result = await self.execute(context)
                
                # Calculate execution time
                end_time = datetime.utcnow()
                result.execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
                
                self.status = result.status
                self._execution_count += 1
                self._last_result = result
                
                return result

            except Exception as e:
                last_error = str(e)
                retries += 1
                
                if retries > self.config.max_retries:
                    break
                
                # Wait before retry (exponential backoff)
                import asyncio
                await asyncio.sleep(2 ** retries)

        # All retries failed
        end_time = datetime.utcnow()
        failed_result = AgentResult(
            agent_name=self.name,
            status=AgentStatus.FAILED,
            errors=[f"Failed after {self.config.max_retries} retries: {last_error}"],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )
        
        self.status = AgentStatus.FAILED
        self._last_result = failed_result
        
        return failed_result

    async def validate_context(self, context: AgentContext) -> List[str]:
        """
        Validate the execution context.
        
        Args:
            context: Context to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not context.task_id:
            errors.append("Task ID is required")
            
        if not context.workspace_path:
            errors.append("Workspace path is required")
            
        return errors

    def get_stats(self) -> Dict[str, Any]:
        """Get agent execution statistics"""
        return {
            "name": self.name,
            "status": self.status.value,
            "execution_count": self._execution_count,
            "last_result": self._last_result.dict() if self._last_result else None,
            "enabled": self.is_enabled,
        }

    def reset(self) -> None:
        """Reset agent state"""
        self.status = AgentStatus.IDLE
        self._execution_count = 0
        self._last_result = None
