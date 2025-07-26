#!/usr/bin/env python3
"""
Complete System Startup Script for Enhanced Financial Multi-Agent System
Manages Fi MCP Server, ADK Agents, and Dashboard with proper process control
"""

import subprocess
import sys
import os
import time
import signal
import threading
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional

class SystemManager:
    def __init__(self):
        self.processes = {}
        self.mcp_port = 8080
        self.dashboard_port = 8501
        self.project_root = Path.cwd()
        self.venv_path = self.project_root / "venv"
        
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_port(self, port: int) -> bool:
        """Check if a port is in use"""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    
    def kill_processes_on_port(self, port: int):
        """Kill any processes running on specified port"""
        try:
            if sys.platform == "darwin":  # macOS
                cmd = f"lsof -ti:{port}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(f"kill -9 {pid}", shell=True)
                            self.log(f"Killed process {pid} on port {port}")
            else:  # Linux
                subprocess.run(f"fuser -k {port}/tcp", shell=True, capture_output=True)
                self.log(f"Killed processes on port {port}")
        except Exception as e:
            self.log(f"Error killing processes on port {port}: {e}", "WARNING")
    
    def kill_process_by_name(self, name: str):
        """Kill processes by name pattern"""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(f"pkill -f '{name}'", shell=True, capture_output=True)
            else:  # Linux
                subprocess.run(f"pkill -f '{name}'", shell=True, capture_output=True)
            self.log(f"Killed processes matching: {name}")
        except Exception as e:
            self.log(f"Error killing processes {name}: {e}", "WARNING")
    
    def cleanup_existing_processes(self):
        """Clean up any existing system processes"""
        self.log("🧹 Cleaning up existing processes...")
        
        # Kill Fi MCP server processes
        self.kill_processes_on_port(self.mcp_port)
        self.kill_process_by_name("go run main.go")
        self.kill_process_by_name("fi-mcp-server")
        
        # Kill Streamlit processes
        self.kill_processes_on_port(self.dashboard_port)
        self.kill_process_by_name("streamlit")
        
        # Kill any Python ADK processes
        self.kill_process_by_name("main_adk.py")
        
        time.sleep(2)  # Wait for processes to terminate
        self.log("✅ Cleanup completed")
    
    def check_go_installation(self) -> bool:
        """Check if Go is installed"""
        try:
            result = subprocess.run(["go", "version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ Go found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
        
        self.log("❌ Go not found. Please install Go to run Fi MCP server", "ERROR")
        return False
    
    def check_python_environment(self) -> bool:
        """Check Python virtual environment"""
        if not self.venv_path.exists():
            self.log("❌ Virtual environment not found. Run: python -m venv venv", "ERROR")
            return False
        
        # Check if we're in the venv
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.log("✅ Virtual environment active")
            return True
        else:
            self.log("⚠️  Virtual environment not activated", "WARNING")
            return True  # We can still try to run
    
    def start_fi_mcp_server(self) -> bool:
        """Start the Fi MCP server"""
        self.log("🚀 Starting Fi MCP Server...")
        
        if not self.check_go_installation():
            return False
        
        mcp_dir = self.project_root / "fi-mcp-server"
        if not mcp_dir.exists():
            self.log("❌ Fi MCP server directory not found", "ERROR")
            return False
        
        # Set environment variables
        env = os.environ.copy()
        env["FI_MCP_PORT"] = str(self.mcp_port)
        
        try:
            # Start the server
            process = subprocess.Popen(
                ["go", "run", "main.go"],
                cwd=mcp_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["fi_mcp_server"] = process
            
            # Wait for server to start
            for i in range(15):
                if self.check_port(self.mcp_port):
                    self.log(f"✅ Fi MCP Server started on port {self.mcp_port}")
                    return True
                time.sleep(1)
            
            self.log("❌ Fi MCP Server failed to start within 15 seconds", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"❌ Error starting Fi MCP Server: {e}", "ERROR")
            return False
    
    def verify_mcp_server(self) -> bool:
        """Verify Fi MCP server is responding"""
        try:
            # Try a few different endpoints that might exist
            endpoints = [
                f"http://localhost:{self.mcp_port}/",
                f"http://localhost:{self.mcp_port}/health",
                f"http://localhost:{self.mcp_port}/api/status"
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=3)
                    self.log(f"✅ Fi MCP Server responding at {endpoint}")
                    return True
                except requests.exceptions.RequestException:
                    continue
            
            # If no endpoint responds, just check if port is open
            if self.check_port(self.mcp_port):
                self.log(f"✅ Fi MCP Server port {self.mcp_port} is open")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"⚠️  MCP Server verification error: {e}", "WARNING")
            return self.check_port(self.mcp_port)
    
    def start_adk_agents(self) -> bool:
        """Start the ADK agents system in background"""
        self.log("🤖 Starting ADK Multi-Agent System...")
        
        try:
            # Prepare environment
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root) + ":" + env.get("PYTHONPATH", "")
            
            # Start ADK system
            process = subprocess.Popen(
                [sys.executable, "main_adk.py"],
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["adk_agents"] = process
            
            # Give it a moment to initialize
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                self.log("✅ ADK Multi-Agent System started successfully")
                return True
            else:
                self.log("❌ ADK Multi-Agent System failed to start", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error starting ADK agents: {e}", "ERROR")
            return False
    
    def start_dashboard(self, dashboard_type: str = "original") -> bool:
        """Start the dashboard"""
        self.log(f"📊 Starting {dashboard_type.title()} Dashboard...")
        
        # Choose dashboard file
        dashboard_file = "dashboard/enhanced_dashboard.py" if dashboard_type == "enhanced" else "dashboard/app.py"
        
        try:
            # Prepare environment
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root) + ":" + env.get("PYTHONPATH", "")
            
            # Start dashboard
            process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", dashboard_file,
                f"--server.port={self.dashboard_port}",
                "--server.headless=true",
                "--server.fileWatcherType=none"
            ], cwd=self.project_root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes["dashboard"] = process
            
            # Wait for dashboard to start
            for i in range(20):
                if self.check_port(self.dashboard_port):
                    self.log(f"✅ {dashboard_type.title()} Dashboard started on http://localhost:{self.dashboard_port}")
                    return True
                time.sleep(1)
            
            self.log(f"❌ {dashboard_type.title()} Dashboard failed to start", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"❌ Error starting dashboard: {e}", "ERROR")
            return False
    
    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        self.log("👁️  Starting process monitoring...")
        
        while True:
            try:
                time.sleep(30)  # Check every 30 seconds
                
                for name, process in self.processes.items():
                    if process.poll() is not None:
                        self.log(f"⚠️  Process {name} has stopped", "WARNING")
                        # Could implement restart logic here
                
            except KeyboardInterrupt:
                self.log("🛑 Monitoring stopped by user")
                break
            except Exception as e:
                self.log(f"Error in process monitoring: {e}", "WARNING")
    
    def stop_all_processes(self):
        """Stop all managed processes"""
        self.log("🛑 Stopping all processes...")
        
        for name, process in self.processes.items():
            try:
                self.log(f"Stopping {name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.log(f"Force killed {name}")
                    
            except Exception as e:
                self.log(f"Error stopping {name}: {e}", "WARNING")
        
        # Final cleanup
        self.cleanup_existing_processes()
        self.log("✅ All processes stopped")
    
    def start_system(self, dashboard_type: str = "original"):
        """Start the complete system"""
        self.log("🚀 Starting Enhanced Financial Multi-Agent System")
        self.log("=" * 60)
        
        # Preliminary checks
        if not self.check_python_environment():
            return False
        
        # Cleanup existing processes
        self.cleanup_existing_processes()
        
        # Start components in order
        success_count = 0
        total_components = 3
        
        # 1. Start Fi MCP Server
        if self.start_fi_mcp_server():
            if self.verify_mcp_server():
                success_count += 1
            else:
                self.log("⚠️  Fi MCP Server may not be responding properly", "WARNING")
        
        # 2. Start ADK Agents
        if self.start_adk_agents():
            success_count += 1
        
        # 3. Start Dashboard
        if self.start_dashboard(dashboard_type):
            success_count += 1
        
        # Summary
        self.log("=" * 60)
        if success_count == total_components:
            self.log("🎉 System started successfully!")
            self.log(f"📊 Dashboard: http://localhost:{self.dashboard_port}")
            self.log(f"🔌 Fi MCP Server: http://localhost:{self.mcp_port}")
            self.log("🤖 ADK Agents: Running")
            self.log("\nPress Ctrl+C to stop all services")
            return True
        else:
            self.log(f"⚠️  Partial success: {success_count}/{total_components} components started")
            return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Enhanced Financial Multi-Agent System")
    parser.add_argument("--dashboard", choices=["original", "enhanced"], default="original",
                       help="Dashboard type to start (default: original)")
    parser.add_argument("--monitor", action="store_true", 
                       help="Enable process monitoring")
    parser.add_argument("--cleanup-only", action="store_true",
                       help="Only cleanup existing processes and exit")
    
    args = parser.parse_args()
    
    manager = SystemManager()
    
    if args.cleanup_only:
        manager.cleanup_existing_processes()
        return
    
    try:
        success = manager.start_system(args.dashboard)
        
        if success and args.monitor:
            # Start monitoring in background
            monitor_thread = threading.Thread(target=manager.monitor_processes, daemon=True)
            monitor_thread.start()
        
        if success:
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop_all_processes()

if __name__ == "__main__":
    main() 