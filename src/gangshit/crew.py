from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool

@CrewBase
class Gangshit:
    """Main CrewAI implementation for the Gangshit project."""
    
    BASE_DIR = Path(__file__).parent
    agents_config = str(BASE_DIR / "config" / "agents.yaml")
    tasks_config  = str(BASE_DIR / "config" / "tasks.yaml")

    def __init__(self):
        """Initialize with environment and configuration loading."""
        load_dotenv(override=True)
        
        # Load YAML configurations with error handling
        try:
            with open(self.agents_config, 'r') as f:
                self._agents_config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️ Warning: {self.agents_config} not found")
            self._agents_config = {}
            
        try:
            with open(self.tasks_config, 'r') as f:
                self._tasks_config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️ Warning: {self.tasks_config} not found")
            self._tasks_config = {}
        
        # Initialize LLMs with fallback models
        self.llama3 = LLM(
            model=os.getenv("OLLAMA_LLAMA3", "llama3.2"),
            base_url="http://localhost:11434", 
            stream=True
        )
        self.gemma3 = LLM(
            model=os.getenv("OLLAMA_GEMMA3", "gemma2:2b"),
            base_url="http://localhost:11434", 
            stream=True
        )
        self.deepseek = LLM(
            model=os.getenv("OLLAMA_DEEPSEEK", "deepseek-coder:1.3b"),
            base_url="http://localhost:11434", 
            stream=True
        )

    @before_kickoff
    def before_kickoff_handler(self, inputs):
        """Pre-execution setup and validation."""
        print("🚀 Starting CrewAI execution with inputs:", inputs.get('topic', 'Unknown'))
        return inputs

    @after_kickoff
    def after_kickoff_handler(self, output):
        """Post-execution cleanup and reporting."""
        print("✅ CrewAI execution completed; output length:", len(str(output)))
        return output

    @agent
    def researcher(self) -> Agent:
        """Research agent with web search capabilities."""
        return Agent(
            config=self._agents_config.get("researcher", {
                "role": "Researcher",
                "goal": "Gather comprehensive research on {topic}",
                "backstory": "Expert researcher with web search capabilities"
            }),
            llm=self.gemma3,
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def analyst(self) -> Agent:
        """Analysis and evaluation agent."""
        return Agent(
            config=self._agents_config.get("analyst", {
                "role": "Analyst", 
                "goal": "Analyze research and provide insights",
                "backstory": "Detail-oriented analyst"
            }),
            llm=self.gemma3,
            verbose=True,
        )

    @agent
    def coding_agent(self) -> Agent:
        """Development and implementation agent."""
        return Agent(
            config=self._agents_config.get("coding_agent", {
                "role": "Developer",
                "goal": "Implement solutions based on requirements", 
                "backstory": "Full-stack developer"
            }),
            llm=self.deepseek,
            verbose=True,
        )

    @agent
    def overlord(self) -> Agent:
        """Coordination and management agent."""
        return Agent(
            config=self._agents_config.get("overlord", {
                "role": "Project Manager",
                "goal": "Coordinate and validate all outputs",
                "backstory": "Experienced project coordinator"
            }),
            llm=self.llama3,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        """Research task configuration."""
        return Task(
            config=self._tasks_config.get("research_task", {
                "description": "Research the given topic thoroughly",
                "expected_output": "Comprehensive research report",
                "agent": "researcher"
            }),
            agent=self.researcher(),
            output_file="results/research_report.md",
        )

    @task
    def analyst_task(self) -> Task:
        """Analysis task configuration."""
        return Task(
            config=self._tasks_config.get("analyst_task", {
                "description": "Analyze research findings",
                "expected_output": "Analysis report with insights",
                "agent": "analyst"
            }),
            agent=self.analyst(),
            output_file="results/analyst_report.md",
        )

    @task
    def coding_task(self) -> Task:
        """Development task configuration."""
        return Task(
            config=self._tasks_config.get("coding_task", {
                "description": "Implement the solution",
                "expected_output": "Working codebase",
                "agent": "coding_agent"
            }),
            agent=self.coding_agent(),
            output_file="results/coding_report.md",
        )

    @task
    def overlord_task(self) -> Task:
        """Management and coordination task."""
        return Task(
            config=self._tasks_config.get("overlord_task", {
                "description": "Coordinate and validate all outputs",
                "expected_output": "Final project report",
                "agent": "overlord"
            }),
            agent=self.overlord(),
            output_file="results/overlord_report.md",
        )

    @crew
    def gangshit_crew(self) -> Crew:
        """Assemble the complete crew with hierarchical process."""
        # Ensure results directory exists
        Path("results").mkdir(exist_ok=True)
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            output_file="results/gangshit_report.md",
            manager_llm=self.llama3,
            stream=True,
        )
