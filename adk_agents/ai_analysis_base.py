"""
AI Analysis Base Class for ADK Agents
Provides Gemini-powered analysis capabilities for all financial agents
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Google AI imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from config import settings

logger = logging.getLogger(__name__)

class AIAnalysisBase:
    """Base class providing AI-powered analysis using Google Gemini"""
    
    def __init__(self, agent_id: str, agent_config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = agent_config
        self.llm = None
        self._initialize_ai_model()
    
    def _initialize_ai_model(self):
        """Initialize the Gemini AI model"""
        try:
            # Use Vertex AI if configured, otherwise use standard Google GenAI
            if settings.google_genai_use_vertexai:
                from langchain_google_vertexai import ChatVertexAI
                self.llm = ChatVertexAI(
                    model_name=self.config.get("model", "gemini-1.5-flash"),
                    project=settings.google_cloud_project,
                    location=settings.google_cloud_location,
                    temperature=self.config.get("generation_config", {}).get("temperature", 0.3),
                    max_output_tokens=self.config.get("generation_config", {}).get("max_output_tokens", 2048),
                    top_p=self.config.get("generation_config", {}).get("top_p", 0.8)
                )
                logger.info(f"Initialized Vertex AI model for {self.agent_id}")
            else:
                self.llm = ChatGoogleGenerativeAI(
                    model=self.config.get("model", "gemini-1.5-flash"),
                    google_api_key=settings.google_api_key,
                    temperature=self.config.get("generation_config", {}).get("temperature", 0.3),
                    max_output_tokens=self.config.get("generation_config", {}).get("max_output_tokens", 2048),
                    top_p=self.config.get("generation_config", {}).get("top_p", 0.8)
                )
                logger.info(f"Initialized Google GenAI model for {self.agent_id}")
                
        except Exception as e:
            logger.error(f"Failed to initialize AI model for {self.agent_id}: {e}")
            raise
    
    async def ai_analyze(self, 
                        analysis_type: str,
                        data: Dict[str, Any], 
                        specific_instructions: str = "",
                        output_format: str = "json") -> Dict[str, Any]:
        """
        Generic AI analysis method using Gemini
        
        Args:
            analysis_type: Type of analysis (risk, market, data_quality, etc.)
            data: Financial data to analyze
            specific_instructions: Additional instructions for this analysis
            output_format: Expected output format (json, text, structured)
        """
        try:
            # Get system instruction from config
            system_instruction = self.config.get("system_instruction", "")
            
            # Create analysis prompt
            analysis_prompt = self._create_analysis_prompt(
                analysis_type, data, specific_instructions, output_format
            )
            
            # Prepare messages
            messages = [
                SystemMessage(content=system_instruction),
                HumanMessage(content=analysis_prompt)
            ]
            
            # Get AI response
            logger.info(f"Starting AI analysis: {analysis_type} for {self.agent_id}")
            response = await self.llm.ainvoke(messages)
            
            # Process response
            result = self._process_ai_response(response.content, output_format)
            
            # Add metadata
            result["ai_analysis_metadata"] = {
                "agent_id": self.agent_id,
                "analysis_type": analysis_type,
                "model": self.config.get("model"),
                "timestamp": datetime.utcnow().isoformat(),
                "confidence_indicators": self._extract_confidence_indicators(result)
            }
            
            logger.info(f"AI analysis completed: {analysis_type}")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI analysis for {self.agent_id}: {e}")
            return {
                "error": str(e),
                "analysis_type": analysis_type,
                "fallback_used": True,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _create_analysis_prompt(self, 
                               analysis_type: str,
                               data: Dict[str, Any], 
                               specific_instructions: str,
                               output_format: str) -> str:
        """Create a comprehensive analysis prompt for Gemini"""
        
        # Data summary for context
        data_summary = self._create_data_summary(data)
        
        prompt = f"""
ANALYSIS REQUEST: {analysis_type.upper()}

FINANCIAL DATA TO ANALYZE:
{json.dumps(data_summary, indent=2)}

SPECIFIC ANALYSIS REQUIREMENTS:
{specific_instructions}

ANALYSIS FRAMEWORK:
1. **Data Assessment**: Evaluate the quality and completeness of provided data
2. **Core Analysis**: Perform deep {analysis_type} analysis using your expertise
3. **Risk Factors**: Identify key risk factors and concerns
4. **Opportunities**: Highlight potential opportunities or positive indicators
5. **Recommendations**: Provide specific, actionable recommendations
6. **Confidence Assessment**: Rate your confidence in the analysis (0.0-1.0)

OUTPUT FORMAT: {output_format.upper()}
- If JSON: Return a structured JSON object with all analysis components
- Include numerical scores/ratings where appropriate
- Provide detailed explanations for all conclusions
- Use the response format specified in your system instructions

CRITICAL REQUIREMENTS:
- Base analysis on the actual financial data provided
- Consider both quantitative metrics and qualitative factors
- Provide specific, actionable insights
- Include confidence levels for key conclusions
- Flag any data quality issues or limitations

Begin your {analysis_type} analysis now:
"""
        return prompt
    
    def _create_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a concise summary of the financial data for the prompt"""
        summary = {
            "data_sources": [],
            "key_metrics": {},
            "data_quality_indicators": {}
        }
        
        try:
            # Summarize data sources
            if "data_sources" in data:
                for source in data["data_sources"]:
                    summary["data_sources"].append({
                        "type": source.get("type", "unknown"),
                        "success": source.get("success", False),
                        "record_count": source.get("record_count", 0)
                    })
            
            # Extract key metrics
            if "data" in data:
                data_content = data["data"]
                if isinstance(data_content, dict):
                    # Common financial metrics
                    metrics_to_extract = [
                        "total_net_worth", "total_assets", "total_liabilities",
                        "credit_score", "epf_balance", "total_investment",
                        "transaction_count", "monthly_income", "monthly_expenses"
                    ]
                    
                    for metric in metrics_to_extract:
                        if metric in data_content:
                            summary["key_metrics"][metric] = data_content[metric]
            
            # Data quality indicators
            summary["data_quality_indicators"] = {
                "sources_available": len(summary["data_sources"]),
                "successful_sources": len([s for s in summary["data_sources"] if s["success"]]),
                "total_records": sum(s["record_count"] for s in summary["data_sources"]),
                "data_completeness": len(summary["key_metrics"]) / len([
                    "total_net_worth", "total_assets", "total_liabilities", "credit_score"
                ])
            }
            
        except Exception as e:
            logger.error(f"Error creating data summary: {e}")
            summary["error"] = str(e)
        
        return summary
    
    def _process_ai_response(self, response_content: str, output_format: str) -> Dict[str, Any]:
        """Process and validate AI response"""
        try:
            if output_format.lower() == "json":
                # Try to parse as JSON
                # Remove any markdown formatting
                content = response_content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                try:
                    result = json.loads(content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, wrap the response
                    result = {
                        "analysis_text": response_content,
                        "parsed_as_json": False,
                        "raw_response": response_content
                    }
            else:
                result = {
                    "analysis_text": response_content,
                    "output_format": output_format
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing AI response: {e}")
            return {
                "error": f"Response processing failed: {e}",
                "raw_response": response_content
            }
    
    def _extract_confidence_indicators(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract confidence indicators from AI analysis result"""
        confidence_indicators = {
            "overall_confidence": 0.5,  # Default
            "data_quality_impact": "medium",
            "analysis_depth": "standard"
        }
        
        try:
            # Look for confidence scores in the result
            if "confidence_score" in result:
                confidence_indicators["overall_confidence"] = result["confidence_score"]
            elif "confidence" in result:
                confidence_indicators["overall_confidence"] = result["confidence"]
            
            # Assess data quality impact
            if "data_quality_score" in result:
                score = result["data_quality_score"]
                if score > 0.8:
                    confidence_indicators["data_quality_impact"] = "low"
                elif score > 0.6:
                    confidence_indicators["data_quality_impact"] = "medium"
                else:
                    confidence_indicators["data_quality_impact"] = "high"
            
            # Assess analysis depth based on response content
            if isinstance(result, dict):
                key_count = len([k for k in result.keys() if not k.startswith("_")])
                if key_count > 8:
                    confidence_indicators["analysis_depth"] = "comprehensive"
                elif key_count > 5:
                    confidence_indicators["analysis_depth"] = "standard"
                else:
                    confidence_indicators["analysis_depth"] = "basic"
            
        except Exception as e:
            logger.error(f"Error extracting confidence indicators: {e}")
        
        return confidence_indicators
    
    async def ai_synthesize_insights(self, 
                                   agent_outputs: Dict[str, Any],
                                   synthesis_focus: str = "comprehensive") -> Dict[str, Any]:
        """
        AI-powered synthesis of insights from multiple sources
        Used by orchestrator for cross-agent analysis
        """
        try:
            synthesis_prompt = f"""
MULTI-AGENT SYNTHESIS REQUEST

AGENT OUTPUTS TO SYNTHESIZE:
{json.dumps(agent_outputs, indent=2)}

SYNTHESIS FOCUS: {synthesis_focus}

SYNTHESIS REQUIREMENTS:
1. **Cross-Agent Insights**: Identify patterns and correlations across different agent analyses
2. **Conflict Resolution**: Address any contradictions between agent findings
3. **Confidence Weighting**: Weight insights based on agent confidence levels and data quality
4. **Integrated Recommendations**: Generate cohesive recommendations that consider all agent inputs
5. **Risk-Opportunity Balance**: Balance risk management with growth opportunities
6. **Priority Ranking**: Rank recommendations by impact and urgency

OUTPUT STRUCTURE (JSON):
{{
    "synthesis_summary": "Brief overview of key findings",
    "cross_agent_insights": [
        {{
            "insight": "Description of insight",
            "supporting_agents": ["agent1", "agent2"],
            "confidence": 0.8,
            "impact": "high/medium/low"
        }}
    ],
    "integrated_recommendations": [
        {{
            "category": "risk_management/growth/operational",
            "recommendation": "Specific actionable recommendation",
            "priority": "high/medium/low",
            "timeframe": "immediate/short_term/long_term",
            "expected_impact": "Description of expected impact",
            "supporting_analysis": "Which agent analyses support this"
        }}
    ],
    "risk_assessment": {{
        "overall_risk_level": "high/medium/low",
        "key_risk_factors": ["factor1", "factor2"],
        "mitigation_priorities": ["priority1", "priority2"]
    }},
    "opportunity_assessment": {{
        "growth_potential": "high/medium/low",
        "key_opportunities": ["opportunity1", "opportunity2"],
        "implementation_priorities": ["priority1", "priority2"]
    }},
    "confidence_assessment": {{
        "synthesis_confidence": 0.8,
        "data_quality_impact": "low/medium/high",
        "analysis_completeness": 0.9
    }}
}}

Perform the synthesis analysis now:
"""
            
            messages = [
                SystemMessage(content="You are an expert financial analyst specializing in synthesizing complex multi-agent analysis results into actionable insights."),
                HumanMessage(content=synthesis_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            result = self._process_ai_response(response.content, "json")
            
            # Add synthesis metadata
            result["synthesis_metadata"] = {
                "synthesis_type": synthesis_focus,
                "agents_synthesized": list(agent_outputs.keys()),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in AI synthesis: {e}")
            return {
                "error": str(e),
                "synthesis_type": synthesis_focus,
                "timestamp": datetime.utcnow().isoformat()
            } 