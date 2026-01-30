#!/usr/bin/env python3
"""
Simple AI Agent Runner
Usage: python3 run.py "your instruction here"
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py \"your instruction here\"")
        print("Example: python3 run.py \"Take a screenshot\"")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    print(f"🤖 AI Agent executing: {instruction}")
    
    try:
        from ai_agent.user_interface.two_phase_app import TwoPhaseAIAgent
        
        # Initialize the agent
        config_path = current_dir / "config.yaml"
        agent = TwoPhaseAIAgent(config_path=str(config_path) if config_path.exists() else None)
        
        # Run the instruction
        options = {"debug": "--debug" in sys.argv}
        result = agent.run(instruction, options)
        
        if result:
            print("✅ Task completed successfully")
        else:
            print("❌ Task failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies:")
        print("  pip install -r requirements.txt")
        print("  pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
