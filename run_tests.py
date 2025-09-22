#!/usr/bin/env python3
"""Test runner script for afrim-py."""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"✅ {description} completed successfully")
        return True


def main():
    """Run the complete test suite."""
    print("🧪 Running afrim-py test suite")
    print("=" * 60)
    
    # Check if we're in a virtual environment
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Not running in a virtual environment")
        print("Consider running: source .venv/bin/activate")
    
    success = True
    
    # Run unit tests
    success &= run_command(
        "python -m pytest tests/ -v",
        "Running unit tests"
    )
    
    # Run tests with coverage
    success &= run_command(
        "python -m pytest tests/ --cov=afrim_py --cov-report=term-missing --cov-report=html",
        "Running tests with coverage analysis"
    )
    
    # Run only integration tests
    success &= run_command(
        "python -m pytest tests/test_integration.py -v",
        "Running integration tests"
    )
    
    # Quick smoke test
    success &= run_command(
        'python -c "from afrim_py import Preprocessor, Translator, convert_toml_to_json; print(\\"✅ Module imports successful\\")"',
        "Quick import smoke test"
    )
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed!")
        print("📊 Coverage report saved to htmlcov/index.html")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
