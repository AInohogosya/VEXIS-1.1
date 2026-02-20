#!/usr/bin/env python3
"""
Test script for the new interactive menu system
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from src.ai_agent.utils.interactive_menu import (
    InteractiveMenu, Colors, success_message, info_message
)

def test_provider_selection():
    """Test the provider selection menu"""
    menu = InteractiveMenu(
        "VEXIS-1.1 AI Agent - Model Provider Selection",
        "Choose your AI model provider:"
    )
    
    menu.add_item(
        "Ollama (Local Models)",
        "Run models locally • Privacy-focused • Requires Ollama installation",
        "ollama",
        "🦊"
    )
    
    menu.add_item(
        "Google Official API (Gemini)",
        "Cloud-based AI • No local setup • Requires Google API key",
        "google",
        "🌐"
    )
    
    # Set a current preference for demonstration
    menu.set_current_selection("google")
    
    # Show the menu
    selected_provider = menu.show()
    
    if selected_provider:
        success_message(f"You selected: {selected_provider}")
        return selected_provider
    else:
        info_message("Selection cancelled")
        return None

def test_model_selection():
    """Test the Google model selection menu"""
    menu = InteractiveMenu(
        "Google Gemini Model Selection",
        "Choose your preferred Gemini model:"
    )
    
    menu.add_item(
        "Gemini 3 Flash",
        "Fast and efficient • Cost-effective for most tasks • Quick response times",
        "gemini-3-flash-preview",
        "🚀"
    )
    
    menu.add_item(
        "Gemini 3.1 Pro",
        "Advanced reasoning • Best for complex problem-solving • Superior performance",
        "gemini-3.1-pro-preview",
        "🧠"
    )
    
    # Set current selection
    menu.set_current_selection("gemini-3-flash-preview")
    
    # Show the menu
    selected_model = menu.show()
    
    if selected_model:
        success_message(f"You selected: {selected_model}")
        return selected_model
    else:
        info_message("Selection cancelled")
        return None

def main():
    """Test the interactive menu system"""
    print(f"{Colors.BRIGHT_CYAN}Testing Interactive Menu System{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 40}{Colors.RESET}")
    print()
    
    info_message("This is a demonstration of the new interactive menu system.")
    info_message("Use arrow keys to navigate and Enter to select.")
    print()
    
    # Test provider selection
    print(f"{Colors.BOLD}{Colors.YELLOW}Test 1: Provider Selection{Colors.RESET}")
    print()
    provider = test_provider_selection()
    print()
    
    if provider:
        # Test model selection
        print(f"{Colors.BOLD}{Colors.YELLOW}Test 2: Model Selection{Colors.RESET}")
        print()
        model = test_model_selection()
        print()
        
        if model:
            success_message("Interactive menu test completed successfully!")
        else:
            info_message("Model selection cancelled")
    else:
        info_message("Provider selection cancelled")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}Test interrupted{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}Error: {e}{Colors.RESET}")
