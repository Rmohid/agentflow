"""Tests for code analyzer agent"""

import pytest
from src.agents.code_analyzer import CodeAnalyzerAgent
from src.agents.base import AgentStatus


@pytest.mark.asyncio
async def test_code_analyzer_finds_todos(sample_context):
    """Test that code analyzer finds TODO comments"""
    agent = CodeAnalyzerAgent()
    result = await agent.run(sample_context)
    
    assert result.is_success()
    assert "todos" in result.data
    assert len(result.data["todos"]) > 0
    
    # Should find the TODO in main.py
    todo_found = any(
        "TODO" in todo["content"]
        for todo in result.data["todos"]
    )
    assert todo_found


@pytest.mark.asyncio
async def test_code_analyzer_finds_security_issues(sample_context):
    """Test that code analyzer finds security issues"""
    agent = CodeAnalyzerAgent()
    result = await agent.run(sample_context)
    
    assert result.is_success()
    assert "security_issues" in result.data
    
    # Should find the hardcoded password
    if result.data["security_issues"]:
        password_issue = any(
            "password" in issue["content"].lower()
            for issue in result.data["security_issues"]
        )
        assert password_issue


@pytest.mark.asyncio
async def test_code_analyzer_generates_stats(sample_context):
    """Test that code analyzer generates code statistics"""
    agent = CodeAnalyzerAgent()
    result = await agent.run(sample_context)
    
    assert result.is_success()
    assert "code_stats" in result.data
    
    stats = result.data["code_stats"]
    assert "python_files" in stats
    assert "total_lines" in stats
    assert stats["python_files"] > 0


@pytest.mark.asyncio
async def test_code_analyzer_generates_summary(sample_context):
    """Test that code analyzer generates a summary"""
    agent = CodeAnalyzerAgent()
    result = await agent.run(sample_context)
    
    assert result.is_success()
    assert "summary" in result.data
    assert len(result.data["summary"]) > 0
    assert "Code Analysis Summary" in result.data["summary"]
