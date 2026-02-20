#!/usr/bin/env python3
"""
Interactive menu system with arrow key navigation and colored output
"""

import sys
import tty
import termios
from typing import List, Tuple, Optional

class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_BLUE = '\033[104m'

class MenuItem:
    """Represents a single menu item"""
    def __init__(self, title: str, description: str = "", value: str = None, icon: str = ""):
        self.title = title
        self.description = description
        self.value = value if value is not None else title
        self.icon = icon

class InteractiveMenu:
    """Interactive menu with arrow key navigation"""
    
    def __init__(self, title: str, subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        self.items: List[MenuItem] = []
        self.current_selection = 0
        self.show_current = False
        self.current_value = None
        
    def add_item(self, title: str, description: str = "", value: str = None, icon: str = ""):
        """Add a menu item"""
        self.items.append(MenuItem(title, description, value, icon))
        
    def set_current_selection(self, value: str):
        """Set the current/preferred value"""
        self.current_value = value
        self.show_current = True
        # Find and set the current selection index
        for i, item in enumerate(self.items):
            if item.value == value:
                self.current_selection = i
                break
    
    def _get_key(self) -> str:
        """Get a single keypress from the user"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle arrow keys (escape sequences)
            if ch == '\x1b':  # ESC
                ch += sys.stdin.read(2)
                if ch == '\x1b[A':  # Up arrow
                    return 'UP'
                elif ch == '\x1b[B':  # Down arrow
                    return 'DOWN'
                elif ch == '\x1b[C':  # Right arrow
                    return 'RIGHT'
                elif ch == '\x1b[D':  # Left arrow
                    return 'LEFT'
            
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _render_menu(self):
        """Render the menu with colors"""
        # Clear screen and move cursor to top
        print('\033[2J\033[H', end='')
        
        # Title
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{self.title}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'=' * len(self.title)}{Colors.RESET}")
        print()
        
        if self.subtitle:
            print(f"{Colors.CYAN}{self.subtitle}{Colors.RESET}")
            print()
        
        # Show current preference if available
        if self.show_current and self.current_value:
            for item in self.items:
                if item.value == self.current_value:
                    print(f"{Colors.BRIGHT_GREEN}Current preference: {item.icon} {item.title}{Colors.RESET}")
                    break
            print()
        
        # Menu items
        for i, item in enumerate(self.items):
            if i == self.current_selection:
                # Selected item - highlight with background
                print(f"{Colors.BG_BRIGHT_BLUE}{Colors.BRIGHT_WHITE}  ▶ {item.icon} {item.title}{Colors.RESET}")
                if item.description:
                    print(f"{Colors.BG_BRIGHT_BLUE}{Colors.BRIGHT_WHITE}     {item.description}{Colors.RESET}")
            else:
                # Normal item
                print(f"  {Colors.BRIGHT_BLACK}{item.icon}{Colors.RESET} {Colors.WHITE}{item.title}{Colors.RESET}")
                if item.description:
                    print(f"    {Colors.BRIGHT_BLACK}{item.description}{Colors.RESET}")
            print()
        
        # Instructions
        print(f"{Colors.BRIGHT_YELLOW}Instructions:{Colors.RESET}")
        print(f"{Colors.CYAN}  ↑/↓  Navigate menu{Colors.RESET}")
        print(f"{Colors.CYAN}  Enter  Select option{Colors.RESET}")
        print(f"{Colors.CYAN}  q/Ctrl+C  Cancel{Colors.RESET}")
    
    def show(self) -> Optional[str]:
        """Display the interactive menu and return selected value"""
        if not self.items:
            return None
        
        while True:
            self._render_menu()
            
            try:
                key = self._get_key()
                
                if key == 'UP':
                    self.current_selection = (self.current_selection - 1) % len(self.items)
                elif key == 'DOWN':
                    self.current_selection = (self.current_selection + 1) % len(self.items)
                elif key in ('\r', '\n'):  # Enter
                    selected_item = self.items[self.current_selection]
                    print(f"\n{Colors.BRIGHT_GREEN}✓ Selected: {selected_item.icon} {selected_item.title}{Colors.RESET}")
                    return selected_item.value
                elif key.lower() == 'q':
                    print(f"\n{Colors.BRIGHT_YELLOW}Operation cancelled{Colors.RESET}")
                    return None
                elif key == '\x03':  # Ctrl+C
                    print(f"\n{Colors.BRIGHT_YELLOW}Operation cancelled{Colors.RESET}")
                    return None
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.BRIGHT_YELLOW}Operation cancelled{Colors.RESET}")
                return None
            except Exception as e:
                print(f"Error reading input: {e}")
                return None

def confirm_dialog(message: str, default: bool = False) -> bool:
    """Show a confirmation dialog"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{message}{Colors.RESET}")
    print(f"{Colors.CYAN}[Y/n]{' (default: Yes)' if default else ' (default: No)'}{Colors.RESET}")
    
    try:
        response = input().strip().lower()
        if not response:
            return default
        return response.startswith('y')
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}Operation cancelled{Colors.RESET}")
        return False

def info_message(message: str, color: str = Colors.BRIGHT_CYAN):
    """Display an info message with color"""
    print(f"\n{color}{message}{Colors.RESET}")

def success_message(message: str):
    """Display a success message"""
    print(f"{Colors.BRIGHT_GREEN}✓ {message}{Colors.RESET}")

def error_message(message: str):
    """Display an error message"""
    print(f"{Colors.BRIGHT_RED}✗ {message}{Colors.RESET}")

def warning_message(message: str):
    """Display a warning message"""
    print(f"{Colors.BRIGHT_YELLOW}⚠ {message}{Colors.RESET}")
