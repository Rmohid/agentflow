"""
Phase management API routes for SDD workflow.

Provides endpoints for managing the four-phase SDD workflow:
- Specify: Define requirements
- Plan: Architecture decisions
- Tasks: Work breakdown
- Implement: Execute tasks
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.core.phases import (
    Phase,
    PhaseManager,
    PhaseValidationError,
    PHASE_ORDER,
)


router = APIRouter(prefix="/api/v1", tags=["phases"])

# Global phase manager instance
_phase_manager: Optional[PhaseManager] = None


def get_phase_manager() -> PhaseManager:
    """Get or create the phase manager instance."""
    global _phase_manager
    if _phase_manager is None:
        _phase_manager = PhaseManager()
    return _phase_manager


# Request/Response models

class CreateProjectRequest(BaseModel):
    """Request to create a new SDD project."""
    project_id: str
    project_name: str = ""


class PhaseTransitionRequest(BaseModel):
    """Request to transition to a phase."""
    project_id: str
    force: bool = Field(default=False, description="Skip validation gates")


class CompletePhaseRequest(BaseModel):
    """Request to complete a phase with artifacts."""
    project_id: str
    artifacts: Dict[str, Any] = Field(default_factory=dict)


class SpecifyRequest(BaseModel):
    """Request to start/update specification phase."""
    project_id: str
    specification: Dict[str, Any] = Field(
        default_factory=dict,
        description="Specification content"
    )
    force: bool = False


class PlanRequest(BaseModel):
    """Request to generate/update plan."""
    project_id: str
    plan: Dict[str, Any] = Field(
        default_factory=dict,
        description="Plan content"
    )
    force: bool = False


class TasksRequest(BaseModel):
    """Request to generate/update task breakdown."""
    project_id: str
    tasks: list = Field(
        default_factory=list,
        description="Task list"
    )
    force: bool = False


class ImplementRequest(BaseModel):
    """Request to start implementation."""
    project_id: str
    force: bool = False


class ProjectResponse(BaseModel):
    """Response with project state."""
    success: bool
    project_id: str
    current_phase: str
    phases: Dict[str, Any]
    message: str = ""


class ErrorResponse(BaseModel):
    """Error response."""
    success: bool = False
    error: str
    details: list = Field(default_factory=list)


# Endpoints

@router.post("/project/create", response_model=ProjectResponse)
async def create_project(request: CreateProjectRequest) -> ProjectResponse:
    """Create a new SDD project."""
    manager = get_phase_manager()
    
    # Check if project already exists
    existing = manager.load_state(request.project_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Project '{request.project_id}' already exists"
        )
    
    state = manager.create_project(request.project_id, request.project_name)
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message=f"Project '{state.project_name}' created in SPECIFY phase"
    )


@router.get("/project/{project_id}/status", response_model=ProjectResponse)
async def get_project_status(project_id: str) -> ProjectResponse:
    """Get current project phase status."""
    manager = get_phase_manager()
    state = manager.load_state(project_id)
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{project_id}' not found"
        )
    
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message=f"Project is in {state.current_phase.value.upper()} phase"
    )


@router.post("/phases/specify", response_model=ProjectResponse)
async def specify_phase(request: SpecifyRequest) -> ProjectResponse:
    """
    Start or update the specification phase.
    
    This is the first phase of SDD where requirements are defined.
    """
    manager = get_phase_manager()
    state = manager.get_or_create_project(request.project_id)
    
    # If we have specification content, complete this phase
    if request.specification:
        state = manager.complete_phase(
            state, 
            Phase.SPECIFY, 
            {"specification": request.specification}
        )
        message = "Specification phase completed"
    else:
        message = "Specification phase started - provide specification content to complete"
    
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message=message
    )


@router.post("/phases/plan", response_model=ProjectResponse)
async def plan_phase(request: PlanRequest) -> ProjectResponse:
    """
    Transition to and execute the plan phase.
    
    Requires specification phase to be completed.
    """
    manager = get_phase_manager()
    state = manager.load_state(request.project_id)
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{request.project_id}' not found"
        )
    
    try:
        state = manager.transition_to_phase(state, Phase.PLAN, force=request.force)
    except PhaseValidationError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": str(e), "validation_errors": e.errors}
        )
    
    # If we have plan content, complete this phase
    if request.plan:
        state = manager.complete_phase(state, Phase.PLAN, {"plan": request.plan})
        message = "Plan phase completed"
    else:
        message = "Plan phase started - provide plan content to complete"
    
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message=message
    )


@router.post("/phases/tasks", response_model=ProjectResponse)
async def tasks_phase(request: TasksRequest) -> ProjectResponse:
    """
    Transition to and execute the tasks phase.
    
    Breaks down the plan into actionable tasks.
    """
    manager = get_phase_manager()
    state = manager.load_state(request.project_id)
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{request.project_id}' not found"
        )
    
    try:
        state = manager.transition_to_phase(state, Phase.TASKS, force=request.force)
    except PhaseValidationError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": str(e), "validation_errors": e.errors}
        )
    
    # If we have tasks, complete this phase
    if request.tasks:
        state = manager.complete_phase(state, Phase.TASKS, {"tasks": request.tasks})
        message = f"Tasks phase completed with {len(request.tasks)} tasks"
    else:
        message = "Tasks phase started - provide task breakdown to complete"
    
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message=message
    )


@router.post("/phases/implement", response_model=ProjectResponse)
async def implement_phase(request: ImplementRequest) -> ProjectResponse:
    """
    Transition to and execute the implementation phase.
    
    This is where tasks are actually executed.
    """
    manager = get_phase_manager()
    state = manager.load_state(request.project_id)
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{request.project_id}' not found"
        )
    
    try:
        state = manager.transition_to_phase(state, Phase.IMPLEMENT, force=request.force)
    except PhaseValidationError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": str(e), "validation_errors": e.errors}
        )
    
    summary = manager.get_phase_summary(state)
    
    return ProjectResponse(
        success=True,
        project_id=state.project_id,
        current_phase=state.current_phase.value,
        phases=summary["phases"],
        message="Implementation phase started - execute tasks to complete"
    )


@router.get("/phases/workflow", response_model=Dict[str, Any])
async def get_workflow_info() -> Dict[str, Any]:
    """Get information about the SDD workflow phases."""
    return {
        "phases": [p.value for p in PHASE_ORDER],
        "description": {
            "specify": "Define what to build - requirements and user stories",
            "plan": "Define how to build it - architecture and tech decisions",
            "tasks": "Break down the plan into actionable, testable work units",
            "implement": "Execute the tasks and validate against specifications"
        },
        "transitions": {
            "specify → plan": "Requires completed specification",
            "plan → tasks": "Requires completed plan",
            "tasks → implement": "Requires task breakdown"
        }
    }
