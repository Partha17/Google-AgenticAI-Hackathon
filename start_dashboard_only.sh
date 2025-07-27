#!/bin/bash
# Dashboard-only startup script using deployed MCP server

echo "🚀 Financial Dashboard Startup (Deployed MCP Server)"
echo "=================================================="

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Using existing virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "   Please run setup first: ./start.sh --setup-only"
    exit 1
fi

# Kill any existing Streamlit processes
echo "🧹 Cleaning up existing processes..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# Start the dashboard
echo "🚀 Starting Financial Dashboard..."
echo "📊 Dashboard will be available at: http://localhost:8501"
echo "🔌 Using deployed MCP server: https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app"
echo ""

# Start Streamlit dashboard
streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0