#!/usr/bin/env python3
"""
Dashboard Launcher for Enhanced Financial Multi-Agent System
Provides options to run different dashboard configurations
"""

import subprocess
import sys
import os
import time
import argparse
from pathlib import Path

def check_port(port):
    """Check if a port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def kill_streamlit_processes():
    """Kill any existing streamlit processes"""
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run("pkill -f streamlit", shell=True, capture_output=True)
        else:  # Linux
            subprocess.run("pkill streamlit", shell=True, capture_output=True)
    except:
        pass

def check_fi_mcp_server():
    """Check if Fi MCP server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8080", timeout=2)
        return True
    except:
        return False

def start_fi_mcp_server():
    """Start the Fi MCP server if not running"""
    if check_fi_mcp_server():
        print("✅ Fi MCP Server already running on port 8080")
        return True
    
    print("🚀 Starting Fi MCP Server...")
    server_dir = Path("fi-mcp-server")
    
    if not server_dir.exists():
        print("❌ Fi MCP Server directory not found!")
        return False
    
    env = os.environ.copy()
    env["FI_MCP_PORT"] = "8080"
    
    try:
        process = subprocess.Popen(
            ["go", "run", "main.go"],
            cwd=server_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        for i in range(10):
            if check_port(8080):
                print("✅ Fi MCP Server started on port 8080")
                return True
            time.sleep(1)
        
        print("❌ Fi MCP Server failed to start")
        return False
        
    except FileNotFoundError:
        print("❌ Go not found. Please install Go to run the Fi MCP Server")
        return False
    except Exception as e:
        print(f"❌ Error starting Fi MCP Server: {e}")
        return False

def launch_dashboard(dashboard_type="original", port=8501, with_mcp=True):
    """Launch the specified dashboard"""
    
    # Kill existing processes
    kill_streamlit_processes()
    time.sleep(1)
    
    # Choose dashboard file
    if dashboard_type == "enhanced":
        dashboard_file = "dashboard/enhanced_dashboard.py"
        title = "Enhanced Dashboard (Google Cloud)"
    else:
        dashboard_file = "dashboard/app.py"
        title = "Original Dashboard"
    
    # Check if we should start Fi MCP server
    if with_mcp:
        start_fi_mcp_server()
    
    print(f"🎨 Starting {title} on http://localhost:{port}")
    
    # Set environment for proper imports
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + ":" + env.get("PYTHONPATH", "")
    
    try:
        # Start the dashboard
        cmd = [
            "streamlit", "run", dashboard_file,
            f"--server.port={port}",
            "--server.headless=false"
        ]
        
        subprocess.run(cmd, env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install: pip install streamlit")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Launch Financial Dashboard")
    parser.add_argument(
        "--dashboard", 
        choices=["original", "enhanced"], 
        default="original",
        help="Choose dashboard type (default: original)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501,
        help="Port to run dashboard on (default: 8501)"
    )
    parser.add_argument(
        "--no-mcp", 
        action="store_true",
        help="Don't start Fi MCP server"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="Interactive mode to choose options"
    )
    
    args = parser.parse_args()
    
    print("🚀 Financial Dashboard Launcher")
    print("=" * 50)
    
    # Interactive mode
    if args.interactive:
        print("\nChoose dashboard type:")
        print("1. Original Dashboard (Stable)")
        print("2. Enhanced Dashboard (Google Cloud)")
        
        choice = input("Enter choice (1-2) [1]: ").strip() or "1"
        
        if choice == "2":
            dashboard_type = "enhanced"
        else:
            dashboard_type = "original"
        
        port = input(f"Port number [{args.port}]: ").strip()
        if port:
            try:
                args.port = int(port)
            except ValueError:
                print("Invalid port, using default")
        
        with_mcp = input("Start Fi MCP Server? [y/N]: ").strip().lower() in ['y', 'yes']
        
    else:
        dashboard_type = args.dashboard
        with_mcp = not args.no_mcp
    
    print(f"\nConfiguration:")
    print(f"📊 Dashboard: {dashboard_type.title()}")
    print(f"🔌 Port: {args.port}")
    print(f"🔗 Fi MCP Server: {'Yes' if with_mcp else 'No'}")
    print()
    
    # Launch the dashboard
    launch_dashboard(dashboard_type, args.port, with_mcp)

if __name__ == "__main__":
    main() 