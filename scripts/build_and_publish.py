#!/usr/bin/env python3
"""
Build and publish script for just_facebook_mcp package.

This script automates the process of building and publishing
the package to PyPI.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    
    # Remove build directories
    dirs_to_remove = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_remove:
        run_command(f"rm -rf {dir_pattern}", check=False)


def run_tests():
    """Run tests before building."""
    print("Running tests...")
    try:
        run_command("uv run pytest", check=True)
        print("✅ All tests passed!")
    except subprocess.CalledProcessError:
        print("❌ Tests failed. Please fix tests before publishing.")
        sys.exit(1)


def run_linting():
    """Run code quality checks."""
    print("Running code quality checks...")
    
    try:
        # Format with black
        run_command("uv run black just_facebook_mcp/")
        print("✅ Code formatted with black")
        
        # Type checking with mypy
        run_command("uv run mypy just_facebook_mcp/")
        print("✅ Type checking passed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Code quality checks failed: {e}")
        choice = input("Continue anyway? (y/N): ")
        if choice.lower() != 'y':
            sys.exit(1)


def build_package():
    """Build the package."""
    print("Building package...")
    run_command("uv build")
    print("✅ Package built successfully!")


def check_package():
    """Check the built package."""
    print("Checking package...")
    run_command("uv run twine check dist/*")
    print("✅ Package check passed!")


def publish_to_test_pypi():
    """Publish to Test PyPI."""
    print("Publishing to Test PyPI...")
    run_command("uv run twine upload --repository testpypi dist/*")
    print("✅ Published to Test PyPI!")


def publish_to_pypi():
    """Publish to PyPI."""
    print("Publishing to PyPI...")
    run_command("uv run twine upload dist/*")
    print("✅ Published to PyPI!")


def main():
    """Main function."""
    print("🚀 Building and publishing just_facebook_mcp package")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")
    
    # Clean previous builds
    clean_build()
    
    # Run quality checks
    run_linting()
    
    # Run tests (if available)
    if Path("tests").exists():
        run_tests()
    else:
        print("⚠️  No tests directory found, skipping tests")
    
    # Build package
    build_package()
    
    # Check package
    check_package()
    
    # Ask user where to publish
    print("\nWhere would you like to publish?")
    print("1. Test PyPI (recommended for first time)")
    print("2. PyPI (production)")
    print("3. Skip publishing")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        publish_to_test_pypi()
    elif choice == "2":
        confirm = input("Are you sure you want to publish to PyPI? (yes/no): ")
        if confirm.lower() == "yes":
            publish_to_pypi()
        else:
            print("Publishing cancelled.")
    elif choice == "3":
        print("Skipping publishing. Package is ready in dist/ directory.")
    else:
        print("Invalid choice. Skipping publishing.")
    
    print("\n🎉 Build process completed!")


if __name__ == "__main__":
    main() 