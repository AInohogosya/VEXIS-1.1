"""
Two-Phase Execution Engine for AI Agent System
Implements the revised architecture: Task List Generation + Sequential Task Execution
Zero-defect policy: robust execution with context preservation
"""

import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from enum import Enum

from ..platform_abstraction.gui_automation import GUIAutomation, AutomationResult
from ..platform_abstraction.screenshot_capture import ScreenshotCapture, ScreenshotMetadata
from ..external_integration.model_runner import ModelRunner, TaskType
from ..utils.exceptions import ExecutionError, ValidationError, TaskGenerationError
from ..utils.logger import get_logger
from .command_parser import ParsedCommand, CommandType


@dataclass
class Task:
    """Individual task structure"""
    description: str


@dataclass
class TaskList:
    """Task list structure"""
    tasks: List[str]  # Simple list of task descriptions
    instruction: str
    generation_time: float = 0.0


class ExecutionPhase(Enum):
    """Execution phases"""
    TASK_GENERATION = "task_generation"
    TASK_EXECUTION = "task_execution"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionContext:
    """Execution context for 2-Phase Architecture"""
    phase: ExecutionPhase
    current_task_index: int = 0
    current_screenshot: Optional[bytes] = None
    previous_screenshot: Optional[bytes] = None
    previous_command: Optional[str] = None
    task_list: Optional[TaskList] = None
    executed_commands: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TwoPhaseEngine:
    """Two-phase execution engine implementing the revised architecture"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger("two_phase_engine")
        
        # Initialize components
        self.gui_automation = GUIAutomation(
            click_delay=self.config.get("click_delay", 0.1),
            typing_delay=self.config.get("typing_delay", 0.05),
            scroll_duration=self.config.get("scroll_duration", 0.5),
            drag_duration=self.config.get("drag_duration", 0.3),
        )
        
        self.screenshot_capture = ScreenshotCapture(
            quality=self.config.get("screenshot_quality", 95),
            format=self.config.get("screenshot_format", "PNG"),
        )
        
        self.model_runner = ModelRunner()
        
        # Execution settings
        self.max_task_retries = self.config.get("max_task_retries", 3)
        self.max_command_retries = self.config.get("max_command_retries", 3)
        self.command_timeout = self.config.get("command_timeout", 30)
        self.task_timeout = self.config.get("task_timeout", 300)  # 5 minutes per task
        
        self.logger.info("Two-phase execution engine initialized")
    
    def execute_instruction(self, instruction: str) -> ExecutionContext:
        """Execute user instruction using two-phase approach"""
        self.logger.info(f"Starting two-phase execution for instruction: {instruction}")
        
        # Initialize execution context
        context = ExecutionContext(
            phase=ExecutionPhase.TASK_GENERATION,
            metadata={"instruction": instruction}
        )
        
        try:
            # Phase 1: Task List Generation
            context = self._execute_phase_1(context, instruction)
            
            # Phase 2: Sequential Task Execution
            context = self._execute_phase_2(context)
            
            # Mark as completed
            context.phase = ExecutionPhase.COMPLETED
            context.end_time = time.time()
            
            self.logger.info(
                "Two-phase execution completed successfully",
                total_tasks=len(context.task_list.tasks) if context.task_list else 0,
                executed_commands=len(context.executed_commands),
                duration=context.end_time - context.start_time
            )
            
            return context
            
        except Exception as e:
            context.phase = ExecutionPhase.FAILED
            context.error = str(e)
            context.end_time = time.time()
            
            self.logger.error(f"Two-phase execution failed: {e}")
            raise ExecutionError(f"Two-phase execution failed: {e}")
    
    def _execute_phase_1(self, context: ExecutionContext, instruction: str) -> ExecutionContext:
        """Phase 1: Task List Generation"""
        self.logger.info("Starting Phase 1: Task List Generation")
        
        try:
            # Capture current screen
            screenshot_data, screenshot_metadata = self.screenshot_capture.capture_screenshot()
            context.current_screenshot = screenshot_data
            context.metadata["screenshot_metadata"] = screenshot_metadata
            
            # Generate task list using AI
            self.logger.info("Generating task list with AI")
            response = self.model_runner.generate_tasks(instruction, screenshot_data)
            
            if not response.success:
                raise TaskGenerationError(f"Task generation failed: {response.error}")
            
            # Parse task list from AI response
            task_list = self._parse_task_list_response(response.content, instruction)
            context.task_list = task_list
            
            self.logger.info(
                "Phase 1 completed successfully",
                task_count=len(task_list.tasks),
                generation_time=task_list.generation_time,
            )
            
            # Transition to Phase 2
            context.phase = ExecutionPhase.TASK_EXECUTION
            context.current_task_index = 0
            
            return context
            
        except Exception as e:
            self.logger.error(f"Phase 1 failed: {e}")
            raise ExecutionError(f"Task generation phase failed: {e}")
    
    def _execute_phase_2(self, context: ExecutionContext) -> ExecutionContext:
        """Phase 2: Sequential Task Execution with context preservation"""
        self.logger.info("Starting Phase 2: Sequential Task Execution")
        
        if not context.task_list or not context.task_list.tasks:
            raise ValidationError("No tasks to execute", "task_list", context.task_list)
        
        try:
            # Execute each task sequentially
            for task_index, task_description in enumerate(context.task_list.tasks):
                task_start_time = time.time()
                self.logger.info(f"Executing task {task_index + 1}: {task_description}")
                
                # Update context
                context.current_task_index = task_index
                
                # Execute task with command generation loop
                success = self._execute_task_with_command_loop(context, task_description)
                
                # Log task execution completion
                task_duration = time.time() - task_start_time
                commands_executed = len([cmd for cmd in context.executed_commands if cmd])
                self.logger.log_task_execution(
                    task_index=task_index + 1,
                    task_description=task_description,
                    success=success,
                    commands_executed=commands_executed,
                    duration=task_duration
                )
                
                if not success:
                    self.logger.warning(f"Task {task_index + 1} failed, continuing to next task")
                
                # Small delay between tasks
                time.sleep(0.5)
            
            self.logger.info("Phase 2 completed successfully")
            return context
            
        except Exception as e:
            self.logger.error(f"Phase 2 failed: {e}")
            raise ExecutionError(f"Task execution phase failed: {e}")
    
    def _execute_task_with_command_loop(self, context: ExecutionContext, task_description: str) -> bool:
        """Execute a single task using command generation loop"""
        task_start_time = time.time()
        command_count = 0
        max_commands_per_task = 10  # Safety limit
        
        while command_count < max_commands_per_task:
            # Capture current screenshot
            screenshot_data, _ = self.screenshot_capture.capture_screenshot()
            
            # Generate command using AI with context preservation
            self.logger.debug(f"Generating command for task: {task_description}")
            response = self.model_runner.parse_command(
                task_description,
                screenshot_data,
                context={"task_description": task_description},
                previous_screenshot=context.previous_screenshot,
                previous_command=context.previous_command
            )
            
            if not response.success:
                self.logger.error(f"Command generation failed: {response.error}")
                return False
            
            # Parse command
            command_text = response.content.strip()
            
            # Log command generation with enhanced details
            self.logger.log_command_generation(
                task_description=task_description,
                command=command_text,
                success=True,
                model=response.model,
                latency=response.latency
            )
            
            # Check for END command
            if command_text.upper() == "END":
                self.logger.info("Received END command, task completed")
                break
            
            # Check for REBUILD command
            if command_text.upper() == "REBUILD":
                self.logger.info("Received REBUILD command, triggering self-repair process")
                return self._handle_rebuild(context, task_description)
            
            # Execute the command
            success = self._execute_single_command(command_text, context)
            
            if not success:
                self.logger.warning(f"Command execution failed: {command_text}")
                # Continue trying with next command
            
            # Update context for next iteration
            context.previous_screenshot = context.current_screenshot
            context.current_screenshot = screenshot_data
            context.previous_command = command_text
            context.executed_commands.append(command_text)
            command_count += 1
            
            # Check timeout
            if time.time() - task_start_time > self.task_timeout:
                self.logger.error(f"Task timeout after {self.task_timeout} seconds")
                return False
        
        return command_count > 0
    
    def _execute_single_command(self, command_text: str, context: ExecutionContext) -> bool:
        """Execute a single command"""
        try:
            self.logger.info(f"Executing command: {command_text}")
            
            # Parse command using command parser
            from .command_parser import CommandParser
            parser = CommandParser()
            parsed_command = parser.parse_command(command_text, context.current_screenshot)
            
            # Execute the parsed command
            result = self._execute_parsed_command(parsed_command)
            
            if result.success:
                self.logger.info(f"Command executed successfully: {command_text}")
                return True
            else:
                self.logger.error(f"Command execution failed: {command_text}, error: {result.error}")
                return False
                
        except Exception as e:
            self.logger.error(f"Command execution error: {command_text}, error: {e}")
            return False
    
    def _execute_parsed_command(self, command: ParsedCommand) -> AutomationResult:
        """Execute a parsed command"""
        try:
            if command.type == CommandType.CLICK:
                coords = command.parameters["coordinates"]
                return self.gui_automation.click(coords.x, coords.y)
                
            elif command.type == CommandType.DOUBLE_CLICK:
                coords = command.parameters["coordinates"]
                return self.gui_automation.double_click(coords.x, coords.y)
                
            elif command.type == CommandType.RIGHT_CLICK:
                coords = command.parameters["coordinates"]
                return self.gui_automation.right_click(coords.x, coords.y)
                
            elif command.type == CommandType.TEXT:
                text = command.parameters["text"]
                return self.gui_automation.type_text(text)
                
            elif command.type == CommandType.KEY:
                keys = command.parameters["keys"]
                return self.gui_automation.press_keys("+".join(keys) if isinstance(keys, list) else keys)
                
            elif command.type == CommandType.DRAG:
                start = command.parameters["start"]
                end = command.parameters["end"]
                return self.gui_automation.drag(start.x, start.y, end.x, end.y)
                
            elif command.type == CommandType.SCROLL:
                direction = command.parameters["direction"]
                amount = command.parameters["amount"]
                return self.gui_automation.scroll(direction, amount)
                
            elif command.type == CommandType.END:
                # END command - no action needed
                return AutomationResult(
                    success=True,
                    action="end",
                    duration=0.0,
                    method="builtin",
                )
                
            elif command.type == CommandType.REBUILD:
                # REBUILD command - trigger self-repair process
                self.logger.info("REBUILD command executed, triggering self-repair")
                return AutomationResult(
                    success=True,
                    action="rebuild",
                    duration=0.0,
                    method="builtin",
                )
                
            else:
                raise ExecutionError(f"Unsupported command type: {command.type}")
                
        except Exception as e:
            return AutomationResult(
                success=False,
                action="command_execution",
                duration=0.0,
                method="error",
                error=str(e),
            )
    
    
    def _parse_task_list_response(self, response_content: str, instruction: str) -> TaskList:
        """Parse AI response into TaskList"""
        try:
            import re
            
            # Extract numbered tasks
            tasks = []
            lines = response_content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Match numbered patterns (1., 1), etc.)
                match = re.match(r'^\d+[\.\)]\s*(.+)$', line)
                if match:
                    task_text = match.group(1).strip()
                    if task_text:
                        tasks.append(task_text)
            
            if not tasks:
                raise TaskGenerationError("No valid tasks found in AI response")
            
            return TaskList(
                tasks=tasks,
                instruction=instruction,
                generation_time=time.time(),
            )
            
        except Exception as e:
            raise TaskGenerationError(f"Failed to parse task list response: {e}")
    
    def _handle_rebuild(self, context: ExecutionContext, failed_task_description: str) -> bool:
        """Handle REBUILD command by triggering self-repair process"""
        rebuild_start_time = time.time()
        
        # Check for infinite loop protection
        rebuild_count = context.metadata.get("rebuild_count", 0)
        max_rebuilds = self.config.get("max_rebuilds_per_session", 3)
        
        if rebuild_count >= max_rebuilds:
            self.logger.error(
                f"Maximum rebuild limit reached ({max_rebuilds}), stopping execution",
                rebuild_count=rebuild_count,
                failed_task=failed_task_description
            )
            context.error = f"Maximum rebuild limit ({max_rebuilds}) exceeded"
            return False
        
        # Increment rebuild counter
        context.metadata["rebuild_count"] = rebuild_count + 1
        
        # Get original instruction from context
        original_instruction = context.metadata.get("instruction", "")
        original_task_list = context.task_list.tasks if context.task_list else []
        execution_history = context.executed_commands
        
        # Log rebuild start with comprehensive context
        self.logger.log_rebuild_start(
            original_instruction=original_instruction,
            original_task_count=len(original_task_list),
            execution_history_count=len(execution_history),
            failed_task=failed_task_description
        )
        
        try:
            # Capture current screenshot for rebuild analysis
            current_screenshot, _ = self.screenshot_capture.capture_screenshot()
            
            # Generate revised task list using rebuild planning
            rebuild_response = self.model_runner.generate_rebuild_plan(
                original_instruction=original_instruction,
                original_task_list=original_task_list,
                execution_history=execution_history,
                current_screenshot=current_screenshot
            )
            
            if not rebuild_response.success:
                rebuild_duration = time.time() - rebuild_start_time
                self.logger.log_rebuild_failure(
                    error=rebuild_response.error,
                    rebuild_duration=rebuild_duration
                )
                return False
            
            # Parse the revised task list
            revised_task_list = self._parse_task_list_response(rebuild_response.content, original_instruction)
            
            # Update context with new task list
            context.task_list = revised_task_list
            context.current_task_index = 0
            context.metadata["rebuild_triggered"] = True
            context.metadata["rebuild_time"] = time.time()
            context.metadata["failed_task"] = failed_task_description
            
            # Log successful rebuild
            rebuild_duration = time.time() - rebuild_start_time
            self.logger.log_rebuild_success(
                new_task_count=len(revised_task_list.tasks),
                rebuild_duration=rebuild_duration
            )
            
            # Restart execution with new task list from current position
            return self._execute_phase_2(context)
            
        except Exception as e:
            rebuild_duration = time.time() - rebuild_start_time
            self.logger.log_rebuild_failure(
                error=str(e),
                rebuild_duration=rebuild_duration
            )
            context.error = f"Rebuild failed: {e}"
            return False
