"""Test configuration and fixtures"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing"""
    temp_dir = tempfile.mkdtemp()
    workspace = Path(temp_dir)
    
    # Create sample project structure
    (workspace / "src").mkdir()
    (workspace / "tests").mkdir()
    (workspace / "src" / "__init__.py").write_text("")
    (workspace / "src" / "main.py").write_text(
        "# TODO: Implement main function\n"
        "def main():\n"
        "    password = 'hardcoded123'  # Security issue\n"
        "    pass\n"
    )
    (workspace / "tests" / "test_main.py").write_text(
        "def test_example():\n"
        "    assert True\n"
    )
    (workspace / "pyproject.toml").write_text(
        "[project]\n"
        "name = 'test-project'\n"
        "version = '0.1.0'\n"
    )
    
    yield workspace
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_context(temp_workspace):
    """Create a sample agent context"""
    from src.agents.base import AgentContext
    
    return AgentContext(
        task_id="test-task",
        workspace_path=str(temp_workspace)
    )
