"""
Two-Phase Application Entry Point for AI Agent System
Implements the revised architecture: Task List Generation + Sequential Task Execution
Zero-defect policy: robust CLI interface with two-phase execution
"""

import sys
import argparse
import time
import signal
from typing import Optional, Dict, Any
from pathlib import Path

from ..core_processing.two_phase_engine import TwoPhaseEngine, ExecutionPhase
from ..utils.exceptions import AIAgentException
from ..utils.logger import get_logger, setup_logging
from ..utils.config import load_config


class TwoPhaseAIAgent:
    """Two-Phase AI Agent implementing the revised architecture"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = load_config(config_path) if config_path else load_config()
        self.logger = get_logger("two_phase_app")
        
        # Initialize two-phase engine
        engine_config = {
            "click_delay": getattr(self.config, 'click_delay', 0.1),
            "typing_delay": getattr(self.config, 'typing_delay', 0.05),
            "scroll_duration": getattr(self.config, 'scroll_duration', 0.5),
            "drag_duration": getattr(self.config, 'drag_duration', 0.3),
            "screenshot_quality": getattr(self.config, 'screenshot_quality', 95),
            "screenshot_format": getattr(self.config, 'screenshot_format', 'PNG'),
            "max_task_retries": getattr(self.config, 'max_task_retries', 3),
            "max_command_retries": getattr(self.config, 'max_command_retries', 3),
            "command_timeout": getattr(self.config, 'command_timeout', 30),
            "task_timeout": getattr(self.config, 'task_timeout', 300),
        }
        
        self.engine = TwoPhaseEngine(engine_config)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("Two-Phase AI Agent initialized")
    
    def run(self, instruction: str, options: Dict[str, Any]) -> int:
        """Run AI Agent with instruction using two-phase execution"""
        try:
            self.logger.info(
                "Starting Two-Phase AI Agent execution",
                instruction=instruction,
                options=options,
            )
            
            # Setup logging if requested
            if options.get("verbose"):
                setup_logging(level="DEBUG")
            elif options.get("log_file"):
                setup_logging(file_path=options["log_file"])
            
            # Validate instruction
            if not instruction or not instruction.strip():
                self.logger.error("Instruction cannot be empty")
                return 1
            
            # Execute instruction using two-phase engine
            execution_context = self.engine.execute_instruction(instruction)
            
            # Simple success check
            success = execution_context.phase == ExecutionPhase.COMPLETED
            
            # Print results
            if not options.get("quiet"):
                print(f"\n{'='*60}")
                print("TWO-PHASE EXECUTION SUMMARY")
                print(f"{'='*60}")
                print(f"Instruction: {instruction}")
                print(f"Success: {success}")
                print(f"Executed Commands: {len(execution_context.executed_commands)}")
                if execution_context.error:
                    print(f"Error: {execution_context.error}")
                print(f"{'='*60}")
            
            # Save results if requested
            if options.get("output"):
                self._save_results(execution_context, options["output"])
            
            # Return exit code based on success
            return 0 if success else 1
                
        except AIAgentException as e:
            self.logger.error(f"Two-Phase AI Agent error: {e}")
            print(f"Error: {e}", file=sys.stderr)
            return 3
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 4
    
    def _save_results(self, execution_context, output_file: str):
        """Save execution results to file"""
        try:
            import json
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            results = {
                "instruction": execution_context.metadata.get("instruction"),
                "success": execution_context.phase == ExecutionPhase.COMPLETED,
                "executed_commands": execution_context.executed_commands,
                "error": execution_context.error,
                "total_tasks": len(execution_context.task_list.tasks) if execution_context.task_list else 0,
            }
            
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger.info(f"Results saved to: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            print(f"Warning: Failed to save results to {output_file}: {e}", file=sys.stderr)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        sys.exit(130)  # Standard exit code for SIGINT
    
    def shutdown(self):
        """Shutdown Two-Phase AI Agent"""
        self.logger.info("Shutting down Two-Phase AI Agent...")
        # Add any cleanup needed here
        self.logger.info("Two-Phase AI Agent shutdown complete")


def create_two_phase_argument_parser() -> argparse.ArgumentParser:
    """Create two-phase command line argument parser"""
    parser = argparse.ArgumentParser(
        description="AI Agent - Vision-based GUI automation with two-phase execution (Task Generation + Sequential Execution)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Open Safari"
  %(prog)s "Search for a calculator in Safari"
  %(prog)s --verbose "Click the button at coordinates (0.5, 0.3)"
  %(prog)s --output results.json "Automate login process"
        """
    )
    
    # Positional arguments
    parser.add_argument(
        "instruction",
        type=str,
        help="Natural language instruction for the AI agent"
    )
    
    # Configuration options
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save execution results to file (JSON format)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output except errors"
    )
    
    # Logging options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        help="Log to specified file"
    )
    
    # Execution options
    parser.add_argument(
        "--max-task-retries",
        type=int,
        default=3,
        help="Maximum number of retries for failed tasks (default: 3)"
    )
    
    parser.add_argument(
        "--max-command-retries",
        type=int,
        default=3,
        help="Maximum number of retries for failed commands (default: 3)"
    )
    
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=30,
        help="Timeout for individual commands in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--task-timeout",
        type=int,
        default=300,
        help="Timeout for individual tasks in seconds (default: 300)"
    )
    
    # Testing options
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with simulated execution"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate configuration and exit"
    )
    
    return parser


def validate_arguments(args: argparse.Namespace) -> bool:
    """Validate command line arguments"""
    # Check instruction
    if not args.instruction or not args.instruction.strip():
        print("Error: Instruction cannot be empty", file=sys.stderr)
        return False
    
    # Check config file
    if args.config and not Path(args.config).exists():
        print(f"Error: Configuration file not found: {args.config}", file=sys.stderr)
        return False
    
    # Check log file directory
    if args.log_file:
        log_path = Path(args.log_file)
        if not log_path.parent.exists():
            try:
                log_path.parent.mkdir(parents=True)
            except Exception as e:
                print(f"Error: Cannot create log directory: {e}", file=sys.stderr)
                return False
    
    # Check output file directory
    if args.output:
        output_path = Path(args.output)
        if not output_path.parent.exists():
            try:
                output_path.parent.mkdir(parents=True)
            except Exception as e:
                print(f"Error: Cannot create output directory: {e}", file=sys.stderr)
                return False
    
    # Validate timeout values
    if args.command_timeout <= 0:
        print("Error: Command timeout must be positive", file=sys.stderr)
        return False
    
    if args.task_timeout <= 0:
        print("Error: Task timeout must be positive", file=sys.stderr)
        return False
    
    if args.max_task_retries < 0:
        print("Error: Max task retries cannot be negative", file=sys.stderr)
        return False
    
    if args.max_command_retries < 0:
        print("Error: Max command retries cannot be negative", file=sys.stderr)
        return False
    
    return True


def main():
    """Main entry point for two-phase AI Agent"""
    # Parse arguments
    parser = create_two_phase_argument_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not validate_arguments(args):
        sys.exit(1)
    
    # Handle validate-only mode
    if args.validate_only:
        try:
            config = load_config(args.config)
            print("Configuration validation passed")
            return 0
        except Exception as e:
            print(f"Configuration validation failed: {e}", file=sys.stderr)
            return 1
    
    # Create Two-Phase AI Agent
    try:
        agent = TwoPhaseAIAgent(args.config)
    except Exception as e:
        print(f"Failed to initialize Two-Phase AI Agent: {e}", file=sys.stderr)
        return 1
    
    # Prepare options
    options = {
        "verbose": args.verbose,
        "quiet": args.quiet,
        "output": args.output,
        "log_file": args.log_file,
        "max_task_retries": args.max_task_retries,
        "max_command_retries": args.max_command_retries,
        "command_timeout": args.command_timeout,
        "task_timeout": args.task_timeout,
        "test_mode": args.test_mode,
    }
    
    # Run Two-Phase AI Agent
    start_time = time.time()
    exit_code = agent.run(args.instruction, options)
    execution_time = time.time() - start_time
    
    # Print final summary
    if not args.quiet:
        print(f"\nTotal execution time: {execution_time:.2f} seconds")
        print(f"Exit code: {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
