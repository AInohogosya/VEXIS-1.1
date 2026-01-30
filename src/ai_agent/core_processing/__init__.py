"""
Core Processing Layer for AI Agent System
2-Phase Architecture: Task generation and execution engine
"""

from .command_parser import CommandParser
from .two_phase_engine import TwoPhaseEngine

__all__ = [
    "CommandParser", 
    "TwoPhaseEngine",
]
