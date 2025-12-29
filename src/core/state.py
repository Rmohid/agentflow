"""State management for tracking workflow execution state"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import asyncio


class WorkflowState(BaseModel):
    """Represents the state of a workflow execution"""
    workflow_id: str
    name: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # State data
    data: Dict[str, Any] = Field(default_factory=dict)
    agent_states: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    
    # Execution info
    current_step: Optional[str] = None
    completed_steps: List[str] = Field(default_factory=list)
    failed_steps: List[str] = Field(default_factory=list)
    
    # Metrics
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    
    def update(self, **kwargs: Any) -> None:
        """Update state and refresh timestamp"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()


class StateManager:
    """
    Manages workflow state with persistence to disk.
    Thread-safe for concurrent access.
    """

    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or Path(".agentflow_state")
        self.state_dir.mkdir(exist_ok=True)
        
        self._states: Dict[str, WorkflowState] = {}
        self._lock = asyncio.Lock()
        
        # Load existing states
        self._load_states()

    def _get_state_file(self, workflow_id: str) -> Path:
        """Get the file path for a workflow state"""
        return self.state_dir / f"{workflow_id}.json"

    def _load_states(self) -> None:
        """Load all states from disk"""
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, "r") as f:
                    data = json.load(f)
                    state = WorkflowState(**data)
                    self._states[state.workflow_id] = state
            except Exception as e:
                print(f"Error loading state from {state_file}: {e}")

    async def _save_state(self, workflow_id: str) -> None:
        """Save a state to disk"""
        if workflow_id not in self._states:
            return
            
        state = self._states[workflow_id]
        state_file = self._get_state_file(workflow_id)
        
        try:
            with open(state_file, "w") as f:
                json.dump(state.dict(), f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving state for {workflow_id}: {e}")

    async def create_state(self, workflow_id: str, name: str) -> WorkflowState:
        """Create a new workflow state"""
        async with self._lock:
            if workflow_id in self._states:
                raise ValueError(f"Workflow {workflow_id} already exists")
            
            state = WorkflowState(
                workflow_id=workflow_id,
                name=name,
                status="initialized"
            )
            
            self._states[workflow_id] = state
            await self._save_state(workflow_id)
            
            return state

    async def get_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get a workflow state by ID"""
        return self._states.get(workflow_id)

    async def update_state(
        self, 
        workflow_id: str, 
        **updates: Any
    ) -> Optional[WorkflowState]:
        """Update a workflow state"""
        async with self._lock:
            if workflow_id not in self._states:
                return None
            
            state = self._states[workflow_id]
            state.update(**updates)
            await self._save_state(workflow_id)
            
            return state

    async def set_data(
        self, 
        workflow_id: str, 
        key: str, 
        value: Any
    ) -> None:
        """Set a data value in the workflow state"""
        async with self._lock:
            if workflow_id in self._states:
                self._states[workflow_id].data[key] = value
                self._states[workflow_id].updated_at = datetime.utcnow()
                await self._save_state(workflow_id)

    async def get_data(
        self, 
        workflow_id: str, 
        key: str, 
        default: Any = None
    ) -> Any:
        """Get a data value from the workflow state"""
        state = self._states.get(workflow_id)
        if not state:
            return default
        return state.data.get(key, default)

    async def update_agent_state(
        self,
        workflow_id: str,
        agent_name: str,
        agent_data: Dict[str, Any]
    ) -> None:
        """Update the state for a specific agent"""
        async with self._lock:
            if workflow_id in self._states:
                self._states[workflow_id].agent_states[agent_name] = agent_data
                self._states[workflow_id].updated_at = datetime.utcnow()
                await self._save_state(workflow_id)

    async def get_agent_state(
        self,
        workflow_id: str,
        agent_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get the state for a specific agent"""
        state = self._states.get(workflow_id)
        if not state:
            return None
        return state.agent_states.get(agent_name)

    async def complete_step(self, workflow_id: str, step: str) -> None:
        """Mark a step as completed"""
        async with self._lock:
            if workflow_id in self._states:
                state = self._states[workflow_id]
                if step not in state.completed_steps:
                    state.completed_steps.append(step)
                state.updated_at = datetime.utcnow()
                await self._save_state(workflow_id)

    async def fail_step(self, workflow_id: str, step: str) -> None:
        """Mark a step as failed"""
        async with self._lock:
            if workflow_id in self._states:
                state = self._states[workflow_id]
                if step not in state.failed_steps:
                    state.failed_steps.append(step)
                state.updated_at = datetime.utcnow()
                await self._save_state(workflow_id)

    async def delete_state(self, workflow_id: str) -> bool:
        """Delete a workflow state"""
        async with self._lock:
            if workflow_id not in self._states:
                return False
            
            # Remove from memory
            del self._states[workflow_id]
            
            # Remove from disk
            state_file = self._get_state_file(workflow_id)
            if state_file.exists():
                state_file.unlink()
            
            return True

    async def list_states(self) -> List[WorkflowState]:
        """List all workflow states"""
        return list(self._states.values())

    async def cleanup_old_states(self, days: int = 7) -> int:
        """
        Clean up states older than specified days.
        Returns count of deleted states.
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        deleted = 0
        
        async with self._lock:
            to_delete = [
                wf_id for wf_id, state in self._states.items()
                if state.updated_at < cutoff
                and state.status in ["completed", "failed", "cancelled"]
            ]
            
            for wf_id in to_delete:
                await self.delete_state(wf_id)
                deleted += 1
        
        return deleted
