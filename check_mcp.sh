#!/bin/bash
# Quick Fi MCP Server status checker

echo "🔍 Fi MCP Server Status Check"
echo "==============================="

# Function to check MCP server status
check_mcp_detailed() {
    echo "🔍 Checking Fi MCP Server..."
    
    # Check if Go is installed
    if ! command -v go >/dev/null 2>&1; then
        echo "❌ Go not installed (required for Fi MCP Server)"
        return 1
    fi
    
    # Check if fi-mcp-server directory exists
    if [ ! -d "fi-mcp-server" ]; then
        echo "❌ fi-mcp-server directory not found"
        return 1
    fi
    
    # Check if process is running
    if pgrep -f "go run main.go" >/dev/null 2>&1; then
        echo "✅ Fi MCP Server process is running"
        
        # Check if port 8080 is responding
        if command -v curl >/dev/null 2>&1; then
            if curl -s --connect-timeout 3 http://localhost:8080 >/dev/null 2>&1; then
                echo "✅ Fi MCP Server responding on http://localhost:8080"
                
                # Try to get server info if available
                response=$(curl -s --connect-timeout 3 http://localhost:8080 2>/dev/null)
                if [ $? -eq 0 ] && [ -n "$response" ]; then
                    echo "📊 Server response received"
                fi
                
                echo ""
                echo "🎉 Fi MCP Server is fully operational!"
                echo "🔗 Access: http://localhost:8080"
                return 0
            else
                echo "⚠️  Process running but port 8080 not responding"
                echo "   The server may still be starting up..."
                return 1
            fi
        elif command -v nc >/dev/null 2>&1; then
            if nc -z localhost 8080 2>/dev/null; then
                echo "✅ Port 8080 is open"
                echo "🎉 Fi MCP Server appears to be running!"
                return 0
            else
                echo "⚠️  Process running but port 8080 not open"
                return 1
            fi
        else
            echo "✅ Process detected (cannot verify port without curl/nc)"
            echo "🎉 Fi MCP Server appears to be running!"
            return 0
        fi
    else
        echo "❌ Fi MCP Server process not found"
        
        # Check if port is still occupied
        if command -v lsof >/dev/null 2>&1; then
            port_check=$(lsof -ti:8080 2>/dev/null)
            if [ -n "$port_check" ]; then
                echo "⚠️  Port 8080 is occupied by process: $port_check"
                echo "   You may need to run: ./start.sh --cleanup-only"
            fi
        fi
        
        echo ""
        echo "💡 To start Fi MCP Server:"
        echo "   ./start.sh                    # Start complete system"
        echo "   cd fi-mcp-server && go run main.go  # Start MCP only"
        return 1
    fi
}

# Parse command line arguments
case "${1:-status}" in
    "status"|"check"|"")
        check_mcp_detailed
        ;;
    "start")
        echo "🚀 Starting Fi MCP Server..."
        if [ -d "fi-mcp-server" ]; then
            cd fi-mcp-server
            FI_MCP_PORT=8080 go run main.go &
            echo "⏳ Server starting in background..."
            sleep 3
            cd ..
            check_mcp_detailed
        else
            echo "❌ fi-mcp-server directory not found"
            exit 1
        fi
        ;;
    "stop")
        echo "🛑 Stopping Fi MCP Server..."
        if pgrep -f "go run main.go" >/dev/null 2>&1; then
            pkill -f "go run main.go"
            echo "✅ Fi MCP Server stopped"
        else
            echo "ℹ️  Fi MCP Server was not running"
        fi
        
        # Also kill any processes on port 8080
        if command -v lsof >/dev/null 2>&1; then
            port_pids=$(lsof -ti:8080 2>/dev/null)
            if [ -n "$port_pids" ]; then
                echo "🧹 Cleaning up port 8080..."
                echo "$port_pids" | xargs kill -9 2>/dev/null
            fi
        fi
        ;;
    "restart")
        echo "🔄 Restarting Fi MCP Server..."
        $0 stop
        sleep 2
        $0 start
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status    Check Fi MCP Server status (default)"
        echo "  start     Start Fi MCP Server"
        echo "  stop      Stop Fi MCP Server"
        echo "  restart   Restart Fi MCP Server"
        echo "  help      Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                # Check status"
        echo "  $0 status         # Check status"
        echo "  $0 start          # Start server"
        echo "  $0 stop           # Stop server"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 