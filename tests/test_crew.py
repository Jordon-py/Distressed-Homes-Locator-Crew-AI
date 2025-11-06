"""Test CrewAI crew execution and functionality."""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_crew_configuration():
    """Test that crew can be properly configured."""
    from gangshit.crew import Gangshit
    
    crew_instance = Gangshit()
    crew = crew_instance.gangshit_crew()
    
    assert crew is not None
    assert len(crew.agents) == 4  # researcher, analyst, coding_agent, overlord
    assert len(crew.tasks) == 4   # corresponding tasks
    print("✅ Crew configuration test passed")

def test_agent_creation():
    """Test that all agents can be created successfully."""
    from gangshit.crew import Gangshit
    
    crew_instance = Gangshit()
    
    # Test individual agent creation
    researcher = crew_instance.researcher()
    analyst = crew_instance.analyst()
    coding_agent = crew_instance.coding_agent()
    overlord = crew_instance.overlord()
    
    assert researcher is not None
    assert analyst is not None
    assert coding_agent is not None
    assert overlord is not None
    print("✅ Agent creation test passed")

def test_task_creation():
    """Test that all tasks can be created successfully."""
    from gangshit.crew import Gangshit
    
    crew_instance = Gangshit()
    
    # Test individual task creation
    research_task = crew_instance.research_task()
    analyst_task = crew_instance.analyst_task()
    coding_task = crew_instance.coding_task()
    overlord_task = crew_instance.overlord_task()
    
    assert research_task is not None
    assert analyst_task is not None
    assert coding_task is not None
    assert overlord_task is not None
    print("✅ Task creation test passed")

if __name__ == "__main__":
    test_crew_configuration()
    test_agent_creation()
    test_task_creation()
    print("🎉 All crew tests passed!")
