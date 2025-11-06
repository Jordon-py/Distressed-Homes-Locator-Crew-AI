#!/usr/bin/env python
"""
Main entry point for the Gangshit CrewAI project.
This file should be used as the primary entry point for the application.
"""
import sys
import warnings
from datetime import datetime
from .crew import Gangshit

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with comprehensive error handling.
    """
    inputs = {
        'topic': """Build a cross-platform desktop application that trains powerful ML and RL models to predict forex currency pair movements (e.g. EUR/USD, GBP/JPY), visualizes training and backtesting metrics, supports backtesting on historical data, provides explanatory tooltips suitable for both beginners and experts, and enables model export for real-world deployment.""",
        'requirements': [
            "Train both supervised ML (e.g. LSTM, random forest) and reinforcement learning (e.g. DQN, PPO) models using at least 10 years of historical forex data.",
            "Visualize training metrics (loss, accuracy, reward) in interactive charts (using Plotly/Matplotlib).",
            "Implement backtesting on multiple forex pairs with downloadable summary reports and equity curves.",
            "Offer user-friendly tooltips that explain model parameters, metrics, and actions in both beginner and expert modes.",
            "Ensure GUI is intuitive and cross-platform (Electron, Tauri, or similar).",
            "Modular backend/frontend separation; code quality enforced via formatting and security audits.",
        ],
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("🚀 Starting Gangshit crew...")
        crew = Gangshit().gangshit()
        result = crew.kickoff(inputs=inputs)
        print("✅ Crew execution completed!")
        print(f"📊 Result: {result}")
        return result
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Try: pip install -r requirements.txt")
        return None
    except FileNotFoundError as e:
        print(f"❌ File Not Found: {e}")
        print("💡 Check configuration files in src/gangshit/config/")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Gangshit().gangshit_crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Gangshit().gangshit_crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Gangshit().gangshit_crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
