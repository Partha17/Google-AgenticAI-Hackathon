#!/bin/bash
# Simple wrapper for Enhanced Financial Multi-Agent System startup

echo "🚀 Enhanced Financial Multi-Agent System Startup"
echo "=================================================="

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Run the system startup script
python start_system.py "$@" 