#!/usr/bin/env python3
"""
Main AI Agent Application
Simple command-line interface for the AI Agent system
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    """Main entry point for the AI Agent CLI"""
    parser = argparse.ArgumentParser(
        description="AI Agent - Vision-based GUI automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-agent "Take a screenshot"
  ai-agent --config config.yaml "Open web browser"
  ai-agent --debug "Click at coordinates (0.5, 0.5)"
        """
    )
    
    parser.add_argument(
        "instruction",
        help="Natural language instruction for the AI agent"
    )
    
    parser.add_argument(
        "--config", "-c",
        help="Configuration file path",
        default="config.yaml"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Show what would be done without executing"
    )
    
    args = parser.parse_args()
    
    try:
        # Import here to avoid import issues
        from ai_agent.user_interface.two_phase_app import TwoPhaseAIAgent
        
        # Create and run the app
        app = TwoPhaseAIAgent(config_path=args.config)
        
        if args.dry_run:
            print(f"[DRY RUN] Would execute: {args.instruction}")
            return
            
        options = {"debug": args.debug}
        result = app.run(args.instruction, options)
        
        if result:
            print("✅ Task completed successfully")
            sys.exit(0)
        else:
            print("❌ Task failed")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the AI Agent is properly installed:")
        print("  pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
