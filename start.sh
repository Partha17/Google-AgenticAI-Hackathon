#!/bin/bash
# Enhanced wrapper for Financial Multi-Agent System startup with auto-setup

echo "🚀 Enhanced Financial Multi-Agent System Startup"
echo "=================================================="

# Change to script directory
cd "$(dirname "$0")"

# Check if this is a setup-only or force-reinstall operation
if [[ "$*" == *"--setup-only"* ]] || [[ "$*" == *"--force-reinstall"* ]]; then
    echo "🔧 Environment setup mode..."
    # Don't try to activate venv for setup operations
    python start_system.py "$@"
    exit $?
fi

# For normal operations, activate venv if it exists
if [ -d "venv" ]; then
    echo "📦 Using existing virtual environment..."
    source venv/bin/activate
else
    echo "📦 Virtual environment will be created automatically..."
fi

# Run the system startup script
python start_system.py "$@" 