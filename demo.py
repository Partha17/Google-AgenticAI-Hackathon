#!/usr/bin/env python3
"""
Demonstration script for the Agentic AI Financial Insights System
Shows the complete workflow with mock data and simulated insights
"""

import json
from datetime import datetime
from models.database import create_tables, SessionLocal, MCPData, AIInsight
from services.mcp_mock import mock_mcp

def demo_data_collection():
    """Demonstrate data collection from mock MCP"""
    print("🔄 Demonstrating Data Collection...")
    
    # Get sample data from mock MCP
    sample_data = mock_mcp.get_batch_data(count=10)
    
    db = SessionLocal()
    try:
        for i, data_item in enumerate(sample_data):
            print(f"   📊 Collecting {data_item['type']}: {data_item.get('symbol', 'N/A')}")
            
            mcp_record = MCPData(
                data_type=data_item.get("type", "unknown"),
                raw_data=json.dumps(data_item),
                timestamp=datetime.utcnow()
            )
            db.add(mcp_record)
        
        db.commit()
        print(f"   ✅ Successfully stored {len(sample_data)} records")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def demo_simulated_insights():
    """Demonstrate AI insight generation with simulated data"""
    print("\n🧠 Demonstrating AI Insight Generation...")
    
    # Create some simulated insights
    simulated_insights = [
        {
            "insight_type": "trend_analysis",
            "title": "Tech Stocks Show Strong Momentum",
            "content": "Analysis of recent data shows technology stocks are demonstrating strong upward momentum with increased trading volumes and positive sentiment indicators.",
            "confidence_score": 0.87,
            "key_factors": ["Increased volume", "Positive sentiment", "Strong fundamentals"],
            "recommended_actions": ["Consider long positions", "Monitor for breakout patterns"]
        },
        {
            "insight_type": "risk_assessment",
            "title": "Market Volatility Alert",
            "content": "Current market conditions show increased volatility with potential for significant price swings. Risk management strategies should be prioritized.",
            "confidence_score": 0.79,
            "key_factors": ["High volatility", "Economic uncertainty", "Mixed signals"],
            "recommended_actions": ["Reduce position sizes", "Implement stop losses"]
        },
        {
            "insight_type": "opportunity",
            "title": "Potential Entry Point Identified",
            "content": "Several stocks are approaching key support levels, presenting potential buying opportunities for medium-term investors.",
            "confidence_score": 0.73,
            "key_factors": ["Support level test", "Oversold conditions", "Volume confirmation"],
            "recommended_actions": ["Watch for bounce signals", "Prepare entry orders"]
        }
    ]
    
    db = SessionLocal()
    try:
        for insight_data in simulated_insights:
            print(f"   🔍 Generating {insight_data['insight_type']}: {insight_data['title']}")
            
            ai_insight = AIInsight(
                insight_type=insight_data["insight_type"],
                title=insight_data["title"],
                content=insight_data["content"],
                confidence_score=insight_data["confidence_score"],
                timestamp=datetime.utcnow()
            )
            
            # Set metadata
            metadata = {
                "key_factors": insight_data["key_factors"],
                "recommended_actions": insight_data["recommended_actions"],
                "model": "demo-simulation",
                "generated_at": datetime.utcnow().isoformat()
            }
            ai_insight.set_metadata(metadata)
            ai_insight.set_source_ids([1, 2, 3])  # Simulated source IDs
            
            db.add(ai_insight)
        
        db.commit()
        print(f"   ✅ Successfully generated {len(simulated_insights)} insights")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def demo_dashboard_data():
    """Show sample data that will be displayed in dashboard"""
    print("\n📊 Dashboard Data Preview...")
    
    db = SessionLocal()
    try:
        # Show MCP data
        mcp_count = db.query(MCPData).count()
        print(f"   📈 MCP Data Records: {mcp_count}")
        
        # Show recent MCP data
        recent_mcp = db.query(MCPData).order_by(MCPData.timestamp.desc()).limit(3).all()
        for record in recent_mcp:
            data = json.loads(record.raw_data)
            print(f"      • {record.data_type}: {data.get('symbol', 'N/A')} - {data.get('price', 'N/A')}")
        
        # Show insights
        insights_count = db.query(AIInsight).count()
        print(f"   🧠 AI Insights: {insights_count}")
        
        # Show recent insights
        recent_insights = db.query(AIInsight).order_by(AIInsight.created_at.desc()).limit(3).all()
        for insight in recent_insights:
            print(f"      • {insight.insight_type}: {insight.title} (confidence: {insight.confidence_score:.2f})")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        db.close()

def main():
    """Run the complete demonstration"""
    print("🤖 Agentic AI Financial Insights System - Demo")
    print("=" * 50)
    
    # Initialize database
    create_tables()
    
    # Run demonstrations
    demo_data_collection()
    demo_simulated_insights()
    demo_dashboard_data()
    
    print("\n🎉 Demo Complete!")
    print("\n📋 Next Steps:")
    print("1. Set your GOOGLE_API_KEY in .env for real AI insights")
    print("2. Run 'streamlit run dashboard/app.py' to see the dashboard")
    print("3. Run 'python main.py start' to begin automated data collection")
    print("4. Replace mock MCP with real Fi MCP server connection")
    
    print("\n🌐 Dashboard should be available at: http://localhost:8501")

if __name__ == "__main__":
    main() 