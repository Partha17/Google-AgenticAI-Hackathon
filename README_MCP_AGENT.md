# MCP Periodic AI Agent

A comprehensive agent that combines automated data collection from Fi MCP server with AI-powered financial analysis.

## Overview

The MCP Periodic AI Agent is designed to:
- **Automatically collect financial data** from Fi MCP server on a scheduled basis
- **Generate AI insights** using Google Gemini models
- **Provide on-demand analysis** through the dashboard
- **Monitor system health** and data quality

## Features

### 🕒 Periodic Data Collection
- Scheduled data collection every 60 minutes (configurable)
- Automatic retry logic for failed connections
- Support for all Fi MCP data types:
  - Net worth analysis
  - Bank transactions
  - Credit reports
  - EPF details
  - Mutual fund transactions
  - Stock transactions

### 🧠 AI-Powered Analysis
- **Portfolio Analysis**: Asset allocation, diversification assessment
- **Risk Assessment**: Credit score analysis, debt evaluation
- **Financial Health**: Comprehensive wellness scoring
- **Opportunity Identification**: Investment and optimization suggestions

### 📊 Dashboard Integration
- Real-time agent status monitoring
- On-demand data collection and analysis buttons
- Recent activity logs and statistics
- Configuration management interface

## Configuration

The agent can be configured via `adk_agents/agent_config.py`:

```python
"mcp_periodic_ai_agent": {
    "collection_interval_minutes": 60,  # How often to collect data
    "analysis_triggers": {
        "data_freshness_hours": 2,      # Trigger analysis if data is older than X hours
        "significant_change_threshold": 0.05  # 5% change threshold
    },
    "model": "gemini-1.5-flash",
    "generation_config": {
        "temperature": 0.3,
        "max_output_tokens": 2048,
        "top_p": 0.8
    }
}
```

## Usage

### Starting the Agent

The agent starts automatically with the ADK system:

```bash
python start_system.py
```

Or manually through the dashboard:
1. Go to the "🤖 MCP AI Agent" tab
2. Click "▶️ Start Periodic Collection"

### On-Demand Operations

#### Collect Data Now
```python
from adk_agents.mcp_periodic_ai_agent import mcp_periodic_ai_agent

result = mcp_periodic_ai_agent.collect_mcp_data()
```

#### Run AI Analysis
```python
result = mcp_periodic_ai_agent.generate_ai_analysis(force=True)
```

### Dashboard Controls

The dashboard provides several control buttons:

- **▶️ Start/⏹️ Stop Periodic Collection**: Control automated data collection
- **📥 Collect Data Now**: Immediate data collection from Fi MCP
- **🧠 Run AI Analysis**: Generate comprehensive AI insights
- **🔄 Refresh Status**: Update agent status display

## API Reference

### MCPPeriodicAIAgent

#### Methods

##### `start_periodic_collection()`
Starts the scheduled data collection process.

##### `stop_periodic_collection()`
Stops the scheduled data collection process.

##### `collect_mcp_data() -> Dict[str, Any]`
Collects data from Fi MCP server and stores in database.

**Returns:**
```python
{
    "success": True,
    "records_stored": 5,
    "data_types": ["net_worth", "credit_report", ...],
    "timestamp": "2024-01-01T12:00:00"
}
```

##### `generate_ai_analysis(force: bool = False) -> Dict[str, Any]`
Generates comprehensive AI analysis of collected financial data.

**Parameters:**
- `force`: Skip quota checks and force analysis

**Returns:**
```python
{
    "success": True,
    "insights_generated": 4,
    "insights": [...],
    "timestamp": "2024-01-01T12:00:00"
}
```

##### `get_agent_status() -> Dict[str, Any]`
Returns current agent status and statistics.

**Returns:**
```python
{
    "agent_id": "mcp_periodic_ai_agent",
    "running": True,
    "stats": {
        "total_collections": 24,
        "successful_collections": 22,
        "analysis_count": 8,
        "last_collection_time": "2024-01-01T12:00:00",
        "last_analysis_time": "2024-01-01T11:30:00"
    },
    "mcp_connection": True
}
```

## Architecture

### Components

1. **Agent Core** (`MCPPeriodicAIAgent`): Main agent class extending `AIAnalysisBase`
2. **Scheduler**: Uses Python `schedule` library for periodic tasks
3. **Data Collector**: Integrates with `fi_mcp_client` for data collection
4. **AI Analyzer**: Uses Google Gemini for financial analysis
5. **Database**: Stores collected data and generated insights
6. **Service Manager** (`MCPAgentService`): Manages agent lifecycle

### Data Flow

```
Fi MCP Server → Agent Collector → Database → AI Analyzer → Insights → Dashboard
     ↑                                                        ↓
     └── Scheduled Collection (every 60 min) ←←←←←←←←←←←←←←←←←←←←┘
```

### Database Schema

The agent uses two main database tables:

#### MCPData
- `data_type`: Type of financial data (net_worth, credit_report, etc.)
- `raw_data`: JSON string of collected data
- `timestamp`: Collection timestamp
- `phone_number`: Associated phone number
- `session_id`: MCP session identifier

#### AIInsight
- `title`: Insight headline
- `content`: Detailed analysis content
- `insight_type`: Category (portfolio_analysis, risk_assessment, etc.)
- `confidence_score`: AI confidence level (0.0-1.0)
- `data_sources`: JSON array of source data types
- `created_at`: Generation timestamp

## Monitoring and Troubleshooting

### Health Checks

The agent provides several health indicators:

- **MCP Connection**: Tests Fi MCP server connectivity
- **Periodic Collection Status**: Shows if scheduled collection is running
- **Quota Status**: Monitors AI API usage limits
- **Recent Activity**: Shows latest collections and analyses

### Common Issues

#### MCP Server Not Accessible
- Ensure Fi MCP server is running on port 8080
- Check network connectivity
- Verify authentication credentials

#### AI Analysis Failing
- Check Google API key configuration
- Monitor quota usage
- Verify input data quality

#### Periodic Collection Not Running
- Check agent status in dashboard
- Review scheduler thread health
- Look for error messages in logs

### Logs

Agent activity is logged to:
- Console output during startup
- Centralized logging system
- Dashboard activity displays

Key log locations:
- **Service logs**: `services/logger_config.py`
- **Agent logs**: `adk_agents/mcp_periodic_ai_agent.py`
- **Dashboard logs**: Dashboard "Recent Activity" section

## Security Considerations

- API keys stored in environment variables
- MCP session management with timeout
- Quota management to prevent API abuse
- Database encryption for sensitive financial data

## Performance Optimization

- Efficient database queries with indexes
- Batch processing for multiple data types
- Async/await patterns for non-blocking operations
- Configurable collection intervals
- Smart analysis triggering based on data freshness

## Future Enhancements

- Real-time data streaming from Fi MCP
- Machine learning model training on collected data
- Predictive analytics and forecasting
- Advanced portfolio optimization algorithms
- Integration with external market data sources 