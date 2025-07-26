"""
Google Cloud Functions Manager
Serverless execution environment for Financial Multi-Agent System
"""

import asyncio
import json
import logging
import zipfile
import tempfile
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Google Cloud Functions imports
from google.cloud import functions_v1
from google.cloud.functions_v1 import CloudFunctionsServiceClient
from google.cloud.functions_v1.types import CloudFunction, SourceRepository, HttpsTrigger, EventTrigger
from google.protobuf import duration_pb2

# Additional Google Cloud imports
from google.cloud import storage

from config import settings

logger = logging.getLogger(__name__)

class GoogleCloudFunctionsManager:
    """Manager for Google Cloud Functions serverless agent execution"""
    
    def __init__(self):
        self.project_id = settings.google_cloud_project
        self.location = settings.google_cloud_functions_region
        self.memory = settings.google_cloud_functions_memory
        self.timeout = settings.google_cloud_functions_timeout
        
        # Initialize clients
        self.functions_client = CloudFunctionsServiceClient()
        self.storage_client = storage.Client(project=self.project_id)
        
        # Function configurations
        self.function_templates = {
            "financial_data_processor": {
                "description": "Process financial data from Fi MCP server",
                "entry_point": "process_financial_data",
                "runtime": "python39",
                "trigger_type": "https",
                "environment_variables": {
                    "MCP_SERVER_URL": settings.mcp_server_url,
                    "GOOGLE_CLOUD_PROJECT": self.project_id
                }
            },
            "portfolio_analyzer": {
                "description": "Serverless portfolio analysis agent",
                "entry_point": "analyze_portfolio",
                "runtime": "python39",
                "trigger_type": "pubsub",
                "topic": settings.google_pubsub_topic_agent_events,
                "environment_variables": {
                    "BIGQUERY_DATASET": settings.google_bigquery_dataset
                }
            },
            "risk_calculator": {
                "description": "Serverless risk assessment calculations",
                "entry_point": "calculate_risk",
                "runtime": "python39",
                "trigger_type": "pubsub",
                "topic": settings.google_pubsub_topic_financial_data,
                "environment_variables": {
                    "FIRESTORE_COLLECTION": settings.google_firestore_collection
                }
            },
            "market_monitor": {
                "description": "Real-time market monitoring function",
                "entry_point": "monitor_market",
                "runtime": "python39",
                "trigger_type": "https",
                "environment_variables": {
                    "MONITORING_INTERVAL": "300"  # 5 minutes
                }
            },
            "alert_generator": {
                "description": "Generate and send financial alerts",
                "entry_point": "generate_alerts",
                "runtime": "python39",
                "trigger_type": "pubsub",
                "topic": settings.google_pubsub_topic_agent_events,
                "environment_variables": {
                    "ALERT_THRESHOLDS": json.dumps({
                        "risk_high": 0.8,
                        "loss_threshold": 0.1
                    })
                }
            }
        }
        
        # Track deployed functions
        self.deployed_functions = {}
        
        logger.info("✅ Google Cloud Functions Manager initialized")
    
    # === Function Deployment ===
    
    async def deploy_function(self, function_name: str, source_code: str, 
                            config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Deploy a cloud function"""
        try:
            # Use template config if not provided
            if not config:
                if function_name in self.function_templates:
                    config = self.function_templates[function_name].copy()
                else:
                    return {"success": False, "error": f"No configuration found for {function_name}"}
            
            # Upload source code
            source_url = await self._upload_source_code(function_name, source_code)
            if not source_url:
                return {"success": False, "error": "Failed to upload source code"}
            
            # Create function configuration
            function_config = self._create_function_config(function_name, source_url, config)
            
            # Deploy the function
            operation = self.functions_client.create_function(
                parent=f"projects/{self.project_id}/locations/{self.location}",
                function=function_config
            )
            
            # Wait for deployment to complete
            result = operation.result(timeout=600)  # 10 minutes timeout
            
            # Track deployed function
            self.deployed_functions[function_name] = {
                "name": result.name,
                "status": result.status.name,
                "trigger_type": config.get("trigger_type"),
                "deployed_at": datetime.utcnow().isoformat(),
                "source_url": source_url
            }
            
            logger.info(f"✅ Deployed function: {function_name}")
            
            return {
                "success": True,
                "function": {
                    "name": function_name,
                    "url": result.https_trigger.url if result.https_trigger else None,
                    "status": result.status.name
                }
            }
            
        except Exception as e:
            logger.error(f"Error deploying function {function_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _upload_source_code(self, function_name: str, source_code: str) -> Optional[str]:
        """Upload function source code to Cloud Storage"""
        try:
            bucket_name = f"{self.project_id}-functions-source"
            
            # Create bucket if it doesn't exist
            try:
                bucket = self.storage_client.bucket(bucket_name)
                if not bucket.exists():
                    bucket = self.storage_client.create_bucket(bucket_name, location=self.location)
            except Exception as e:
                logger.warning(f"Could not create/access bucket: {e}")
                return None
            
            # Create zip file with source code
            zip_filename = f"{function_name}-{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
            
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
                with zipfile.ZipFile(temp_file, 'w') as zip_file:
                    # Add main.py with the source code
                    zip_file.writestr('main.py', source_code)
                    
                    # Add requirements.txt
                    requirements = self._get_function_requirements()
                    zip_file.writestr('requirements.txt', requirements)
                
                temp_file_path = temp_file.name
            
            # Upload to Cloud Storage
            blob = bucket.blob(zip_filename)
            blob.upload_from_filename(temp_file_path)
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            return f"gs://{bucket_name}/{zip_filename}"
            
        except Exception as e:
            logger.error(f"Error uploading source code: {e}")
            return None
    
    def _get_function_requirements(self) -> str:
        """Get requirements.txt content for cloud functions"""
        return """
functions-framework==3.2.0
google-cloud-firestore==2.11.0
google-cloud-storage==2.10.0
google-cloud-pubsub==2.18.0
google-cloud-bigquery==3.11.0
google-cloud-monitoring==2.15.0
google-generativeai==0.3.2
pandas==2.0.3
numpy==1.24.3
requests==2.31.0
"""
    
    def _create_function_config(self, function_name: str, source_url: str, 
                              config: Dict[str, Any]) -> CloudFunction:
        """Create Cloud Function configuration"""
        
        function_path = f"projects/{self.project_id}/locations/{self.location}/functions/{function_name}"
        
        # Base function configuration
        function_config = CloudFunction(
            name=function_path,
            description=config.get("description", f"Financial agent function: {function_name}"),
            source_archive_url=source_url,
            entry_point=config.get("entry_point", "main"),
            runtime=config.get("runtime", "python39"),
            timeout=duration_pb2.Duration(seconds=self.timeout),
            available_memory_mb=self._parse_memory(self.memory),
            environment_variables=config.get("environment_variables", {})
        )
        
        # Configure trigger
        trigger_type = config.get("trigger_type", "https")
        
        if trigger_type == "https":
            function_config.https_trigger = HttpsTrigger()
        elif trigger_type == "pubsub":
            topic = config.get("topic")
            if topic:
                topic_path = f"projects/{self.project_id}/topics/{topic}"
                function_config.event_trigger = EventTrigger(
                    event_type="providers/cloud.pubsub/eventTypes/topic.publish",
                    resource=topic_path
                )
        
        return function_config
    
    def _parse_memory(self, memory_str: str) -> int:
        """Parse memory string to MB integer"""
        if memory_str.endswith('Mi'):
            return int(memory_str[:-2])
        elif memory_str.endswith('Gi'):
            return int(memory_str[:-2]) * 1024
        else:
            return 512  # Default
    
    # === Function Management ===
    
    async def update_function(self, function_name: str, new_source_code: str) -> Dict[str, Any]:
        """Update an existing cloud function"""
        try:
            if function_name not in self.deployed_functions:
                return {"success": False, "error": f"Function {function_name} not found"}
            
            # Upload new source code
            source_url = await self._upload_source_code(function_name, new_source_code)
            if not source_url:
                return {"success": False, "error": "Failed to upload new source code"}
            
            # Get current function
            function_path = self.deployed_functions[function_name]["name"]
            current_function = self.functions_client.get_function(name=function_path)
            
            # Update source
            current_function.source_archive_url = source_url
            
            # Update the function
            operation = self.functions_client.update_function(function=current_function)
            result = operation.result(timeout=600)
            
            # Update tracking
            self.deployed_functions[function_name]["source_url"] = source_url
            self.deployed_functions[function_name]["updated_at"] = datetime.utcnow().isoformat()
            
            logger.info(f"✅ Updated function: {function_name}")
            
            return {
                "success": True,
                "function_name": function_name,
                "status": result.status.name
            }
            
        except Exception as e:
            logger.error(f"Error updating function {function_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_function(self, function_name: str) -> Dict[str, Any]:
        """Delete a cloud function"""
        try:
            if function_name not in self.deployed_functions:
                return {"success": False, "error": f"Function {function_name} not found"}
            
            function_path = self.deployed_functions[function_name]["name"]
            
            # Delete the function
            operation = self.functions_client.delete_function(name=function_path)
            operation.result(timeout=300)
            
            # Remove from tracking
            del self.deployed_functions[function_name]
            
            logger.info(f"✅ Deleted function: {function_name}")
            
            return {"success": True, "function_name": function_name}
            
        except Exception as e:
            logger.error(f"Error deleting function {function_name}: {e}")
            return {"success": False, "error": str(e)}
    
    # === Function Invocation ===
    
    async def invoke_function(self, function_name: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """Invoke a cloud function"""
        try:
            if function_name not in self.deployed_functions:
                return {"success": False, "error": f"Function {function_name} not found"}
            
            function_info = self.deployed_functions[function_name]
            
            # For HTTPS functions, we would make HTTP request
            if function_info["trigger_type"] == "https":
                # This would require the function URL and HTTP client
                return {"success": False, "error": "HTTPS function invocation not implemented in this example"}
            
            # For Pub/Sub functions, publish message to trigger
            elif function_info["trigger_type"] == "pubsub":
                from services.google_cloud_manager import google_cloud_manager
                
                await google_cloud_manager.publish_agent_event(
                    agent_id=function_name,
                    event_type="function_invocation",
                    event_data=payload or {}
                )
                
                return {
                    "success": True,
                    "message": f"Published trigger event for {function_name}"
                }
            
            return {"success": False, "error": "Unknown trigger type"}
            
        except Exception as e:
            logger.error(f"Error invoking function {function_name}: {e}")
            return {"success": False, "error": str(e)}
    
    # === Pre-built Function Templates ===
    
    def get_financial_data_processor_code(self) -> str:
        """Get source code for financial data processor function"""
        return '''
import json
import logging
from google.cloud import firestore
from google.cloud import pubsub_v1
import requests
import os

def process_financial_data(request):
    """Process financial data from Fi MCP server"""
    try:
        # Initialize clients
        db = firestore.Client()
        publisher = pubsub_v1.PublisherClient()
        
        # Get MCP server URL
        mcp_url = os.environ.get('MCP_SERVER_URL', 'http://localhost:8080')
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        
        # Get request data
        request_json = request.get_json(silent=True)
        phone_number = request_json.get('phone_number') if request_json else None
        
        if not phone_number:
            return {'error': 'Phone number required'}, 400
        
        # Fetch data from Fi MCP server
        endpoints = [
            f'{mcp_url}/fetch_bank_transactions?phone={phone_number}',
            f'{mcp_url}/fetch_net_worth?phone={phone_number}',
            f'{mcp_url}/fetch_mf_transactions?phone={phone_number}'
        ]
        
        collected_data = {}
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=30)
                if response.status_code == 200:
                    data_type = endpoint.split('/')[-1].split('?')[0]
                    collected_data[data_type] = response.json()
            except Exception as e:
                logging.error(f"Error fetching from {endpoint}: {e}")
        
        # Store in Firestore
        doc_ref = db.collection('financial_data').document(phone_number)
        doc_ref.set({
            'data': collected_data,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'processed_by': 'cloud_function'
        }, merge=True)
        
        # Publish completion event
        topic_path = publisher.topic_path(project_id, 'financial-data-updates')
        message_data = json.dumps({
            'phone_number': phone_number,
            'data_types': list(collected_data.keys()),
            'timestamp': str(firestore.SERVER_TIMESTAMP)
        }).encode('utf-8')
        
        publisher.publish(topic_path, message_data)
        
        return {
            'success': True,
            'phone_number': phone_number,
            'data_types_collected': list(collected_data.keys())
        }
        
    except Exception as e:
        logging.error(f"Error processing financial data: {e}")
        return {'error': str(e)}, 500
'''
    
    def get_portfolio_analyzer_code(self) -> str:
        """Get source code for portfolio analyzer function"""
        return '''
import json
import logging
from google.cloud import firestore
from google.cloud import bigquery
import pandas as pd
import numpy as np

def analyze_portfolio(event, context):
    """Analyze portfolio performance and risk"""
    try:
        # Initialize clients
        db = firestore.Client()
        bq_client = bigquery.Client()
        
        # Parse Pub/Sub message
        message_data = json.loads(event['data'].decode('utf-8'))
        phone_number = message_data.get('phone_number')
        
        if not phone_number:
            logging.error("No phone number in message")
            return
        
        # Get financial data from Firestore
        doc_ref = db.collection('financial_data').document(phone_number)
        doc = doc_ref.get()
        
        if not doc.exists:
            logging.error(f"No data found for {phone_number}")
            return
        
        data = doc.to_dict()
        
        # Perform portfolio analysis
        analysis_results = {
            'phone_number': phone_number,
            'analysis_timestamp': firestore.SERVER_TIMESTAMP,
            'total_assets': 0,
            'diversification_score': 0,
            'risk_level': 'medium',
            'recommendations': []
        }
        
        # Calculate total assets
        if 'fetch_net_worth' in data.get('data', {}):
            net_worth_data = data['data']['fetch_net_worth']
            if isinstance(net_worth_data, dict) and 'total_assets' in net_worth_data:
                analysis_results['total_assets'] = net_worth_data['total_assets']
        
        # Simple diversification analysis
        if 'fetch_mf_transactions' in data.get('data', {}):
            mf_data = data['data']['fetch_mf_transactions']
            if isinstance(mf_data, list):
                unique_funds = len(set(fund.get('fund_name', '') for fund in mf_data))
                analysis_results['diversification_score'] = min(unique_funds / 10.0, 1.0)
        
        # Store analysis results
        analysis_ref = db.collection('portfolio_analysis').document(phone_number)
        analysis_ref.set(analysis_results, merge=True)
        
        # Store in BigQuery for analytics
        dataset_id = 'financial_analytics'
        table_id = 'portfolio_analysis'
        
        table_ref = bq_client.dataset(dataset_id).table(table_id)
        
        rows_to_insert = [{
            'phone_number': phone_number,
            'analysis_date': str(analysis_results['analysis_timestamp']),
            'total_assets': analysis_results['total_assets'],
            'diversification_score': analysis_results['diversification_score'],
            'risk_level': analysis_results['risk_level']
        }]
        
        errors = bq_client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            logging.error(f"BigQuery insert errors: {errors}")
        
        logging.info(f"Portfolio analysis completed for {phone_number}")
        
    except Exception as e:
        logging.error(f"Error in portfolio analysis: {e}")
'''
    
    # === Deployment Management ===
    
    async def deploy_all_financial_functions(self) -> Dict[str, Any]:
        """Deploy all pre-built financial functions"""
        try:
            results = {}
            
            # Deploy financial data processor
            data_processor_code = self.get_financial_data_processor_code()
            results["financial_data_processor"] = await self.deploy_function(
                "financial_data_processor", 
                data_processor_code
            )
            
            # Deploy portfolio analyzer
            portfolio_analyzer_code = self.get_portfolio_analyzer_code()
            results["portfolio_analyzer"] = await self.deploy_function(
                "portfolio_analyzer", 
                portfolio_analyzer_code
            )
            
            successful_deployments = sum(1 for r in results.values() if r.get("success"))
            
            logger.info(f"✅ Deployed {successful_deployments}/{len(results)} financial functions")
            
            return {
                "success": True,
                "deployed_functions": successful_deployments,
                "total_functions": len(results),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error deploying financial functions: {e}")
            return {"success": False, "error": str(e)}
    
    # === Monitoring and Status ===
    
    async def get_function_logs(self, function_name: str, limit: int = 100) -> Dict[str, Any]:
        """Get logs for a specific function"""
        try:
            if function_name not in self.deployed_functions:
                return {"success": False, "error": f"Function {function_name} not found"}
            
            # This would integrate with Cloud Logging
            # For now, return placeholder
            return {
                "success": True,
                "function_name": function_name,
                "logs": f"Logs for {function_name} (limit: {limit})",
                "message": "Log retrieval not fully implemented in this example"
            }
            
        except Exception as e:
            logger.error(f"Error getting function logs: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_functions_status(self) -> Dict[str, Any]:
        """Get status of all deployed functions"""
        try:
            functions_list = []
            
            # List all functions in the project
            parent = f"projects/{self.project_id}/locations/{self.location}"
            
            for function in self.functions_client.list_functions(parent=parent):
                function_name = function.name.split("/")[-1]
                
                function_info = {
                    "name": function_name,
                    "status": function.status.name,
                    "runtime": function.runtime,
                    "memory": f"{function.available_memory_mb}MB",
                    "trigger_type": "https" if function.https_trigger else "event",
                    "update_time": function.update_time.strftime("%Y-%m-%d %H:%M:%S") if function.update_time else None
                }
                
                if function.https_trigger:
                    function_info["url"] = function.https_trigger.url
                
                functions_list.append(function_info)
            
            return {
                "success": True,
                "functions": functions_list,
                "total_functions": len(functions_list),
                "project_id": self.project_id,
                "location": self.location
            }
            
        except Exception as e:
            logger.error(f"Error getting functions status: {e}")
            return {"success": False, "error": str(e)}

# Global instance
google_cloud_functions_manager = GoogleCloudFunctionsManager() 