"""
Platform Abstraction Layer for AI Agent System
Cross-platform screenshot capture and GUI automation
"""

from .screenshot_capture import ScreenshotCapture
from .gui_automation import GUIAutomation
from .platform_detector import PlatformDetector

__all__ = [
    "ScreenshotCapture",
    "GUIAutomation", 
    "PlatformDetector",
]
