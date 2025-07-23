"""
Financial Data Collector Agent - ADK Implementation with AI-Powered Analysis
Specialized agent for gathering and AI-powered analysis of financial data using Google Gemini
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from adk_agents.agent_config import adk_config
from adk_agents.ai_analysis_base import AIAnalysisBase
from services.fi_mcp_client import fi_mcp_client

logger = logging.getLogger(__name__)

class FinancialDataCollectorAgent(AIAnalysisBase):
    """ADK-based Financial Data Collector Agent powered by Gemini AI for intelligent data analysis"""
    
    def __init__(self):
        self.agent_id = "financial_data_collector"
        config = adk_config.get_agent_definitions()[self.agent_id]
        super().__init__(self.agent_id, config)
        
    async def collect_all_financial_data(self, phone_number: str = None) -> Dict[str, Any]:
        """
        AI-powered comprehensive financial data collection and analysis using Gemini
        """
        try:
            logger.info("Starting AI-powered comprehensive financial data collection...")
            
            collection_result = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "success": False,
                "data_sources": [],
                "data_quality_score": 0.0,
                "collection_summary": {},
                "data": {},
                "ai_insights": {}
            }
            
            # Data collection types
            data_types = [
                "fetch_net_worth",
                "fetch_bank_transactions", 
                "fetch_credit_report",
                "fetch_epf_details",
                "fetch_mf_transactions",
                "fetch_stock_transactions"
            ]
            
            collected_data = {}
            successful_collections = 0
            
            # Collect data from each source
            for data_type in data_types:
                try:
                    logger.info(f"Collecting {data_type}...")
                    
                    if phone_number:
                        data = await fi_mcp_client.call_mcp_tool(data_type, {"phone_number": phone_number})
                    else:
                        # Use test data if no phone number provided
                        data = await fi_mcp_client.call_mcp_tool(data_type, {})
                    
                    source_info = {
                        "type": data_type,
                        "success": data is not None and "error" not in data,
                        "timestamp": datetime.utcnow().isoformat(),
                        "record_count": self._count_records(data) if data else 0
                    }
                    
                    if source_info["success"]:
                        collected_data[data_type] = data
                        successful_collections += 1
                        logger.info(f"✅ {data_type} collected successfully")
                    else:
                        logger.warning(f"❌ {data_type} collection failed")
                        source_info["error"] = str(data.get("error", "Unknown error")) if data else "No data returned"
                    
                    collection_result["data_sources"].append(source_info)
                    
                except Exception as e:
                    logger.error(f"Error collecting {data_type}: {e}")
                    collection_result["data_sources"].append({
                        "type": data_type,
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
            # AI-powered data quality analysis and insights
            if collected_data:
                collection_result["data"] = collected_data
                
                specific_instructions = """
                Perform comprehensive financial data quality assessment and analysis:
                
                1. **Data Quality Assessment**:
                   - Completeness analysis (missing fields, empty values)
                   - Consistency evaluation (data format, value ranges)
                   - Accuracy indicators (logical relationships, outliers)
                   - Timeliness assessment (data freshness, update frequency)
                   - Reliability scoring (source credibility, validation status)
                
                2. **Financial Profile Analysis**:
                   - Net worth and asset composition analysis
                   - Income and expense pattern evaluation
                   - Credit profile and risk assessment
                   - Investment portfolio analysis
                   - Financial behavior patterns
                
                3. **Data Insights Generation**:
                   - Key financial metrics extraction
                   - Trend identification and analysis
                   - Risk indicators and warning signs
                   - Opportunity identification
                   - Benchmarking against typical profiles
                
                4. **Data Quality Score Calculation**:
                   - Overall quality score (0.0-1.0)
                   - Component quality scores by data type
                   - Impact assessment of missing/poor quality data
                   - Recommendations for data improvement
                
                5. **Collection Summary**:
                   - Successfully collected data types
                   - Critical missing data identification
                   - Data relationship validation
                   - Integration readiness assessment
                
                Provide detailed quality assessment, financial insights,
                and specific recommendations for data enhancement.
                """
                
                # Use AI analysis for data quality and insights
                ai_analysis = await self.ai_analyze(
                    analysis_type="financial_data_quality_and_insights",
                    data={"collected_data": collected_data, "collection_sources": collection_result["data_sources"]},
                    specific_instructions=specific_instructions,
                    output_format="json"
                )
                
                # Extract AI insights and quality score
                if "error" not in ai_analysis:
                    collection_result["ai_insights"] = ai_analysis
                    collection_result["data_quality_score"] = ai_analysis.get("overall_quality_score", 0.5)
                    
                    # Enhance collection summary with AI insights
                    collection_result["collection_summary"] = {
                        "total_sources": len(data_types),
                        "successful_sources": successful_collections,
                        "data_quality_score": collection_result["data_quality_score"],
                        "key_insights": ai_analysis.get("key_insights", []),
                        "quality_issues": ai_analysis.get("quality_issues", []),
                        "recommendations": ai_analysis.get("recommendations", [])
                    }
                else:
                    # Fallback to simple calculation if AI fails
                    collection_result["data_quality_score"] = successful_collections / len(data_types)
                    collection_result["collection_summary"] = {
                        "total_sources": len(data_types),
                        "successful_sources": successful_collections,
                        "success_rate": collection_result["data_quality_score"],
                        "ai_analysis_failed": True
                    }
            
            collection_result["success"] = successful_collections > 0
            
            logger.info(f"AI-powered data collection completed - Quality Score: {collection_result['data_quality_score']:.2f}")
            return collection_result
            
        except Exception as e:
            logger.error(f"Error in AI-powered data collection: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "success": False,
                "fallback_analysis": "AI data collection failed, manual intervention required"
            }
    
    async def validate_data_quality(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered data quality validation and enhancement recommendations
        """
        try:
            logger.info("Starting AI-powered data quality validation...")
            
            specific_instructions = """
            Perform detailed data quality validation focusing on:
            
            1. **Completeness Validation**:
               - Required field presence check
               - Missing value impact assessment
               - Data coverage analysis by source
               - Critical gap identification
               - Completeness score calculation
            
            2. **Consistency Validation**:
               - Cross-source data consistency check
               - Format and structure validation
               - Value range and logical consistency
               - Temporal consistency analysis
               - Business rule validation
            
            3. **Accuracy Assessment**:
               - Data reasonableness checks
               - Outlier detection and analysis
               - Mathematical relationship validation
               - Historical trend consistency
               - Benchmark comparison
            
            4. **Data Reliability Evaluation**:
               - Source credibility assessment
               - Update frequency and timeliness
               - Data lineage and provenance
               - Error rate estimation
               - Confidence level calculation
            
            5. **Enhancement Recommendations**:
               - Priority data quality improvements
               - Additional data source suggestions
               - Collection process optimizations
               - Validation rule recommendations
               - Monitoring and alerting setup
            
            Provide specific quality scores, issue identification,
            and actionable improvement recommendations.
            """
            
            validation_results = await self.ai_analyze(
                analysis_type="data_quality_validation",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for validation results
            if "error" not in validation_results:
                validation_results = self._enhance_validation_structure(validation_results)
            
            logger.info("AI-powered data quality validation completed")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error in AI data quality validation: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def detect_data_anomalies(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered anomaly detection in financial data
        """
        try:
            logger.info("Starting AI-powered anomaly detection...")
            
            specific_instructions = """
            Perform comprehensive anomaly detection focusing on:
            
            1. **Statistical Anomalies**:
               - Unusual value distributions
               - Extreme outliers identification
               - Pattern deviations from norm
               - Seasonal anomaly detection
               - Variance anomaly analysis
            
            2. **Business Logic Anomalies**:
               - Impossible value combinations
               - Business rule violations
               - Logical inconsistencies
               - Relationship anomalies
               - Domain-specific oddities
            
            3. **Temporal Anomalies**:
               - Sudden trend changes
               - Irregular timing patterns
               - Missing time series data
               - Frequency anomalies
               - Sequential order issues
            
            4. **Behavioral Anomalies**:
               - Unusual spending patterns
               - Investment behavior deviations
               - Transaction frequency changes
               - Amount pattern anomalies
               - Account usage irregularities
            
            5. **Risk Indicators**:
               - Potential fraud indicators
               - Data manipulation signs
               - Quality degradation signals
               - System error indicators
               - External factor impacts
            
            Provide specific anomaly descriptions, severity ratings,
            potential causes, and recommended actions.
            """
            
            anomaly_results = await self.ai_analyze(
                analysis_type="financial_data_anomaly_detection",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for anomaly results
            if "error" not in anomaly_results:
                anomaly_results = self._enhance_anomaly_structure(anomaly_results)
            
            logger.info("AI-powered anomaly detection completed")
            return anomaly_results
            
        except Exception as e:
            logger.error(f"Error in AI anomaly detection: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _count_records(self, data: Dict[str, Any]) -> int:
        """Count records in collected data"""
        if not data or not isinstance(data, dict):
            return 0
        
        # Try to find array/list fields that indicate record count
        for key, value in data.items():
            if isinstance(value, list):
                return len(value)
            elif isinstance(value, dict) and "count" in value:
                return value["count"]
        
        return 1 if data else 0
    
    def _enhance_validation_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response structure for validation results"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_data_validation",
            **ai_response
        }
        
        # Ensure required fields
        if "overall_quality_score" not in enhanced:
            enhanced["overall_quality_score"] = enhanced.get("quality_score", 0.5)
        
        if "validation_results" not in enhanced:
            enhanced["validation_results"] = enhanced.get("results", {})
        
        if "quality_issues" not in enhanced:
            enhanced["quality_issues"] = enhanced.get("issues", [])
        
        if "recommendations" not in enhanced:
            enhanced["recommendations"] = enhanced.get("improvement_recommendations", [])
        
        return enhanced
    
    def _enhance_anomaly_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response structure for anomaly results"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_anomaly_detection",
            **ai_response
        }
        
        # Ensure required fields
        if "anomalies_detected" not in enhanced:
            enhanced["anomalies_detected"] = len(enhanced.get("anomalies", []))
        
        if "severity_distribution" not in enhanced:
            anomalies = enhanced.get("anomalies", [])
            severity_count = {}
            for anomaly in anomalies:
                severity = anomaly.get("severity", "medium")
                severity_count[severity] = severity_count.get(severity, 0) + 1
            enhanced["severity_distribution"] = severity_count
        
        if "recommended_actions" not in enhanced:
            enhanced["recommended_actions"] = enhanced.get("actions", [])
        
        return enhanced

# Create global instance
financial_data_collector_agent = FinancialDataCollectorAgent() 