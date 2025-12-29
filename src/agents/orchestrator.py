"""Orchestrator Agent - Coordinates multiple agents to complete complex workflows"""

from typing import Any, Dict, List, Optional
from uuid import uuid4
from src.agents.base import BaseAgent, AgentConfig, AgentContext, AgentResult, AgentStatus
from src.core.task_queue import Task, TaskQueue, TaskStatus, TaskPriority
from src.core.state import StateManager
from src.utils.logging import get_logger

logger = get_logger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Agent that orchestrates complex workflows by coordinating
    multiple specialized agents.
    """

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        agents: Optional[Dict[str, BaseAgent]] = None
    ):
        if config is None:
            config = AgentConfig(
                name="orchestrator",
                description="Coordinates multiple agents for complex workflows",
                tags=["orchestration", "coordination"],
                timeout_seconds=1800  # 30 minutes for complex workflows
            )
        super().__init__(config)
        
        self.agents = agents or {}
        self.task_queue = TaskQueue(max_concurrent_tasks=5)
        self.state_manager = StateManager()
        
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info("Registered agent", agent=agent.name)
    
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute orchestrated workflow"""
        logger.info("Starting orchestration", task_id=context.task_id)
        
        result = AgentResult(
            agent_name=self.name,
            status=AgentStatus.RUNNING
        )
        
        try:
            # Determine workflow type from context
            workflow_type = context.config.get("workflow_type", "code_review")
            
            if workflow_type == "code_review":
                workflow_result = await self._execute_code_review(context)
            elif workflow_type == "pr_check":
                workflow_result = await self._execute_pr_check(context)
            elif workflow_type == "dependency_audit":
                workflow_result = await self._execute_dependency_audit(context)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            result.data = workflow_result
            result.status = AgentStatus.SUCCESS
            
            logger.info(
                "Orchestration completed",
                task_id=context.task_id,
                workflow_type=workflow_type
            )
            
        except Exception as e:
            logger.error("Orchestration failed", task_id=context.task_id, error=str(e))
            result.status = AgentStatus.FAILED
            result.add_error(str(e))
        
        return result
    
    async def _execute_code_review(self, context: AgentContext) -> Dict[str, Any]:
        """Execute a code review workflow"""
        workflow_id = str(uuid4())
        
        # Create workflow state
        state = await self.state_manager.create_state(
            workflow_id=workflow_id,
            name="code_review"
        )
        
        results = {
            "workflow_id": workflow_id,
            "workflow_type": "code_review",
            "agent_results": {}
        }
        
        # Step 1: Code Analysis
        if "code_analyzer" in self.agents:
            logger.info("Running code analysis", workflow_id=workflow_id)
            analyzer = self.agents["code_analyzer"]
            analysis_result = await analyzer.run(context)
            results["agent_results"]["code_analyzer"] = analysis_result.dict()
            
            await self.state_manager.update_agent_state(
                workflow_id=workflow_id,
                agent_name="code_analyzer",
                agent_data={"status": "completed", "result": analysis_result.dict()}
            )
        
        # Step 2: Run Build & Tests
        if "builder" in self.agents:
            logger.info("Running build and tests", workflow_id=workflow_id)
            builder = self.agents["builder"]
            build_result = await builder.run(context)
            results["agent_results"]["builder"] = build_result.dict()
            
            await self.state_manager.update_agent_state(
                workflow_id=workflow_id,
                agent_name="builder",
                agent_data={"status": "completed", "result": build_result.dict()}
            )
        
        # Generate final summary
        results["summary"] = self._generate_code_review_summary(
            results["agent_results"]
        )
        
        # Update workflow state
        await self.state_manager.update_state(
            workflow_id=workflow_id,
            status="completed",
            data=results
        )
        
        return results
    
    async def _execute_pr_check(self, context: AgentContext) -> Dict[str, Any]:
        """Execute PR checks workflow"""
        workflow_id = str(uuid4())
        
        state = await self.state_manager.create_state(
            workflow_id=workflow_id,
            name="pr_check"
        )
        
        results = {
            "workflow_id": workflow_id,
            "workflow_type": "pr_check",
            "agent_results": {},
            "checks_passed": True
        }
        
        # Run all checks in parallel via task queue
        tasks = []
        
        if "code_analyzer" in self.agents:
            task = Task(
                name="analyze_code",
                agent_name="code_analyzer",
                priority=TaskPriority.HIGH,
                input_data={"context": context.dict() if hasattr(context, 'dict') else {}}
            )
            task_id = await self.task_queue.add_task(task)
            tasks.append(task_id)
        
        if "builder" in self.agents:
            task = Task(
                name="run_build",
                agent_name="builder",
                priority=TaskPriority.HIGH,
                input_data={"context": context.dict() if hasattr(context, 'dict') else {}}
            )
            task_id = await self.task_queue.add_task(task)
            tasks.append(task_id)
        
        # Execute tasks
        for task_id in tasks:
            task = await self.task_queue.get_task(task_id)
            if task and task.agent_name in self.agents:
                agent = self.agents[task.agent_name]
                await self.task_queue.mark_task_started(task_id)
                
                agent_result = await agent.run(context)
                results["agent_results"][task.agent_name] = agent_result.dict()
                
                if agent_result.is_failed():
                    results["checks_passed"] = False
                    await self.task_queue.mark_task_failed(
                        task_id,
                        "Agent execution failed"
                    )
                else:
                    await self.task_queue.mark_task_completed(
                        task_id,
                        {"result": agent_result.dict()}
                    )
        
        results["summary"] = f"PR Checks: {'PASSED' if results['checks_passed'] else 'FAILED'}"
        
        await self.state_manager.update_state(
            workflow_id=workflow_id,
            status="completed",
            data=results
        )
        
        return results
    
    async def _execute_dependency_audit(self, context: AgentContext) -> Dict[str, Any]:
        """Execute dependency audit workflow"""
        workflow_id = str(uuid4())
        
        state = await self.state_manager.create_state(
            workflow_id=workflow_id,
            name="dependency_audit"
        )
        
        results = {
            "workflow_id": workflow_id,
            "workflow_type": "dependency_audit",
            "dependencies": [],
            "vulnerabilities": [],
            "updates_available": []
        }
        
        # This would check dependencies using pip, npm, etc.
        # For now, placeholder implementation
        results["summary"] = "Dependency audit completed (implementation pending)"
        
        await self.state_manager.update_state(
            workflow_id=workflow_id,
            status="completed",
            data=results
        )
        
        return results
    
    def _generate_code_review_summary(
        self,
        agent_results: Dict[str, Any]
    ) -> str:
        """Generate summary from all agent results"""
        summary_parts = ["Code Review Summary:", ""]
        
        # Code Analysis Summary
        if "code_analyzer" in agent_results:
            analyzer_data = agent_results["code_analyzer"].get("data", {})
            summary_parts.append("Code Analysis:")
            summary_parts.append(analyzer_data.get("summary", "No data available"))
            summary_parts.append("")
        
        # Build Summary
        if "builder" in agent_results:
            builder_data = agent_results["builder"].get("data", {})
            summary_parts.append("Build & Tests:")
            summary_parts.append(builder_data.get("summary", "No data available"))
            summary_parts.append("")
        
        # Overall recommendation
        all_success = all(
            result.get("status") == "success"
            for result in agent_results.values()
        )
        
        if all_success:
            summary_parts.append("✓ Overall: Code review PASSED - Ready for merge")
        else:
            summary_parts.append("✗ Overall: Code review FAILED - Issues need attention")
        
        return "\n".join(summary_parts)
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow"""
        state = await self.state_manager.get_state(workflow_id)
        if not state:
            return None
        
        return {
            "workflow_id": state.workflow_id,
            "name": state.name,
            "status": state.status,
            "created_at": state.created_at.isoformat(),
            "updated_at": state.updated_at.isoformat(),
            "current_step": state.current_step,
            "completed_steps": state.completed_steps,
            "failed_steps": state.failed_steps,
        }
