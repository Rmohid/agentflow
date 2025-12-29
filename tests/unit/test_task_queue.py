"""Tests for task queue"""

import pytest
from src.core.task_queue import Task, TaskQueue, TaskStatus, TaskPriority


@pytest.mark.asyncio
async def test_add_task():
    """Test adding a task to the queue"""
    queue = TaskQueue()
    
    task = Task(
        name="test_task",
        agent_name="test_agent",
        priority=TaskPriority.NORMAL
    )
    
    task_id = await queue.add_task(task)
    
    assert task_id == task.id
    retrieved = await queue.get_task(task_id)
    assert retrieved is not None
    assert retrieved.status == TaskStatus.QUEUED


@pytest.mark.asyncio
async def test_get_next_task_priority():
    """Test that tasks are retrieved by priority"""
    queue = TaskQueue()
    
    # Add tasks with different priorities
    normal_task = Task(
        name="normal",
        agent_name="agent",
        priority=TaskPriority.NORMAL
    )
    high_task = Task(
        name="high",
        agent_name="agent",
        priority=TaskPriority.HIGH
    )
    
    await queue.add_task(normal_task)
    await queue.add_task(high_task)
    
    # Should get high priority task first
    next_task = await queue.get_next_task()
    assert next_task is not None
    assert next_task.priority == TaskPriority.HIGH


@pytest.mark.asyncio
async def test_task_dependencies():
    """Test task dependency handling"""
    queue = TaskQueue()
    
    # Create tasks with dependencies
    task1 = Task(name="task1", agent_name="agent")
    task2 = Task(
        name="task2",
        agent_name="agent",
        depends_on=[task1.id]
    )
    
    await queue.add_task(task1)
    await queue.add_task(task2)
    
    # task2 should not be ready until task1 is completed
    assert not task2.is_ready(set())
    assert task2.is_ready({task1.id})


@pytest.mark.asyncio
async def test_mark_task_completed():
    """Test marking a task as completed"""
    queue = TaskQueue()
    
    task = Task(name="test", agent_name="agent")
    task_id = await queue.add_task(task)
    
    await queue.mark_task_started(task_id)
    await queue.mark_task_completed(task_id, {"result": "success"})
    
    completed_task = await queue.get_task(task_id)
    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.output_data["result"] == "success"


@pytest.mark.asyncio
async def test_get_queue_stats():
    """Test getting queue statistics"""
    queue = TaskQueue()
    
    task1 = Task(name="task1", agent_name="agent")
    task2 = Task(name="task2", agent_name="agent")
    
    await queue.add_task(task1)
    await queue.add_task(task2)
    
    stats = await queue.get_stats()
    
    assert stats["total_tasks"] == 2
    assert stats["status_breakdown"][TaskStatus.QUEUED.value] == 2
