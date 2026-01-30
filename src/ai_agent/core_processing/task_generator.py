"""
Task Generation Engine for AI Agent System
2-Phase Vision-Only Architecture: Phase 1 Task List Generation
"""

import re
import time
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..external_integration.model_runner import get_model_runner
from ..utils.exceptions import TaskGenerationError, ValidationError
from ..utils.logger import get_logger


@dataclass
class Task:
    """Individual task structure - matches specification"""
    description: str


@dataclass
class TaskList:
    """Task list structure - matches specification"""
    tasks: List[Task]
    instruction: str
    generation_time: float = 0.0


class TaskGenerator:
    """Task generation engine for 2-Phase Architecture"""
    
    def __init__(self):
        self.logger = get_logger("task_generator")
        self.model_runner = get_model_runner()
        self.logger.info("Task generator initialized for 2-Phase Architecture")
    
    
    def generate_tasks(self, instruction: str, screenshot: bytes, context: Optional[Dict[str, Any]] = None) -> TaskList:
        """Generate task list from instruction and screenshot using Gemini 3 Flash"""
        start_time = time.time()
        
        try:
            self.logger.info(
                "Starting Phase 1: Task List Generation",
                instruction=instruction,
                screenshot_size=len(screenshot),
            )
            
            # Validate inputs
            self._validate_inputs(instruction, screenshot)
            
            # Generate tasks using AI (Gemini 3 Flash)
            model_response = self.model_runner.generate_tasks(instruction, screenshot, context)
            
            if not model_response.success:
                raise TaskGenerationError(
                    f"AI task generation failed: {model_response.error}",
                    instruction=instruction
                )
            
            # Parse AI response into task list
            raw_tasks = self._parse_ai_response(model_response.content)
            
            # Create task objects
            tasks = self._create_task_objects(raw_tasks)
            
            # Create task list
            task_list = TaskList(
                tasks=tasks,
                instruction=instruction,
                generation_time=time.time() - start_time,
            )
            
            # Validate task list
            self._validate_task_list(task_list)
            
            self.logger.info(
                "Phase 1 Task Generation completed",
                task_count=len(tasks),
                generation_time=task_list.generation_time,
            )
            
            return task_list
            
        except Exception as e:
            self.logger.error(f"Task generation failed: {e}")
            raise TaskGenerationError(f"Failed to generate tasks: {e}", instruction=instruction)
    
    def _validate_inputs(self, instruction: str, screenshot: bytes):
        """Validate input parameters"""
        if not instruction or not instruction.strip():
            raise ValidationError("Instruction cannot be empty", "instruction", instruction)
        
        if len(instruction) > 1000:
            raise ValidationError("Instruction too long", "instruction", len(instruction))
        
        if not screenshot:
            raise ValidationError("Screenshot cannot be empty", "screenshot", len(screenshot))
        
        if len(screenshot) > 20 * 1024 * 1024:  # 20MB limit
            raise ValidationError("Screenshot too large", "screenshot", len(screenshot))
    
    def _parse_ai_response(self, ai_response: str) -> List[str]:
        """Parse AI response into task list"""
        try:
            # Clean response
            cleaned_response = ai_response.strip()
            
            # Extract numbered list
            tasks = []
            lines = cleaned_response.split('\n')
            
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
                elif re.match(r'^\d+\s+', line):
                    # Handle space-separated numbers
                    task_text = re.sub(r'^\d+\s+', '', line).strip()
                    if task_text:
                        tasks.append(task_text)
            
            # Validate task list
            if not tasks:
                raise TaskGenerationError("No valid tasks found in AI response")
            
            # Limit number of tasks based on complexity
            max_tasks = 15  # Hard limit for safety
            if len(tasks) > max_tasks:
                tasks = tasks[:max_tasks]
                self.logger.warning(f"Task list truncated to {max_tasks} tasks")
            
            return tasks
            
        except Exception as e:
            raise TaskGenerationError(f"Failed to parse AI response: {e}")
    
    def _create_task_objects(self, raw_tasks: List[str]) -> List[Task]:
        """Create task objects from raw task descriptions"""
        tasks = []
        
        for task_description in raw_tasks:
            # Create task object
            task = Task(description=task_description)
            tasks.append(task)
        
        return tasks
    
    def _validate_task_list(self, task_list: TaskList):
        """Validate generated task list"""
        if not task_list.tasks:
            raise ValidationError("Task list cannot be empty", "tasks", [])