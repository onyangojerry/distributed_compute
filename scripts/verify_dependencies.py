#!/usr/bin/env python3
"""
Dependency verification script for the distributed file storage system
"""
import subprocess
import sys
import json
from pathlib import Path


def check_python_dependencies():
    """Check if all Python dependencies are available"""
    print("🐍 Checking Python dependencies...")
    
    # Check production dependencies
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "check"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All Python dependencies are compatible")
        else:
            print(f"❌ Dependency conflicts found:\n{result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking Python dependencies: {e}")
        return False
    
    return True


def check_requirements_files():
    """Verify requirements files exist and are readable"""
    print("📋 Checking requirements files...")
    
    files = ["requirements.txt", "requirements-dev.txt"]
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"✅ {file} exists")
            try:
                with open(path) as f:
                    lines = len([line for line in f if line.strip() and not line.startswith('#')])
                    print(f"   📦 {lines} packages defined")
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
                return False
        else:
            print(f"❌ {file} not found")
            return False
    
    return True


def check_node_dependencies():
    """Check Node.js dependencies if web-ui exists"""
    print("🟢 Checking Node.js dependencies...")
    
    web_ui_path = Path("web-ui")
    if not web_ui_path.exists():
        print("ℹ️  No web-ui directory found, skipping Node.js checks")
        return True
    
    package_json = web_ui_path / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in web-ui")
        return False
    
    try:
        with open(package_json) as f:
            package_data = json.load(f)
            deps = len(package_data.get("dependencies", {}))
            dev_deps = len(package_data.get("devDependencies", {}))
            print(f"✅ package.json found")
            print(f"   📦 {deps} dependencies, {dev_deps} devDependencies")
    except Exception as e:
        print(f"❌ Error reading package.json: {e}")
        return False
    
    return True


def check_test_setup():
    """Check if test infrastructure is properly set up"""
    print("🧪 Checking test setup...")
    
    test_dirs = ["tests", "tests/unit", "tests/load"]
    for test_dir in test_dirs:
        path = Path(test_dir)
        if path.exists():
            print(f"✅ {test_dir}/ exists")
        else:
            print(f"❌ {test_dir}/ not found")
            return False
    
    # Check for key test files
    test_files = [
        "tests/__init__.py",
        "tests/unit/test_basic.py", 
        "tests/load/upload_test.py"
    ]
    
    for test_file in test_files:
        path = Path(test_file)
        if path.exists():
            print(f"✅ {test_file} exists")
        else:
            print(f"❌ {test_file} not found")
            return False
    
    return True


def check_config_files():
    """Check configuration files"""
    print("⚙️  Checking configuration files...")
    
    config_files = [
        "pyproject.toml",
        ".flake8", 
        ".gitignore",
        "Makefile",
        "docker-compose.yml"
    ]
    
    for config_file in config_files:
        path = Path(config_file)
        if path.exists():
            print(f"✅ {config_file} exists")
        else:
            print(f"❌ {config_file} not found")
            return False
    
    return True


def main():
    """Run all dependency checks"""
    print("🚀 Starting dependency verification for distributed file storage system\n")
    
    checks = [
        check_requirements_files,
        check_python_dependencies,
        check_node_dependencies,
        check_test_setup,
        check_config_files,
    ]
    
    all_passed = True
    for check in checks:
        result = check()
        if not result:
            all_passed = False
        print()  # Empty line between checks
    
    if all_passed:
        print("🎉 All dependency checks passed! System ready for deployment.")
        return 0
    else:
        print("❌ Some dependency checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())