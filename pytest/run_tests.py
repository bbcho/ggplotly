#!/usr/bin/env python3
"""
Test runner script for ggplotly library.
This script provides various options for running tests and generating reports.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_tests_with_pytest(test_dir="pytest", verbose=False, coverage=False, html_report=False, parallel=False):
    """
    Run tests using pytest with various options.
    
    Args:
        test_dir (str): Directory containing tests
        verbose (bool): Run tests in verbose mode
        coverage (bool): Generate coverage report
        html_report (bool): Generate HTML test report
        parallel (bool): Run tests in parallel
    """
    
    # Build pytest command
    cmd = ["python", "-m", "pytest", test_dir]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=ggplotly", "--cov-report=term-missing"])
        if html_report:
            cmd.extend(["--cov-report=html"])
    
    if html_report:
        cmd.extend(["--html=pytest/report.html", "--self-contained-html"])
    
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add additional useful options
    cmd.extend([
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings"  # Disable warnings for cleaner output
    ])
    
    print(f"Running tests with command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False

def run_specific_test_file(test_file, verbose=False):
    """
    Run tests from a specific test file.
    
    Args:
        test_file (str): Path to test file
        verbose (bool): Run tests in verbose mode
    """
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    cmd = ["python", "-m", "pytest", test_file]
    if verbose:
        cmd.append("-v")
    
    print(f"Running tests from: {test_file}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 60)
        print("✅ Tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False

def run_test_class(test_file, test_class, verbose=False):
    """
    Run tests from a specific test class.
    
    Args:
        test_file (str): Path to test file
        test_class (str): Name of test class
        verbose (bool): Run tests in verbose mode
    """
    cmd = ["python", "-m", "pytest", f"{test_file}::{test_class}"]
    if verbose:
        cmd.append("-v")
    
    print(f"Running test class: {test_class} from {test_file}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 60)
        print("✅ Tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False

def list_test_files():
    """List all available test files."""
    test_dir = Path("pytest")
    test_files = list(test_dir.glob("test_*.py"))
    
    print("Available test files:")
    print("=" * 30)
    for test_file in test_files:
        print(f"  {test_file.name}")
    
    print(f"\nTotal: {len(test_files)} test files")
    
    # Also list test categories
    print("\nTest Categories:")
    print("=" * 30)
    print("  • test_geoms.py - Geometry components")
    print("  • test_scales.py - Scale transformations")
    print("  • test_themes_and_coords.py - Themes and coordinate systems")
    print("  • test_facets_stats_utils.py - Faceting, stats, and utilities")
    print("  • test_error_handling.py - Error handling and edge cases")
    print("  • test_integration.py - Complex plot combinations")
    print("  • test_main.py - Basic functionality tests")

def check_test_environment():
    """Check if the test environment is properly set up."""
    print("Checking test environment...")
    
    # Check if pytest is available
    try:
        import pytest
        print(f"✅ pytest version: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return False
    
    # Check if required packages are available
    required_packages = ['pandas', 'plotly', 'numpy']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} not found")
            return False
    
    # Check if ggplotly can be imported
    try:
        sys.path.insert(0, os.path.abspath("."))
        import ggplotly
        print("✅ ggplotly can be imported")
    except ImportError as e:
        print(f"❌ ggplotly cannot be imported: {e}")
        return False
    
    print("✅ Test environment is ready!")
    return True

def main():
    """Main function to handle command line arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run ggplotly tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests in verbose mode")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")
    parser.add_argument("--html-report", "-r", action="store_true", help="Generate HTML test report")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel")
    parser.add_argument("--file", "-f", help="Run tests from specific file")
    parser.add_argument("--class", "-k", dest="test_class", help="Run tests from specific class")
    parser.add_argument("--list", "-l", action="store_true", help="List available test files")
    parser.add_argument("--check", action="store_true", help="Check test environment")
    
    args = parser.parse_args()
    
    if args.check:
        return check_test_environment()
    
    if args.list:
        list_test_files()
        return
    
    if args.file:
        if args.test_class:
            return run_test_class(args.file, args.test_class, args.verbose)
        else:
            return run_specific_test_file(args.file, args.verbose)
    
    # Default: run all tests
    return run_tests_with_pytest(
        verbose=args.verbose,
        coverage=args.coverage,
        html_report=args.html_report,
        parallel=args.parallel
    )

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

