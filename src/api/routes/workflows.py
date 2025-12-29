"""Workflow orchestration routes"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agents.base import AgentConfig, AgentContext
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.builder import BuilderAgent
from src.agents.orchestrator import OrchestratorAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class WorkflowRequest(BaseModel):
    """Request to start a workflow"""
    workflow_type: str = Field(..., description="Type of workflow: code_review, pr_check, dependency_audit")
    workspace_path: str = Field(..., description="Path to workspace/repository")
    config: dict = Field(default_factory=dict, description="Additional configuration")


class WorkflowResponse(BaseModel):
    """Workflow execution response"""
    workflow_id: str
    status: str
    data: dict


class WorkflowStatusResponse(BaseModel):
    """Workflow status response"""
    workflow_id: str
    name: str
    status: str
    created_at: str
    updated_at: str
    current_step: Optional[str]
    completed_steps: list[str]
    failed_steps: list[str]


# Initialize orchestrator with agents
orchestrator = OrchestratorAgent()
orchestrator.register_agent(CodeAnalyzerAgent())
orchestrator.register_agent(BuilderAgent())


@router.post("/execute", response_model=WorkflowResponse)
async def execute_workflow(request: WorkflowRequest):
    """Execute a workflow"""
    logger.info("Workflow execution requested", workflow_type=request.workflow_type)
    
    try:
        # Create execution context
        context = AgentContext(
            task_id=f"workflow-{request.workflow_type}",
            workspace_path=request.workspace_path,
            config={
                "workflow_type": request.workflow_type,
                **request.config
            }
        )
        
        # Execute workflow
        result = await orchestrator.run(context)
        
        if result.is_failed():
            raise HTTPException(
                status_code=500,
                detail=f"Workflow failed: {', '.join(result.errors)}"
            )
        
        return WorkflowResponse(
            workflow_id=result.data.get("workflow_id", "unknown"),
            status=result.status.value,
            data=result.data
        )
        
    except Exception as e:
        logger.error("Workflow execution failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{workflow_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    try:
        status = await orchestrator.get_workflow_status(workflow_id)
        
        if not status:
            raise HTTPException(
                status_code=404,
                detail=f"Workflow {workflow_id} not found"
            )
        
        return WorkflowStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get workflow status", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_workflows():
    """List all workflows"""
    try:
        states = await orchestrator.state_manager.list_states()
        
        return {
            "workflows": [
                {
                    "workflow_id": state.workflow_id,
                    "name": state.name,
                    "status": state.status,
                    "created_at": state.created_at.isoformat(),
                    "updated_at": state.updated_at.isoformat()
                }
                for state in states
            ]
        }
        
    except Exception as e:
        logger.error("Failed to list workflows", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
