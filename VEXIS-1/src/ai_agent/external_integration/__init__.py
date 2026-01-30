"""
External Integration Layer for AI Agent System
Vision API client and model runner for AI communication
"""

from .vision_api_client import VisionAPIClient
from .model_runner import ModelRunner

__all__ = [
    "VisionAPIClient",
    "ModelRunner",
]
