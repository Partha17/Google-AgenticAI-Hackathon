# 🚀 Quick Start Guide

## One-Command Startup

Start the entire system with one command:
```bash
./start_system.sh
```

## What This Does

1. ✅ Kills any existing processes on ports 8080, 8501, 8502
2. ✅ Starts Fi MCP Server (Go) on port 8080
3. ✅ Activates Python virtual environment
4. ✅ Installs/updates dependencies
5. ✅ Starts Python AI application with real Fi MCP connection
6. ✅ Launches Streamlit dashboard
7. ✅ Shows system status and access information

## Access Points

- **Dashboard**: http://localhost:8501 or http://localhost:8502
- **MCP Server**: http://localhost:8080

## Test Login Numbers

Use any of these phone numbers when prompted to login:

| Phone Number | Scenario Description |
|-------------|----------------------|
| `2222222222` | Full portfolio with large mutual fund holdings |
| `3333333333` | Full portfolio with small mutual fund holdings |
| `1111111111` | Minimal assets (only savings account) |
| `7777777777` | Debt-heavy user with poor performance |
| `8888888888` | SIP Samurai (consistent SIP investor) |
| `9999999999` | Fixed Income focused investor |

## Stop Everything

```bash
./stop_system.sh
```

## Troubleshooting

**If startup fails:**
1. Run `./stop_system.sh` first
2. Check logs: `tail -f mcp_server.log` or `tail -f agentic_ai_startup.log`
3. Try `./start_system.sh` again

**If port conflicts:**
```bash
# Kill specific port
lsof -ti:8080 | xargs kill -9
```

**If missing dependencies:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Manual Commands (if needed)

```bash
# Check system status
source venv/bin/activate && python3 main.py status

# Generate AI insights manually
source venv/bin/activate && python3 main.py generate

# Test MCP connection
source venv/bin/activate && python3 main.py test
```

## Logs Location

- **MCP Server**: `mcp_server.log`
- **Python App**: `agentic_ai_startup.log` 
- **Dashboard**: `dashboard.log`
- **System**: `agentic_ai.log`

---

✨ **Your AI financial advisor is ready!** Open the dashboard and start exploring your financial insights. 