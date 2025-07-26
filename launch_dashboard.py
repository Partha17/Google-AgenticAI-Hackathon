#!/usr/bin/env python3
"""
Simplified Dashboard Launcher for Financial Multi-Agent System
Launches the optimized financial dashboard
"""

import subprocess
import sys
import time
import argparse
import psutil
import os
from pathlib import Path

def log(message: str, level: str = "INFO"):
    """Simple logging"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_port(port: int) -> bool:
    """Check if a port is in use"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False

def kill_streamlit_processes():
    """Kill existing streamlit processes"""
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'streamlit' or (proc.info['cmdline'] and 'streamlit' in ' '.join(proc.info['cmdline'])):
                proc.kill()
                killed += 1
                log(f"Killed streamlit process {proc.pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed

def check_fi_mcp_server() -> bool:
    """Check if Fi MCP server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8080", timeout=2)
        return True
    except:
        return False

def start_fi_mcp_server():
    """Start Fi MCP server if not running"""
    if check_fi_mcp_server():
        log("✅ Fi MCP Server already running")
        return True
    
    log("🚀 Starting Fi MCP Server...")
    mcp_dir = Path("fi-mcp-server")
    if not mcp_dir.exists():
        log("❌ Fi MCP server directory not found")
        return False
    
    try:
        env = os.environ.copy()
        env["FI_MCP_PORT"] = "8080"
        subprocess.Popen(["go", "run", "main.go"], cwd=mcp_dir, env=env)
        
        # Wait for server to start
        for i in range(10):
            if check_fi_mcp_server():
                log("✅ Fi MCP Server started")
                return True
            time.sleep(1)
        
        log("⚠️ Fi MCP Server may not be ready yet")
        return True
    except Exception as e:
        log(f"❌ Failed to start Fi MCP Server: {e}")
        return False

def launch_dashboard(port: int = 8501, start_mcp: bool = True):
    """Launch the financial dashboard"""
    log("🚀 Financial Dashboard Launcher")
    log("=" * 50)
    
    # Start MCP server if requested
    if start_mcp:
        start_fi_mcp_server()
    
    # Kill existing streamlit processes
    killed = kill_streamlit_processes()
    if killed > 0:
        log(f"🧹 Cleaned up {killed} existing streamlit processes")
        time.sleep(2)
    
    # Check if port is still in use
    if check_port(port):
        log(f"⚠️ Port {port} is still in use")
        time.sleep(2)
    
    # Launch dashboard
    log(f"📊 Starting Financial Dashboard on port {port}...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard/app.py",
            f"--server.port={port}",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        log("👋 Dashboard stopped by user")
    except Exception as e:
        log(f"❌ Error running dashboard: {e}")

def main():
    parser = argparse.ArgumentParser(description="Launch Financial Dashboard")
    parser.add_argument("--port", type=int, default=8501, help="Port to run dashboard on (default: 8501)")
    parser.add_argument("--no-mcp", action="store_true", help="Don't start Fi MCP server")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("🎯 Financial Dashboard Launcher")
        print("=" * 40)
        
        # Get port
        try:
            port_input = input(f"Port (default: {args.port}): ").strip()
            port = int(port_input) if port_input else args.port
        except ValueError:
            port = args.port
        
        # Start MCP option
        mcp_input = input("Start Fi MCP server? (Y/n): ").strip().lower()
        start_mcp = mcp_input != 'n'
        
        print()
        launch_dashboard(port, start_mcp)
    else:
        launch_dashboard(args.port, not args.no_mcp)

if __name__ == "__main__":
    main() 