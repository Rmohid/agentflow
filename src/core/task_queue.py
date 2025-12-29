"""Task queue management for coordinating agent work"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from uuid import uuid4
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(int, Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class Task(BaseModel):
    """Represents a task to be executed by an agent"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    agent_name: str
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Task data
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    
    # Dependencies and retry
    depends_on: List[str] = Field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

    def is_ready(self, completed_tasks: set[str]) -> bool:
        """Check if all dependencies are completed"""
        return all(dep_id in completed_tasks for dep_id in self.depends_on)

    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries

    def mark_started(self) -> None:
        """Mark task as started"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()

    def mark_completed(self, output_data: Dict[str, Any]) -> None:
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.output_data = output_data

    def mark_failed(self, error: str) -> None:
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error
        self.retry_count += 1


class TaskQueue:
    """
    Task queue for managing and executing tasks in priority order.
    Handles task dependencies and retry logic.
    """

    def __init__(self, max_concurrent_tasks: int = 5):
        self.max_concurrent_tasks = max_concurrent_tasks
        self._tasks: Dict[str, Task] = {}
        self._running_tasks: set[str] = set()
        self._completed_tasks: set[str] = set()
        self._lock = asyncio.Lock()

    async def add_task(self, task: Task) -> str:
        """
        Add a task to the queue.
        
        Args:
            task: Task to add
            
        Returns:
            Task ID
        """
        async with self._lock:
            if task.id in self._tasks:
                raise ValueError(f"Task {task.id} already exists")
            
            task.status = TaskStatus.QUEUED
            self._tasks[task.id] = task
            
        return task.id

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self._tasks.get(task_id)

    async def get_next_task(self) -> Optional[Task]:
        """
        Get the next task ready to execute based on:
        1. Dependencies are met
        2. Priority (highest first)
        3. Creation time (oldest first)
        """
        async with self._lock:
            # Filter ready tasks
            ready_tasks = [
                task for task in self._tasks.values()
                if task.status == TaskStatus.QUEUED
                and task.is_ready(self._completed_tasks)
            ]
            
            if not ready_tasks:
                return None
            
            # Sort by priority (desc) then creation time (asc)
            ready_tasks.sort(
                key=lambda t: (-t.priority.value, t.created_at)
            )
            
            return ready_tasks[0]

    async def mark_task_started(self, task_id: str) -> None:
        """Mark a task as started"""
        async with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].mark_started()
                self._running_tasks.add(task_id)

    async def mark_task_completed(
        self, 
        task_id: str, 
        output_data: Dict[str, Any]
    ) -> None:
        """Mark a task as completed"""
        async with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].mark_completed(output_data)
                self._running_tasks.discard(task_id)
                self._completed_tasks.add(task_id)

    async def mark_task_failed(self, task_id: str, error: str) -> None:
        """Mark a task as failed and potentially retry"""
        async with self._lock:
            if task_id not in self._tasks:
                return
                
            task = self._tasks[task_id]
            task.mark_failed(error)
            self._running_tasks.discard(task_id)
            
            # Retry if possible
            if task.can_retry():
                task.status = TaskStatus.QUEUED
            else:
                task.status = TaskStatus.FAILED

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        async with self._lock:
            if task_id not in self._tasks:
                return False
                
            task = self._tasks[task_id]
            if task.status in [TaskStatus.PENDING, TaskStatus.QUEUED]:
                task.status = TaskStatus.CANCELLED
                return True
                
        return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        async with self._lock:
            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = sum(
                    1 for t in self._tasks.values() if t.status == status
                )
            
            return {
                "total_tasks": len(self._tasks),
                "running_tasks": len(self._running_tasks),
                "completed_tasks": len(self._completed_tasks),
                "status_breakdown": status_counts,
                "max_concurrent": self.max_concurrent_tasks,
            }

    async def clear_completed(self) -> int:
        """Clear completed tasks and return count cleared"""
        async with self._lock:
            completed_ids = [
                task_id for task_id, task in self._tasks.items()
                if task.status == TaskStatus.COMPLETED
            ]
            
            for task_id in completed_ids:
                del self._tasks[task_id]
                
        return len(completed_ids)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self._tasks.values())
