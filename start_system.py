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
    
    def check_python_environment(self, force_reinstall: bool = False) -> bool:
        """Check and setup Python virtual environment"""
        if not self.venv_path.exists():
            self.log("📦 Virtual environment not found. Creating...")
            if not self.create_virtual_environment():
                return False
        
        # Check if requirements are installed
        if not self.check_dependencies(force_reinstall):
            self.log("📦 Installing dependencies...")
            if not self.install_dependencies():
                return False
        
        self.log("✅ Python environment ready")
        return True
    
    def create_virtual_environment(self) -> bool:
        """Create a new virtual environment"""
        try:
            self.log("🔧 Creating virtual environment...")
            result = subprocess.run([sys.executable, "-m", "venv", "venv"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("✅ Virtual environment created successfully")
                return True
            else:
                self.log(f"❌ Failed to create virtual environment: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error creating virtual environment: {e}", "ERROR")
            return False
    
    def get_venv_python(self) -> str:
        """Get the path to the Python executable in the venv"""
        if sys.platform == "win32":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")
    
    def get_venv_pip(self) -> str:
        """Get the path to pip in the venv"""
        if sys.platform == "win32":
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")
    
    def check_dependencies(self, force_reinstall: bool = False) -> bool:
        """Check if key dependencies are installed"""
        if force_reinstall:
            self.log("🔄 Force reinstall requested, skipping dependency check")
            return False
            
        try:
            venv_python = self.get_venv_python()
            
            # Check for key packages
            key_packages = ["streamlit", "langchain", "requests"]
            
            for package in key_packages:
                result = subprocess.run([venv_python, "-c", f"import {package}"], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.log(f"📦 Missing package: {package}")
                    return False
            
            self.log("✅ Dependencies already installed")
            return True
            
        except Exception as e:
            self.log(f"⚠️  Error checking dependencies: {e}", "WARNING")
            return False
    
    def install_dependencies(self) -> bool:
        """Install dependencies from requirements.txt"""
        try:
            requirements_file = self.project_root / "requirements.txt"
            
            if not requirements_file.exists():
                self.log("⚠️  requirements.txt not found, skipping dependency installation", "WARNING")
                return True
            
            venv_pip = self.get_venv_pip()
            
            self.log("📥 Installing dependencies from requirements.txt...")
            
            # Upgrade pip first
            self.log("🔄 Upgrading pip...")
            result = subprocess.run([venv_pip, "install", "--upgrade", "pip"], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log(f"⚠️  Warning: Could not upgrade pip: {result.stderr}", "WARNING")
            
            # Install requirements
            result = subprocess.run([venv_pip, "install", "-r", str(requirements_file)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Dependencies installed successfully")
                return True
            else:
                self.log(f"❌ Failed to install dependencies: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error installing dependencies: {e}", "ERROR")
            return False
    
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
            # Use venv Python if available
            python_executable = self.get_venv_python() if self.venv_path.exists() else sys.executable
            
            # Prepare environment
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root) + ":" + env.get("PYTHONPATH", "")
            
            # Start ADK system
            process = subprocess.Popen(
                [python_executable, "main_adk.py"],
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
    
    def start_dashboard(self) -> bool:
        """Start the dashboard"""
        self.log(f"📊 Starting Financial Dashboard...")
        
        # Use the main dashboard
        dashboard_file = "dashboard/app.py"
        
        try:
            # Use venv Python if available
            python_executable = self.get_venv_python() if self.venv_path.exists() else sys.executable
            
            # Prepare environment
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root) + ":" + env.get("PYTHONPATH", "")
            
            # Start dashboard
            process = subprocess.Popen([
                python_executable, "-m", "streamlit", "run", dashboard_file,
                f"--server.port={self.dashboard_port}",
                "--server.headless=true",
                "--server.fileWatcherType=none"
            ], cwd=self.project_root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes["dashboard"] = process
            
            # Wait for dashboard to start
            for i in range(20):
                if self.check_port(self.dashboard_port):
                    self.log(f"✅ Financial Dashboard started on http://localhost:{self.dashboard_port}")
                    return True
                time.sleep(1)
            
            self.log(f"❌ Financial Dashboard failed to start", "ERROR")
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
    
    def start_system(self):
        """Start the complete system"""
        try:
            self.log("🚀 Starting Enhanced Financial Multi-Agent System")
            self.log("="*60)
            
            # Environment setup
            if not self.check_python_environment(False):
                self.log("❌ Environment setup failed", "ERROR")
                return False
            
            # Cleanup existing processes
            self.cleanup_existing_processes()
            
            # Start Fi MCP Server
            if not self.start_fi_mcp_server():
                self.log("❌ Failed to start Fi MCP Server")
                return False
            
            # Verify MCP server is responding
            if not self.verify_mcp_server():
                self.log("⚠️  MCP Server verification failed")
            
            # Start ADK Agents
            if not self.start_adk_agents():
                self.log("❌ Failed to start ADK agents")
                return False
            
            # Start Dashboard
            if self.start_dashboard():
                self.log("🎉 All services started successfully!")
                self.log("="*60)
                self.log(f"📊 Dashboard: http://localhost:{self.dashboard_port}")
                self.log(f"🔌 Fi MCP Server: http://localhost:{self.mcp_port}")
                self.log(f"🤖 ADK Agents: Running")
                self.log("="*60)
                return True
            else:
                self.log("❌ Failed to start dashboard")
                return False
                
        except Exception as e:
            self.log(f"❌ System startup failed: {e}", "ERROR")
            return False
    
    def main():
        """Main function"""
        import argparse
        
        parser = argparse.ArgumentParser(description="Start Enhanced Financial Multi-Agent System")
# Dashboard option removed - now uses single optimized dashboard
        parser.add_argument("--monitor", action="store_true", 
                           help="Enable process monitoring")
        parser.add_argument("--cleanup-only", action="store_true",
                           help="Only cleanup existing processes and exit")
        parser.add_argument("--force-reinstall", action="store_true",
                           help="Force reinstall dependencies even if they exist")
        parser.add_argument("--setup-only", action="store_true",
                           help="Only setup environment (venv + dependencies) and exit")
        
        args = parser.parse_args()
        
        manager = SystemManager()
        
        if args.cleanup_only:
            manager.cleanup_existing_processes()
            return
        
        if args.setup_only:
            manager.force_reinstall = args.force_reinstall
            if manager.check_python_environment(args.force_reinstall):
                manager.log("✅ Environment setup completed successfully!")
            else:
                manager.log("❌ Environment setup failed!", "ERROR")
            return
        
        try:
            # Set force reinstall flag
            manager.force_reinstall = args.force_reinstall
            success = manager.start_system()
            
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