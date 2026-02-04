#!/usr/bin/env python3
"""
Test script to verify dependency installer works across platforms
"""

import sys
import subprocess
import platform
from pathlib import Path

def test_installer():
    """Test the dependency installer"""
    print(f"Testing dependency installer on {platform.system()}...")
    
    project_root = Path(__file__).parent
    minimal_checker = project_root / "minimal_dependency_checker.py"
    
    if not minimal_checker.exists():
        print("ERROR: minimal_dependency_checker.py not found")
        return False
    
    try:
        # Test the dependency checker
        result = subprocess.run(
            [sys.executable, str(minimal_checker)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("SUCCESS: Dependency installer test passed")
            return True
        else:
            print(f"FAILED: Dependency installer test failed")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("FAILED: Dependency installer test timed out")
        return False
    except Exception as e:
        print(f"FAILED: Dependency installer test error: {e}")
        return False

def test_venv_deletion():
    """Test virtual environment deletion"""
    print("Testing virtual environment deletion...")
    
    project_root = Path(__file__).parent
    
    try:
        # Import the checker
        sys.path.insert(0, str(project_root))
        from minimal_dependency_checker import MinimalDependencyChecker
        
        checker = MinimalDependencyChecker(project_root)
        success, message = checker.delete_all_virtual_environments()
        
        print(f"Venv deletion result: {message}")
        return success
        
    except Exception as e:
        print(f"FAILED: Venv deletion test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("VEXIS-1 Dependency Installer Test Suite")
    print("=" * 60)
    
    # Test 1: Basic installer functionality
    test1_passed = test_installer()
    
    # Test 2: Virtual environment deletion
    test2_passed = test_venv_deletion()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"Installer functionality: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Venv deletion: {'PASS' if test2_passed else 'FAIL'}")
    
    overall_success = test1_passed and test2_passed
    print(f"Overall: {'PASS' if overall_success else 'FAIL'}")
    
    sys.exit(0 if overall_success else 1)
