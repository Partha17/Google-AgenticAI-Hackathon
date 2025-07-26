# 🚀 Quick Start Guide

## ⚡ Complete System Startup (Recommended)

```bash
# One command to start everything
./start.sh
```

**What this does:**
- ✅ **Auto-creates virtual environment** if needed
- ✅ **Installs dependencies** automatically  
- ✅ **Starts Fi MCP Server** (port 8080)
- ✅ **Launches ADK Agents** (multi-agent system)
- ✅ **Opens Financial Dashboard** (port 8501)
- ✅ **Verifies all components** are running

## 🎯 Alternative Startup Options

### **🖥️ Dashboard Only**
```bash
# Launch just the dashboard (requires MCP server running)
python launch_dashboard.py
```

### **🔌 MCP Server Only**
```bash
# Start/check Fi MCP server
./check_mcp.sh start
./check_mcp.sh status
```

### **🛠️ Environment Setup Only**
```bash
# Setup virtual environment and dependencies without starting services
./start.sh --setup-only
```

### **🧹 Cleanup Only**
```bash
# Stop all services and clean up processes
./start.sh --cleanup-only
```

## 📊 System Status Check

```bash
# Check Fi MCP server status
./check_mcp.sh

# Check all running processes
ps aux | grep -E "(streamlit|go run|python main_adk)"
```

## 🌐 Access Points

Once started, access your system at:

- **📊 Financial Dashboard**: http://localhost:8501
- **🔌 Fi MCP Server**: http://localhost:8080  
- **🤖 ADK Agents**: Running in background

## 🔧 Troubleshooting

### **Port Conflicts**
```bash
# Clean up and restart
./start.sh --cleanup-only
./start.sh
```

### **Missing Dependencies**  
```bash
# Force reinstall everything
./start.sh --force-reinstall
```

### **Go Not Found**
```bash
# macOS
brew install go

# Ubuntu/Debian  
sudo apt install golang-go
```

## 🎉 Quick Test

1. **Start the system**: `./start.sh`
2. **Open browser**: http://localhost:8501
3. **Check data**: Look for financial data in the dashboard
4. **Try AI chat**: Ask "What's my net worth?" in the AI section

## 💡 Pro Tips

- **Use `./start.sh`** for daily development - it handles everything
- **Check `./check_mcp.sh status`** if dashboard shows no data
- **The system auto-creates virtual environment** on first run
- **All processes can be stopped** with Ctrl+C or `./start.sh --cleanup-only`

**Ready to explore your Enhanced Financial Multi-Agent System! 🚀** 