"""Analysis routes"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agents.base import AgentContext
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.builder import BuilderAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class AnalysisRequest(BaseModel):
    """Request for code analysis"""
    workspace_path: str = Field(..., description="Path to workspace/repository to analyze")


class BuildRequest(BaseModel):
    """Request for build/test"""
    workspace_path: str = Field(..., description="Path to workspace/repository to build")


@router.post("/code")
async def analyze_code(request: AnalysisRequest):
    """Analyze code in a workspace"""
    logger.info("Code analysis requested", workspace=request.workspace_path)
    
    try:
        agent = CodeAnalyzerAgent()
        context = AgentContext(
            task_id="analyze-code",
            workspace_path=request.workspace_path
        )
        
        result = await agent.run(context)
        
        if result.is_failed():
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {', '.join(result.errors)}"
            )
        
        return {
            "status": result.status.value,
            "data": result.data,
            "warnings": result.warnings,
            "execution_time_ms": result.execution_time_ms
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Code analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build")
async def run_build(request: BuildRequest):
    """Run build and tests"""
    logger.info("Build requested", workspace=request.workspace_path)
    
    try:
        agent = BuilderAgent()
        context = AgentContext(
            task_id="run-build",
            workspace_path=request.workspace_path
        )
        
        result = await agent.run(context)
        
        if result.is_failed():
            raise HTTPException(
                status_code=500,
                detail=f"Build failed: {', '.join(result.errors)}"
            )
        
        return {
            "status": result.status.value,
            "data": result.data,
            "warnings": result.warnings,
            "execution_time_ms": result.execution_time_ms
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Build failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
