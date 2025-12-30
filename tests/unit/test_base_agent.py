"""Tests for base agent functionality"""

import pytest
from src.agents.base import (
    BaseAgent,
    AgentConfig,
    AgentContext,
    AgentResult,
    AgentStatus
)


class TestAgent(BaseAgent):
    """Test agent implementation"""
    
    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            status=AgentStatus.SUCCESS,
            data={"test": "data"}
        )


class FailingAgent(BaseAgent):
    """Agent that always fails"""
    
    async def execute(self, context: AgentContext) -> AgentResult:
        raise ValueError("Test error")


@pytest.mark.asyncio
async def test_agent_success(sample_context):
    """Test successful agent execution"""
    config = AgentConfig(name="test_agent", description="Test agent")
    agent = TestAgent(config)
    
    result = await agent.run(sample_context)
    
    assert result.is_success()
    assert result.agent_name == "test_agent"
    assert result.data["test"] == "data"
    assert result.execution_time_ms >= 0  # Could be 0 for very fast execution


@pytest.mark.asyncio
async def test_agent_failure_with_retry(sample_context):
    """Test agent failure with retry logic"""
    config = AgentConfig(
        name="failing_agent",
        description="Failing agent",
        max_retries=2
    )
    agent = FailingAgent(config)
    
    result = await agent.run(sample_context)
    
    assert result.is_failed()
    assert len(result.errors) > 0
    assert "Test error" in result.errors[0]


@pytest.mark.asyncio
async def test_disabled_agent(sample_context):
    """Test that disabled agents don't execute"""
    config = AgentConfig(
        name="disabled_agent",
        description="Disabled agent",
        enabled=False
    )
    agent = TestAgent(config)
    
    result = await agent.run(sample_context)
    
    assert result.status == AgentStatus.CANCELLED
    assert "disabled" in result.errors[0].lower()


def test_agent_stats():
    """Test agent statistics"""
    config = AgentConfig(name="stats_agent", description="Stats agent")
    agent = TestAgent(config)
    
    stats = agent.get_stats()
    
    assert stats["name"] == "stats_agent"
    assert stats["status"] == AgentStatus.IDLE.value
    assert stats["execution_count"] == 0
    assert stats["enabled"] is True
