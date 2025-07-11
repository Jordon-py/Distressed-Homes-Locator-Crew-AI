# ======================================================================
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# ======================================================================

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
import os
import sys
import yaml
from crewai import LLM


# =========================
# 1. ENVIRONMENT LOADING & PATHS
# =========================
print("[CrewAI] Loading environment variables...")
load_dotenv(override=True)

# ======================================================================
# This crew is designed for web application development, including research, analysis, coding, and project
# =======================================================================                                                                

@CrewBase
class Gangshit():
    """Gangshit crew for web application development"""
    agents = List[BaseAgent]
    tasks = List[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # =========================
    # 2. INITIALIZATION
    # =========================
    @staticmethod
    def _setup_llms(self) -> tuple:
        """Setup and return configured LLM instances"""
        llama_model = os.getenv("OLLAMA_LLAMA3", "llama3.2:latest")
        gemma3_model = os.getenv("OLLAMA_GEMMA3", "gemma3:latest")
        deepseek_model = os.getenv("OLLAMA_DEEPSEEK", "deepseek-r1:1.5b-qwen-distill-q8_0")
        
        print(f"🔧 Using Ollama Llama3.2: {llama_model}")
        print(f"🔧 Using Ollama Gemma3: {gemma3_model}")
        print(f"🔧 Using Ollama DeepSeek: {deepseek_model}")
        
        llama3 = LLM(
            model=llama_model,
            base_url="http://localhost:11434",
        )
        gemma3 = LLM(
            model=gemma3_model,
            base_url="http://localhost:11434",
        )
        deepseek = LLM(
            model=deepseek_model,
            base_url="http://localhost:11434",
        )

        return llama3, gemma3, deepseek
    setup_llms = _setup_llms()
    

    def __init__(self):
        """Initialize the crew with proper configuration"""
        self.llama3, self.gemma3, self.deepseek = self._setup_llms()
        self.agents_config = self.agents_config
        self.tasks_config = self.tasks_config

    @before_kickoff
    def before_kickoff(self, inputs):
        """Setup before crew execution"""
        print("🚀 Crew is about to start!")
        print(f"📝 Topic: {inputs.get('topic', 'General Development')}")

    @after_kickoff
    def after_kickoff(self, output):
        """Cleanup after crew execution"""
        print("✅ Crew has completed execution!")
        print(f"📊 Generated {len(str(output))} characters of analysis")

    @agent
    def researcher(self) -> Agent:
        """
        Research specialist, uses GEMMA3 and web search tool.
        Config injected from YAML by CrewAI.
        """
        print("[CrewAI] Instantiating researcher agent...")
        try:
            return Agent(
                config=self.agents_config['researcher'],
                llm=self.gemma3,
                verbose=True,
                tools=[SerperDevTool()]  # Add more tools if needed
            )
        except Exception as e:
            print(f"[ERROR] Failed to initialize 'researcher' agent: {e}")
            raise

    @agent
    def analyst(self) -> Agent:
        """Analysis agent for processing information"""
        return Agent(
            config=self.agents_config.get('analyst', {}),
            verbose=True,
            llm=self.gemma3,
        )
        
    @agent
    def coding_agent(self) -> Agent:
        """Coding agent for development tasks"""
        return Agent(
            config=self.agents_config.get('coding_agent', {}),
            verbose=True,
            llm=self.deepseek,
        )
        
    @agent
    def overlord(self) -> Agent:
        """Overlord agent for coordination and management"""
        return Agent(
            config=self.agents_config.get('overlord', {}),
            verbose=True,
            llm=self.llama3,
        )

    @task
    def research_task(self) -> Task:
        """
        Task: Research with data curation and CSV/Markdown output.
        """
        print("[CrewAI] Configuring research_task...")
        try:
            return Task(
                config=self.tasks_config['research_task'],
                output_file='results/research_report.md',
                tools=[SerperDevTool()]
            )
        except Exception as e:
            print(f"[ERROR] Failed to configure 'research_task': {e}")
            raise

    @task
    def analyst_task(self) -> Task:
        """
        Task: Analyze research output, create architecture spec.
        """
        print("[CrewAI] Configuring analyst_task...")
        try:
            return Task(
                config=self.tasks_config['analyst_task'],
                output_file='results/analyst_report.md'
            )
        except Exception as e:
            print(f"[ERROR] Failed to configure 'analyst_task': {e}")
            raise

    @task
    def coding_task(self) -> Task:
        """
        Task: Build app/codebase for topic, ensure compliance.
        """
        print("[CrewAI] Configuring coding_task...")
        try:
            return Task(
                config=self.tasks_config['coding_task'],
                output_file='results/coding_report.md'
            )
        except Exception as e:
            print(f"[ERROR] Failed to configure 'coding_task': {e}")
            raise

    @task
    def overlord_task(self) -> Task:
        """
        Task: Final orchestration, QA, compliance reporting.
        """
        print("[CrewAI] Configuring overlord_task...")
        try:
            return Task(
                config=self.tasks_config['overlord_task'],
                output_file='results/overlord_report.md'
            )
        except Exception as e:
            print(f"[ERROR] Failed to configure 'overlord_task': {e}")
            raise


    # =========================
    # 6. CREW ASSEMBLY
    # =========================
    @crew
    def gangshit_crew(self) -> Crew:
        """
        Assemble all agents and tasks into a hierarchical crew.
        Includes manager LLM and live tools.
        """
        print("[CrewAI] Assembling crew (hierarchical process)...")

        return Crew(
            agents= self.agents, # Automatically created by the @agent decorator
            tasks= self.tasks, # Automatically created by the @task decorator
            # process=Process.sequential,
            
            verbose=True,
            process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            output_file='results/gangshit_report.md', # Output file for the crew's results
            manager_llm=self.llama3,  # Use Llama3 for crew management
            tools=[SerperDevTool()],  # Add any additional tools here
            
        )

# END OF FILE
# =========================