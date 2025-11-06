"""Test CrewAI imports and basic functionality."""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_crewai_imports():
    """Test that all required CrewAI components can be imported."""
    try:
        from crewai import Agent, Crew, Process, Task, LLM
        print("✅ Core CrewAI imports successful")
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import CrewAI components: {e}")

def test_gangshit_import():
    """Test that our Gangshit crew can be imported."""
    try:
        from gangshit.crew import Gangshit
        print("✅ Gangshit crew import successful")
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import Gangshit crew: {e}")

def test_tools_import():
    """Test that CrewAI tools can be imported."""
    try:
        from crewai_tools import SerperDevTool
        print("✅ CrewAI tools import successful")
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import CrewAI tools: {e}")

def test_crew_instantiation():
    """Test that the Gangshit crew can be instantiated."""
    try:
        from gangshit.crew import Gangshit
        crew_instance = Gangshit()
        assert crew_instance is not None
        print("✅ Crew instantiation successful")
    except Exception as e:
        pytest.fail(f"Failed to instantiate crew: {e}")

if __name__ == "__main__":
    test_crewai_imports()
    test_gangshit_import() 
    test_tools_import()
    test_crew_instantiation()
    print("🎉 All import tests passed!")