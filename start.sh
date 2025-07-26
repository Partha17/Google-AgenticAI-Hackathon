#!/bin/bash
# Enhanced wrapper for Financial Multi-Agent System startup with MCP server verification

echo "🚀 Enhanced Financial Multi-Agent System Startup"
echo "=================================================="

# Change to script directory
cd "$(dirname "$0")"

# Function to check if Fi MCP server is running
check_mcp_server() {
    local max_attempts=10
    local attempt=1
    
    echo "🔍 Checking Fi MCP Server status..."
    
    while [ $attempt -le $max_attempts ]; do
        # Check if port 8080 is open
        if command -v nc >/dev/null 2>&1; then
            # Use netcat if available
            if nc -z localhost 8080 2>/dev/null; then
                echo "✅ Fi MCP Server detected on port 8080"
                return 0
            fi
        elif command -v curl >/dev/null 2>&1; then
            # Use curl if available
            if curl -s --connect-timeout 2 http://localhost:8080 >/dev/null 2>&1; then
                echo "✅ Fi MCP Server responding on port 8080"
                return 0
            fi
        else
            # Fallback: check if process exists
            if pgrep -f "go run main.go" >/dev/null 2>&1; then
                echo "✅ Fi MCP Server process detected"
                return 0
            fi
        fi
        
        if [ $attempt -eq 1 ]; then
            echo "⏳ Waiting for Fi MCP Server to start..."
        fi
        
        sleep 2
        ((attempt++))
    done
    
    echo "⚠️  Fi MCP Server not detected (will be started automatically)"
    return 1
}

# Function to verify Go installation
check_go_installation() {
    if ! command -v go >/dev/null 2>&1; then
        echo "❌ Go not found! Fi MCP Server requires Go."
        echo "📥 Install Go:"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "   macOS: brew install go"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "   Ubuntu/Debian: sudo apt install golang-go"
            echo "   CentOS/RHEL: sudo yum install golang"
        fi
        echo "   Or download from: https://golang.org/dl/"
        return 1
    fi
    echo "✅ Go found: $(go version)"
    return 0
}

# Check if this is a setup-only or cleanup-only operation (skip MCP checks)
if [[ "$*" == *"--setup-only"* ]] || [[ "$*" == *"--cleanup-only"* ]] || [[ "$*" == *"--force-reinstall"* ]]; then
    echo "🔧 Environment setup/cleanup mode..."
    # Don't try to activate venv for setup operations
    python start_system.py "$@"
    exit $?
fi

# For normal system startup, check prerequisites
echo "🔍 Verifying system prerequisites..."

# Check Go installation (required for Fi MCP server)
if ! check_go_installation; then
    echo "❌ Cannot start system without Go. Please install Go first."
    exit 1
fi

# Check if Fi MCP Server directory exists
if [ ! -d "fi-mcp-server" ]; then
    echo "❌ Fi MCP Server directory not found!"
    echo "   Make sure you're in the correct project directory."
    exit 1
fi

# For normal operations, activate venv if it exists
if [ -d "venv" ]; then
    echo "📦 Using existing virtual environment..."
    source venv/bin/activate
else
    echo "📦 Virtual environment will be created automatically..."
fi

# Run the system startup script
echo "🚀 Starting complete system..."
python start_system.py "$@"

# After startup, verify MCP server is running
startup_exit_code=$?

if [ $startup_exit_code -eq 0 ]; then
    echo ""
    echo "🔍 Final system verification..."
    
    # Give system a moment to fully start
    sleep 3
    
    # Verify Fi MCP Server is responsive
    if check_mcp_server; then
        echo ""
        echo "🎉 System startup completed successfully!"
        echo "📊 Dashboard: http://localhost:8501"
        echo "🔌 Fi MCP Server: http://localhost:8080"
        echo "🤖 ADK Agents: Running"
        echo ""
        echo "Press Ctrl+C to stop all services"
        echo "=================================================="
    else
        echo ""
        echo "⚠️  System started but Fi MCP Server verification failed"
        echo "   The system may still work, but financial data collection might be limited."
        echo "   Check the logs above for Fi MCP Server startup messages."
    fi
else
    echo ""
    echo "❌ System startup failed (exit code: $startup_exit_code)"
    echo "   Check the error messages above for troubleshooting guidance."
fi

exit $startup_exit_code 