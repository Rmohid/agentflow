#!/usr/bin/env python3
"""
Demo script to showcase AgentFlow capabilities with SDD workflow.

This demo shows:
1. The SDD (Specification-Driven Development) phase workflow
2. Code Analysis Agent
3. Builder Agent
4. Full Orchestration
"""

import asyncio
from pathlib import Path
from src.agents.base import AgentContext
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.builder import BuilderAgent
from src.agents.orchestrator import OrchestratorAgent
from src.core.phases import PhaseManager, Phase, PHASE_ORDER
from src.utils.logging import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


async def demo_sdd_phases():
    """Demo: SDD Phase Workflow"""
    print("\n" + "="*60)
    print("DEMO 1: Specification-Driven Development (SDD) Workflow")
    print("="*60)
    
    print("\n📋 AgentFlow uses the four-phase SDD workflow:\n")
    
    for i, phase in enumerate(PHASE_ORDER):
        arrow = "→" if i < len(PHASE_ORDER) - 1 else ""
        print(f"  {i+1}. {phase.value.upper():10} {arrow}")
    
    print("\n📂 Explore the .spec/ directory to see our specifications:\n")
    
    spec_files = [
        (".spec/specification.md", "What we're building (requirements)"),
        (".spec/plan.md", "How we're building it (architecture)"),
        (".spec/tasks.md", "Work breakdown (actionable tasks)"),
        (".spec/implementation.md", "Implementation log (decisions)"),
    ]
    
    for file_path, description in spec_files:
        exists = "✓" if Path(file_path).exists() else "✗"
        print(f"  {exists} {file_path:30} - {description}")
    
    # Demo the phase manager
    print("\n🔄 Creating a demo SDD project...")
    manager = PhaseManager()
    
    # Create or get demo project
    project_id = "demo-sdd-project"
    state = manager.get_or_create_project(project_id, "Demo SDD Project")
    
    print(f"\n  Project: {state.project_name}")
    print(f"  Current Phase: {state.current_phase.value.upper()}")
    
    # Show phase statuses
    print("\n  Phase Status:")
    summary = manager.get_phase_summary(state)
    for phase_name, phase_info in summary["phases"].items():
        status_icon = {
            "not_started": "⬜",
            "in_progress": "🟡",
            "completed": "🟢",
            "failed": "🔴"
        }.get(phase_info["status"], "⬜")
        print(f"    {status_icon} {phase_name.upper():12} - {phase_info['status']}")
    
    print("\n✓ SDD workflow demonstration complete!")


async def demo_code_analyzer():
    """Demo: Code Analyzer Agent"""
    print("\n" + "="*60)
    print("DEMO 2: Code Analyzer Agent")
    print("="*60)
    
    # Analyze the agentflow project itself
    agent = CodeAnalyzerAgent()
    context = AgentContext(
        task_id="demo-analyzer",
        workspace_path=str(Path.cwd()),
        current_phase="implement"  # Running in implementation phase
    )
    
    result = await agent.run(context)
    
    if result.is_success():
        print("\n✓ Analysis completed successfully!")
        print(f"\nExecution time: {result.execution_time_ms}ms")
        print("\n" + result.data["summary"])
        
        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")
    else:
        print("\n✗ Analysis failed!")
        for error in result.errors:
            print(f"  Error: {error}")


async def demo_builder():
    """Demo: Builder Agent"""
    print("\n" + "="*60)
    print("DEMO 3: Builder Agent")
    print("="*60)
    
    agent = BuilderAgent()
    context = AgentContext(
        task_id="demo-builder",
        workspace_path=str(Path.cwd()),
        current_phase="implement"
    )
    
    result = await agent.run(context)
    
    if result.is_success():
        print("\n✓ Build completed successfully!")
        print(f"\nExecution time: {result.execution_time_ms}ms")
        print("\n" + result.data["summary"])
        
        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")
    else:
        print("\n✗ Build failed!")
        for error in result.errors:
            print(f"  Error: {error}")


async def demo_orchestrator():
    """Demo: Orchestrator with full workflow"""
    print("\n" + "="*60)
    print("DEMO 4: Orchestrated Code Review Workflow")
    print("="*60)
    
    # Create orchestrator and register agents
    orchestrator = OrchestratorAgent()
    orchestrator.register_agent(CodeAnalyzerAgent())
    orchestrator.register_agent(BuilderAgent())
    
    context = AgentContext(
        task_id="demo-orchestrator",
        workspace_path=str(Path.cwd()),
        config={"workflow_type": "code_review"},
        current_phase="implement"
    )
    
    result = await orchestrator.run(context)
    
    if result.is_success():
        print("\n✓ Workflow completed successfully!")
        print(f"\nExecution time: {result.execution_time_ms}ms")
        print("\n" + "─"*60)
        print(result.data.get("summary", "No summary available"))
        print("─"*60)
    else:
        print("\n✗ Workflow failed!")
        for error in result.errors:
            print(f"  Error: {error}")


async def main():
    """Run all demos"""
    print("\n" + "#"*60)
    print("#  AgentFlow Demo - SDD + Agentic AI")
    print("#"*60)
    
    try:
        # Demo 1: SDD Phases
        await demo_sdd_phases()
        await asyncio.sleep(1)
        
        # Demo 2: Code Analyzer
        await demo_code_analyzer()
        await asyncio.sleep(1)
        
        # Demo 3: Builder
        await demo_builder()
        await asyncio.sleep(1)
        
        # Demo 4: Full Orchestration
        await demo_orchestrator()
        
        print("\n" + "="*60)
        print("All demos completed!")
        print("="*60)
        
        print("\n💡 Next steps:")
        print("  1. Explore .spec/ directory to see SDD artifacts")
        print("  2. Read docs/sdd-guide.md to learn about SDD")
        print("  3. Start the API: uvicorn src.api.main:app --reload")
        print("  4. Visit http://localhost:8000/docs for API docs")
        print("  5. Try the phase API: POST /api/v1/project/create")
        
    except Exception as e:
        logger.error("Demo failed", error=str(e))
        raise


if __name__ == "__main__":
    asyncio.run(main())
