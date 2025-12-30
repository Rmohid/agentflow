"""Core module initialization"""

from src.core.task_queue import Task, TaskQueue, TaskStatus
from src.core.state import StateManager
from src.core.tools import ToolRegistry, ToolResult
from src.core.phases import (
    Phase,
    PhaseStatus,
    PhaseResult,
    ProjectState,
    PhaseManager,
    PhaseValidationError,
    PHASE_ORDER,
)

__all__ = [
    "Task",
    "TaskQueue", 
    "TaskStatus",
    "StateManager",
    "ToolRegistry",
    "ToolResult",
    # SDD Phase management
    "Phase",
    "PhaseStatus",
    "PhaseResult",
    "ProjectState",
    "PhaseManager",
    "PhaseValidationError",
    "PHASE_ORDER",
]
