import pytest
import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gangshit.crew import Gangshit

class TestGangshitCrew:
    """Test suite for Gangshit CrewAI implementation."""
    
    def test_crew_initialization(self):
        """Test that the crew can be properly initialized."""
        crew_instance = Gangshit()
        assert crew_instance is not None
        assert hasattr(crew_instance, '_agents_config')
        assert hasattr(crew_instance, '_tasks_config')
    
    def test_agents_config_loading(self):
        """Test that agents configuration loads properly."""
        crew_instance = Gangshit()
        config = crew_instance._agents_config
        
        required_agents = ['researcher', 'analyst', 'coding_agent', 'overlord']
        for agent in required_agents:
            assert agent in config, f"Missing agent configuration: {agent}"
    
    def test_tasks_config_loading(self):
        """Test that tasks configuration loads properly.""" 
        crew_instance = Gangshit()
        config = crew_instance._tasks_config
        
        required_tasks = ['research_task', 'analyst_task', 'coding_task', 'overlord_task']
        for task in required_tasks:
            assert task in config, f"Missing task configuration: {task}"
    
    def test_crew_creation(self):
        """Test that the crew can be created without errors."""
        crew_instance = Gangshit()
        crew = crew_instance.gangshit()
        assert crew is not None
        assert len(crew.agents) == 4
        assert len(crew.tasks) == 4

if __name__ == "__main__":
    pytest.main([__file__])