#!/bin/bash

# 🛑 Agentic AI Financial Insights System - Stop Script
# This script stops all running components

echo "🛑 Stopping Agentic AI Financial Insights System..."

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local service_name=$2
    echo "🔍 Stopping $service_name on port $port..."
    
    if lsof -ti:$port > /dev/null 2>&1; then
        lsof -ti:$port | xargs kill -9
        echo "✅ $service_name stopped"
    else
        echo "ℹ️  $service_name was not running"
    fi
}

# Stop services by port
kill_port 8080 "MCP Server"
kill_port 8501 "Dashboard (8501)"
kill_port 8502 "Dashboard (8502)"

# Stop services by process name
echo ""
echo "🔍 Stopping background processes..."

if pkill -f "go run" 2>/dev/null; then
    echo "✅ Go processes stopped"
else
    echo "ℹ️  No Go processes found"
fi

if pkill -f "python.*main.py" 2>/dev/null; then
    echo "✅ Python main processes stopped"
else
    echo "ℹ️  No Python main processes found"
fi

if pkill -f "streamlit" 2>/dev/null; then
    echo "✅ Streamlit processes stopped"
else
    echo "ℹ️  No Streamlit processes found"
fi

# Clean up log files (optional)
echo ""
read -p "🗑️  Do you want to clean up log files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f mcp_server.log agentic_ai_startup.log dashboard.log
    echo "✅ Log files cleaned up"
fi

echo ""
echo "✅ ==================================="
echo "✅ ALL SERVICES STOPPED"
echo "✅ ==================================="
echo ""
echo "🚀 To restart the system: ./start_system.sh" 