"""
Phase management for Specification-Driven Development (SDD).

This module implements the four-phase SDD workflow:
1. SPECIFY - Define what to build
2. PLAN - Define how to build it
3. TASKS - Break down into actionable work
4. IMPLEMENT - Execute the tasks
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from pydantic import BaseModel, Field


class Phase(str, Enum):
    """SDD workflow phases."""
    SPECIFY = "specify"
    PLAN = "plan"
    TASKS = "tasks"
    IMPLEMENT = "implement"


class PhaseStatus(str, Enum):
    """Status of a phase."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Phase ordering for transitions
PHASE_ORDER = [Phase.SPECIFY, Phase.PLAN, Phase.TASKS, Phase.IMPLEMENT]


class PhaseResult(BaseModel):
    """Result and state of a single phase."""
    phase: Phase
    status: PhaseStatus = PhaseStatus.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    validation_errors: List[str] = Field(default_factory=list)
    
    def start(self) -> None:
        """Mark phase as started."""
        self.status = PhaseStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
    
    def complete(self, artifacts: Optional[Dict[str, Any]] = None) -> None:
        """Mark phase as completed."""
        self.status = PhaseStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if artifacts:
            self.artifacts.update(artifacts)
    
    def fail(self, errors: List[str]) -> None:
        """Mark phase as failed."""
        self.status = PhaseStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.validation_errors = errors


class ProjectState(BaseModel):
    """Complete state of an SDD project."""
    project_id: str
    project_name: str = ""
    current_phase: Phase = Phase.SPECIFY
    phases: Dict[str, PhaseResult] = Field(default_factory=dict)
    specification: Optional[Dict[str, Any]] = None
    plan: Optional[Dict[str, Any]] = None
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize phase results if not present."""
        for phase in Phase:
            if phase.value not in self.phases:
                self.phases[phase.value] = PhaseResult(phase=phase)
    
    def get_phase_result(self, phase: Phase) -> PhaseResult:
        """Get result for a specific phase."""
        return self.phases.get(phase.value, PhaseResult(phase=phase))
    
    def update_phase(self, phase: Phase, result: PhaseResult) -> None:
        """Update a phase result."""
        self.phases[phase.value] = result
        self.updated_at = datetime.utcnow()


class PhaseValidationError(Exception):
    """Raised when phase validation fails."""
    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors


class PhaseManager:
    """
    Manages SDD phase transitions and validation.
    
    Ensures phases are completed in order and validates
    gate conditions before allowing transitions.
    """
    
    def __init__(self, state_dir: str = ".agentflow_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
    
    def _state_file(self, project_id: str) -> Path:
        """Get state file path for a project."""
        return self.state_dir / f"{project_id}_sdd_state.json"
    
    def create_project(self, project_id: str, project_name: str = "") -> ProjectState:
        """Create a new SDD project."""
        state = ProjectState(
            project_id=project_id,
            project_name=project_name or project_id
        )
        # Start the first phase
        specify_result = state.get_phase_result(Phase.SPECIFY)
        specify_result.start()
        state.update_phase(Phase.SPECIFY, specify_result)
        
        self.save_state(state)
        return state
    
    def load_state(self, project_id: str) -> Optional[ProjectState]:
        """Load project state from disk."""
        state_file = self._state_file(project_id)
        if not state_file.exists():
            return None
        
        with open(state_file, "r") as f:
            data = json.load(f)
        
        # Reconstruct PhaseResult objects
        if "phases" in data:
            for phase_key, phase_data in data["phases"].items():
                data["phases"][phase_key] = PhaseResult(**phase_data)
        
        return ProjectState(**data)
    
    def save_state(self, state: ProjectState) -> None:
        """Save project state to disk."""
        state_file = self._state_file(state.project_id)
        
        # Convert to dict with proper serialization
        data = state.model_dump(mode="json")
        
        with open(state_file, "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def get_or_create_project(self, project_id: str, project_name: str = "") -> ProjectState:
        """Get existing project or create new one."""
        state = self.load_state(project_id)
        if state is None:
            state = self.create_project(project_id, project_name)
        return state
    
    def validate_phase_gate(self, state: ProjectState, target_phase: Phase) -> List[str]:
        """
        Validate gate conditions for transitioning to target phase.
        
        Returns list of validation errors (empty if valid).
        """
        errors = []
        current_idx = PHASE_ORDER.index(state.current_phase)
        target_idx = PHASE_ORDER.index(target_phase)
        
        # Can always go back or stay at current phase
        if target_idx <= current_idx:
            return errors
        
        # Check all phases before target are completed
        for i in range(target_idx):
            phase = PHASE_ORDER[i]
            result = state.get_phase_result(phase)
            if result.status != PhaseStatus.COMPLETED:
                errors.append(f"Phase '{phase.value}' must be completed before '{target_phase.value}'")
        
        # Phase-specific validations
        if target_phase == Phase.PLAN:
            if not state.specification:
                errors.append("Specification document required before planning")
        
        elif target_phase == Phase.TASKS:
            if not state.plan:
                errors.append("Plan document required before task breakdown")
        
        elif target_phase == Phase.IMPLEMENT:
            if not state.tasks:
                errors.append("Task breakdown required before implementation")
        
        return errors
    
    def transition_to_phase(
        self, 
        state: ProjectState, 
        target_phase: Phase,
        force: bool = False
    ) -> ProjectState:
        """
        Transition project to a new phase.
        
        Args:
            state: Current project state
            target_phase: Phase to transition to
            force: If True, skip validation (for demos/learning)
        
        Returns:
            Updated project state
            
        Raises:
            PhaseValidationError: If gate validation fails and force=False
        """
        if not force:
            errors = self.validate_phase_gate(state, target_phase)
            if errors:
                raise PhaseValidationError(
                    f"Cannot transition to '{target_phase.value}'",
                    errors
                )
        
        # Complete current phase if moving forward
        current_idx = PHASE_ORDER.index(state.current_phase)
        target_idx = PHASE_ORDER.index(target_phase)
        
        if target_idx > current_idx:
            current_result = state.get_phase_result(state.current_phase)
            if current_result.status == PhaseStatus.IN_PROGRESS:
                current_result.complete()
                state.update_phase(state.current_phase, current_result)
        
        # Start new phase
        state.current_phase = target_phase
        target_result = state.get_phase_result(target_phase)
        target_result.start()
        state.update_phase(target_phase, target_result)
        
        self.save_state(state)
        return state
    
    def complete_phase(
        self,
        state: ProjectState,
        phase: Phase,
        artifacts: Optional[Dict[str, Any]] = None
    ) -> ProjectState:
        """
        Mark a phase as completed with optional artifacts.
        
        Args:
            state: Current project state
            phase: Phase to complete
            artifacts: Output artifacts from this phase
            
        Returns:
            Updated project state
        """
        result = state.get_phase_result(phase)
        result.complete(artifacts)
        state.update_phase(phase, result)
        
        # Store phase-specific data
        if phase == Phase.SPECIFY and artifacts:
            state.specification = artifacts.get("specification", artifacts)
        elif phase == Phase.PLAN and artifacts:
            state.plan = artifacts.get("plan", artifacts)
        elif phase == Phase.TASKS and artifacts:
            state.tasks = artifacts.get("tasks", [])
        
        self.save_state(state)
        return state
    
    def get_phase_summary(self, state: ProjectState) -> Dict[str, Any]:
        """Get a summary of all phases and their status."""
        summary = {
            "project_id": state.project_id,
            "project_name": state.project_name,
            "current_phase": state.current_phase.value,
            "phases": {}
        }
        
        for phase in PHASE_ORDER:
            result = state.get_phase_result(phase)
            summary["phases"][phase.value] = {
                "status": result.status.value,
                "started_at": result.started_at.isoformat() if result.started_at else None,
                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                "has_artifacts": bool(result.artifacts),
                "errors": result.validation_errors
            }
        
        return summary
