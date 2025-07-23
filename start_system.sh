#!/bin/bash

# 🚀 Agentic AI Financial Insights System - Startup Script
# This script starts all components: MCP server, Python app, and dashboard

echo "🚀 Starting Agentic AI Financial Insights System..."

# Function to check if port is in use and kill processes
kill_port() {
    local port=$1
    echo "🔍 Checking port $port..."
    if lsof -ti:$port > /dev/null 2>&1; then
        echo "⚠️  Port $port is in use. Killing existing processes..."
        lsof -ti:$port | xargs kill -9
        sleep 2
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s $url > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start after $max_attempts attempts"
    return 1
}

# Step 1: Kill any existing processes
echo ""
echo "📋 Step 1: Cleaning up existing processes..."
kill_port 8080
kill_port 8501
kill_port 8502
pkill -f "go run" 2>/dev/null || true
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "streamlit" 2>/dev/null || true

# Step 2: Start MCP Server
echo ""
echo "📋 Step 2: Starting Fi MCP Server..."
cd fi-mcp-server
echo "🔧 Installing Go dependencies..."
go mod tidy
echo "🌐 Starting MCP server on port 8080..."
FI_MCP_PORT=8080 go run . > ../mcp_server.log 2>&1 &
MCP_PID=$!
cd ..

# Wait for MCP server to be ready
if wait_for_service "http://localhost:8080/mcp/stream" "MCP Server"; then
    echo "✅ MCP Server started successfully (PID: $MCP_PID)"
else
    echo "❌ Failed to start MCP Server"
    exit 1
fi

# Step 3: Setup Python Environment and Start App
echo ""
echo "📋 Step 3: Starting Python Application..."
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "🧠 Starting AI application with real Fi MCP data..."
MCP_SERVER_URL=http://localhost:8080 python3 main.py start > agentic_ai_startup.log 2>&1 &
PYTHON_PID=$!

# Wait a moment for Python app to initialize
sleep 5

# Check if Python app is running
if ps -p $PYTHON_PID > /dev/null; then
    echo "✅ Python Application started successfully (PID: $PYTHON_PID)"
else
    echo "❌ Failed to start Python Application"
    exit 1
fi

# Step 4: Start Dashboard
echo ""
echo "📋 Step 4: Starting Streamlit Dashboard..."
python3 main.py dashboard > dashboard.log 2>&1 &
DASHBOARD_PID=$!

# Wait for dashboard to be ready
sleep 8
if wait_for_service "http://localhost:8501" "Dashboard" || wait_for_service "http://localhost:8502" "Dashboard"; then
    DASHBOARD_PORT=$(lsof -ti:8501,8502 | head -1 | xargs -I {} lsof -p {} | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)
    if [ -z "$DASHBOARD_PORT" ]; then
        DASHBOARD_PORT="8501 or 8502"
    fi
    echo "✅ Dashboard started successfully (PID: $DASHBOARD_PID)"
else
    echo "❌ Failed to start Dashboard"
fi

# Step 5: Final Status Check
echo ""
echo "📋 Step 5: System Status Check..."
source venv/bin/activate
python3 main.py status

echo ""
echo "🎉 ==================================="
echo "🎉 SYSTEM STARTUP COMPLETE!"
echo "🎉 ==================================="
echo ""
echo "📊 Services Running:"
echo "   • MCP Server: http://localhost:8080 (PID: $MCP_PID)"
echo "   • Python App: Background process (PID: $PYTHON_PID)"
echo "   • Dashboard: http://localhost:8501 or http://localhost:8502 (PID: $DASHBOARD_PID)"
echo ""
echo "🔑 Test Login Numbers:"
echo "   • 2222222222 (Full portfolio with large MF)"
echo "   • 3333333333 (Full portfolio with small MF)"
echo "   • 1111111111 (Minimal assets)"
echo "   • 7777777777 (Debt-heavy user)"
echo ""
echo "📝 Logs available in:"
echo "   • MCP Server: mcp_server.log"
echo "   • Python App: agentic_ai_startup.log"
echo "   • Dashboard: dashboard.log"
echo "   • System Log: agentic_ai.log"
echo ""
echo "🛑 To stop all services: ./stop_system.sh"
echo ""
echo "✨ Happy analyzing! Your AI financial advisor is ready!" 