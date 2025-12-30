"""Tests for the SDD phase management module."""

import json
import pytest
from pathlib import Path
from datetime import datetime

from src.core.phases import (
    Phase,
    PhaseStatus,
    PhaseResult,
    ProjectState,
    PhaseManager,
    PhaseValidationError,
    PHASE_ORDER,
)


class TestPhaseEnums:
    """Tests for Phase and PhaseStatus enums."""
    
    def test_phase_values(self):
        """Test Phase enum has correct values."""
        assert Phase.SPECIFY.value == "specify"
        assert Phase.PLAN.value == "plan"
        assert Phase.TASKS.value == "tasks"
        assert Phase.IMPLEMENT.value == "implement"
    
    def test_phase_status_values(self):
        """Test PhaseStatus enum has correct values."""
        assert PhaseStatus.NOT_STARTED.value == "not_started"
        assert PhaseStatus.IN_PROGRESS.value == "in_progress"
        assert PhaseStatus.COMPLETED.value == "completed"
        assert PhaseStatus.FAILED.value == "failed"
    
    def test_phase_order(self):
        """Test PHASE_ORDER contains all phases in correct order."""
        assert len(PHASE_ORDER) == 4
        assert PHASE_ORDER[0] == Phase.SPECIFY
        assert PHASE_ORDER[1] == Phase.PLAN
        assert PHASE_ORDER[2] == Phase.TASKS
        assert PHASE_ORDER[3] == Phase.IMPLEMENT


class TestPhaseResult:
    """Tests for PhaseResult model."""
    
    def test_default_values(self):
        """Test PhaseResult has correct defaults."""
        result = PhaseResult(phase=Phase.SPECIFY)
        
        assert result.phase == Phase.SPECIFY
        assert result.status == PhaseStatus.NOT_STARTED
        assert result.started_at is None
        assert result.completed_at is None
        assert result.artifacts == {}
        assert result.validation_errors == []
    
    def test_start(self):
        """Test starting a phase."""
        result = PhaseResult(phase=Phase.SPECIFY)
        result.start()
        
        assert result.status == PhaseStatus.IN_PROGRESS
        assert result.started_at is not None
    
    def test_complete(self):
        """Test completing a phase."""
        result = PhaseResult(phase=Phase.SPECIFY)
        result.start()
        result.complete(artifacts={"spec": "content"})
        
        assert result.status == PhaseStatus.COMPLETED
        assert result.completed_at is not None
        assert result.artifacts == {"spec": "content"}
    
    def test_fail(self):
        """Test failing a phase."""
        result = PhaseResult(phase=Phase.SPECIFY)
        result.start()
        result.fail(errors=["Something went wrong"])
        
        assert result.status == PhaseStatus.FAILED
        assert result.completed_at is not None
        assert result.validation_errors == ["Something went wrong"]


class TestProjectState:
    """Tests for ProjectState model."""
    
    def test_create_project_state(self):
        """Test creating a new project state."""
        state = ProjectState(project_id="test-project")
        
        assert state.project_id == "test-project"
        assert state.current_phase == Phase.SPECIFY
        assert state.specification is None
        assert state.plan is None
        assert state.tasks == []
    
    def test_phases_initialized(self):
        """Test that all phases are initialized."""
        state = ProjectState(project_id="test-project")
        
        for phase in Phase:
            result = state.get_phase_result(phase)
            assert result is not None
            assert result.phase == phase
    
    def test_update_phase(self):
        """Test updating a phase result."""
        state = ProjectState(project_id="test-project")
        
        result = PhaseResult(phase=Phase.SPECIFY)
        result.start()
        result.complete(artifacts={"spec": "test"})
        
        state.update_phase(Phase.SPECIFY, result)
        
        updated = state.get_phase_result(Phase.SPECIFY)
        assert updated.status == PhaseStatus.COMPLETED


class TestPhaseManager:
    """Tests for PhaseManager."""
    
    @pytest.fixture
    def temp_state_dir(self, tmp_path):
        """Create a temporary state directory."""
        return str(tmp_path / "test_state")
    
    @pytest.fixture
    def manager(self, temp_state_dir):
        """Create a PhaseManager with temp directory."""
        return PhaseManager(state_dir=temp_state_dir)
    
    def test_create_project(self, manager):
        """Test creating a new project."""
        state = manager.create_project("test-proj", "Test Project")
        
        assert state.project_id == "test-proj"
        assert state.project_name == "Test Project"
        assert state.current_phase == Phase.SPECIFY
        
        # Specify phase should be started
        result = state.get_phase_result(Phase.SPECIFY)
        assert result.status == PhaseStatus.IN_PROGRESS
    
    def test_save_and_load_state(self, manager):
        """Test saving and loading project state."""
        original = manager.create_project("save-test", "Save Test")
        original.specification = {"title": "Test Spec"}
        manager.save_state(original)
        
        loaded = manager.load_state("save-test")
        
        assert loaded is not None
        assert loaded.project_id == "save-test"
        assert loaded.specification == {"title": "Test Spec"}
    
    def test_load_nonexistent(self, manager):
        """Test loading a nonexistent project."""
        state = manager.load_state("does-not-exist")
        assert state is None
    
    def test_get_or_create_new(self, manager):
        """Test get_or_create with new project."""
        state = manager.get_or_create_project("new-proj")
        assert state.project_id == "new-proj"
    
    def test_get_or_create_existing(self, manager):
        """Test get_or_create with existing project."""
        manager.create_project("existing-proj", "Existing")
        state = manager.get_or_create_project("existing-proj")
        
        assert state.project_name == "Existing"
    
    def test_validate_phase_gate_specify_to_plan(self, manager):
        """Test validation from SPECIFY to PLAN."""
        state = manager.create_project("gate-test")
        
        # Without specification, should fail
        errors = manager.validate_phase_gate(state, Phase.PLAN)
        assert len(errors) > 0
        assert any("completed" in e.lower() for e in errors)
        
        # Complete specify phase with specification
        state = manager.complete_phase(
            state, 
            Phase.SPECIFY, 
            {"specification": {"title": "Test"}}
        )
        
        errors = manager.validate_phase_gate(state, Phase.PLAN)
        assert len(errors) == 0
    
    def test_transition_to_phase(self, manager):
        """Test transitioning between phases."""
        state = manager.create_project("transition-test")
        
        # Complete SPECIFY phase
        state = manager.complete_phase(
            state,
            Phase.SPECIFY,
            {"specification": {"title": "Test"}}
        )
        
        # Transition to PLAN
        state = manager.transition_to_phase(state, Phase.PLAN)
        
        assert state.current_phase == Phase.PLAN
        result = state.get_phase_result(Phase.PLAN)
        assert result.status == PhaseStatus.IN_PROGRESS
    
    def test_transition_fails_without_gate(self, manager):
        """Test that transition fails without meeting gate conditions."""
        state = manager.create_project("fail-test")
        
        with pytest.raises(PhaseValidationError) as exc_info:
            manager.transition_to_phase(state, Phase.PLAN)
        
        assert len(exc_info.value.errors) > 0
    
    def test_transition_with_force(self, manager):
        """Test force transition bypasses validation."""
        state = manager.create_project("force-test")
        
        # Should succeed with force=True even without spec
        state = manager.transition_to_phase(state, Phase.PLAN, force=True)
        
        assert state.current_phase == Phase.PLAN
    
    def test_complete_phase_stores_data(self, manager):
        """Test that completing phases stores the appropriate data."""
        state = manager.create_project("data-test")
        
        # Complete SPECIFY
        state = manager.complete_phase(
            state,
            Phase.SPECIFY,
            {"specification": {"title": "My Spec"}}
        )
        assert state.specification == {"title": "My Spec"}
        
        # Complete PLAN
        state = manager.transition_to_phase(state, Phase.PLAN, force=True)
        state = manager.complete_phase(
            state,
            Phase.PLAN,
            {"plan": {"architecture": "layered"}}
        )
        assert state.plan == {"architecture": "layered"}
        
        # Complete TASKS
        state = manager.transition_to_phase(state, Phase.TASKS, force=True)
        state = manager.complete_phase(
            state,
            Phase.TASKS,
            {"tasks": [{"name": "task1"}, {"name": "task2"}]}
        )
        assert len(state.tasks) == 2
    
    def test_get_phase_summary(self, manager):
        """Test getting phase summary."""
        state = manager.create_project("summary-test", "Summary Test")
        
        summary = manager.get_phase_summary(state)
        
        assert summary["project_id"] == "summary-test"
        assert summary["project_name"] == "Summary Test"
        assert summary["current_phase"] == "specify"
        assert "phases" in summary
        assert "specify" in summary["phases"]
        assert "plan" in summary["phases"]


class TestPhaseValidationError:
    """Tests for PhaseValidationError."""
    
    def test_error_with_details(self):
        """Test creating error with details."""
        error = PhaseValidationError(
            "Cannot transition",
            errors=["Missing spec", "Missing plan"]
        )
        
        assert str(error) == "Cannot transition"
        assert error.errors == ["Missing spec", "Missing plan"]
