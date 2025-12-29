#!/usr/bin/env python3
"""
Demo script to showcase AgentFlow capabilities
"""

import asyncio
from pathlib import Path
from src.agents.base import AgentContext
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.builder import BuilderAgent
from src.agents.orchestrator import OrchestratorAgent
from src.utils.logging import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


async def demo_code_analyzer():
    """Demo: Code Analyzer Agent"""
    print("\n" + "="*60)
    print("DEMO 1: Code Analyzer Agent")
    print("="*60)
    
    # Analyze the agentflow project itself
    agent = CodeAnalyzerAgent()
    context = AgentContext(
        task_id="demo-analyzer",
        workspace_path=str(Path.cwd())
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
    print("DEMO 2: Builder Agent")
    print("="*60)
    
    agent = BuilderAgent()
    context = AgentContext(
        task_id="demo-builder",
        workspace_path=str(Path.cwd())
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
    print("DEMO 3: Orchestrated Code Review Workflow")
    print("="*60)
    
    # Create orchestrator and register agents
    orchestrator = OrchestratorAgent()
    orchestrator.register_agent(CodeAnalyzerAgent())
    orchestrator.register_agent(BuilderAgent())
    
    context = AgentContext(
        task_id="demo-orchestrator",
        workspace_path=str(Path.cwd()),
        config={"workflow_type": "code_review"}
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
    print("#  AgentFlow Demo - Agentic AI in Action")
    print("#"*60)
    
    try:
        # Demo 1: Code Analyzer
        await demo_code_analyzer()
        await asyncio.sleep(1)
        
        # Demo 2: Builder
        await demo_builder()
        await asyncio.sleep(1)
        
        # Demo 3: Full Orchestration
        await demo_orchestrator()
        
        print("\n" + "="*60)
        print("All demos completed!")
        print("="*60)
        
        print("\n💡 Next steps:")
        print("  1. Start the API server: uvicorn src.api.main:app --reload")
        print("  2. Visit http://localhost:8000/docs for interactive API docs")
        print("  3. Run tests: pytest")
        print("  4. Check coverage: pytest --cov=src --cov-report=html")
        
    except Exception as e:
        logger.error("Demo failed", error=str(e))
        raise


if __name__ == "__main__":
    asyncio.run(main())
