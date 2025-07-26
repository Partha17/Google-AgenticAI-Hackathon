"""
Google Cloud Services Manager
Comprehensive integration of all Google Cloud components for the Financial Multi-Agent System
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from contextlib import asynccontextmanager

# Google Cloud imports
from google.cloud import firestore
from google.cloud import storage
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from google.cloud import scheduler
from google.cloud import pubsub_v1
from google.cloud import secretmanager
from google.cloud import bigquery
from google.cloud import functions_v1
from google.auth import default
from google.oauth2 import service_account

# Vertex AI imports
from google.cloud import aiplatform
from google.cloud.aiplatform import vertex_ai

# Additional imports
import httpx
from config import settings

logger = logging.getLogger(__name__)

class GoogleCloudManager:
    """Comprehensive manager for all Google Cloud services used in the financial system"""
    
    def __init__(self):
        self.project_id = settings.google_cloud_project
        self.location = settings.google_cloud_location
        self.initialized_services = {}
        self.monitoring_client = None
        self.logging_client = None
        
        # Initialize services
        self._initialize_core_services()
    
    def _initialize_core_services(self):
        """Initialize core Google Cloud services"""
        try:
            # Set up default credentials
            credentials, _ = default()
            
            # Initialize Firestore
            if settings.google_firestore_database:
                self.firestore_client = firestore.Client(
                    project=self.project_id,
                    database=settings.google_firestore_database
                )
                self.initialized_services['firestore'] = True
                logger.info("✅ Firestore initialized")
            
            # Initialize Cloud Storage
            if settings.google_cloud_storage_bucket:
                self.storage_client = storage.Client(project=self.project_id)
                self.bucket = self.storage_client.bucket(settings.google_cloud_storage_bucket)
                self.initialized_services['storage'] = True
                logger.info("✅ Cloud Storage initialized")
            
            # Initialize Cloud Monitoring
            if settings.google_cloud_monitoring_enabled:
                self.monitoring_client = monitoring_v3.MetricServiceClient()
                self.initialized_services['monitoring'] = True
                logger.info("✅ Cloud Monitoring initialized")
            
            # Initialize Cloud Logging
            if settings.google_cloud_logging_enabled:
                self.logging_client = cloud_logging.Client(project=self.project_id)
                self.logging_client.setup_logging()
                self.initialized_services['logging'] = True
                logger.info("✅ Cloud Logging initialized")
            
            # Initialize Pub/Sub
            if settings.google_pubsub_project:
                self.publisher = pubsub_v1.PublisherClient()
                self.subscriber = pubsub_v1.SubscriberClient()
                self.initialized_services['pubsub'] = True
                logger.info("✅ Pub/Sub initialized")
            
            # Initialize BigQuery
            if settings.google_bigquery_dataset:
                self.bigquery_client = bigquery.Client(project=self.project_id)
                self.initialized_services['bigquery'] = True
                logger.info("✅ BigQuery initialized")
            
            # Initialize Secret Manager
            if settings.google_secret_manager_enabled:
                self.secret_client = secretmanager.SecretManagerServiceClient()
                self.initialized_services['secret_manager'] = True
                logger.info("✅ Secret Manager initialized")
            
            # Initialize Vertex AI
            vertex_ai.init(project=self.project_id, location=self.location)
            self.initialized_services['vertex_ai'] = True
            logger.info("✅ Vertex AI initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Google Cloud services: {e}")
    
    # === Firestore Real-time Data Management ===
    
    async def store_financial_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Store financial data in Firestore with real-time sync"""
        try:
            if 'firestore' not in self.initialized_services:
                return False
            
            collection_ref = self.firestore_client.collection(settings.google_firestore_collection)
            doc_ref = collection_ref.document(user_id)
            
            # Add timestamp and metadata
            enhanced_data = {
                **data,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'last_updated': datetime.utcnow().isoformat(),
                'version': data.get('version', 1) + 1
            }
            
            # Store with merge to preserve existing data
            doc_ref.set(enhanced_data, merge=True)
            
            # Publish to Pub/Sub for real-time updates
            if 'pubsub' in self.initialized_services:
                await self._publish_data_update(user_id, enhanced_data)
            
            logger.info(f"✅ Financial data stored for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing financial data: {e}")
            return False
    
    async def get_financial_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve financial data from Firestore"""
        try:
            if 'firestore' not in self.initialized_services:
                return None
            
            collection_ref = self.firestore_client.collection(settings.google_firestore_collection)
            doc_ref = collection_ref.document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving financial data: {e}")
            return None
    
    def setup_real_time_listener(self, user_id: str, callback):
        """Set up real-time listener for data changes"""
        try:
            if 'firestore' not in self.initialized_services:
                return None
            
            collection_ref = self.firestore_client.collection(settings.google_firestore_collection)
            doc_ref = collection_ref.document(user_id)
            
            # Create real-time listener
            watch = doc_ref.on_snapshot(callback)
            return watch
            
        except Exception as e:
            logger.error(f"Error setting up real-time listener: {e}")
            return None
    
    # === Cloud Storage for File Management ===
    
    async def upload_file(self, file_path: str, destination_blob_name: str, content: Union[str, bytes]) -> bool:
        """Upload file to Google Cloud Storage"""
        try:
            if 'storage' not in self.initialized_services:
                return False
            
            blob_name = f"{settings.google_cloud_storage_prefix}{destination_blob_name}"
            blob = self.bucket.blob(blob_name)
            
            if isinstance(content, str):
                blob.upload_from_string(content)
            else:
                blob.upload_from_string(content)
            
            logger.info(f"✅ File uploaded to {blob_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    async def download_file(self, blob_name: str) -> Optional[bytes]:
        """Download file from Google Cloud Storage"""
        try:
            if 'storage' not in self.initialized_services:
                return None
            
            full_blob_name = f"{settings.google_cloud_storage_prefix}{blob_name}"
            blob = self.bucket.blob(full_blob_name)
            
            if blob.exists():
                return blob.download_as_bytes()
            return None
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return None
    
    # === Cloud Monitoring & Metrics ===
    
    async def record_custom_metric(self, metric_name: str, value: float, labels: Dict[str, str] = None):
        """Record custom metric to Cloud Monitoring"""
        try:
            if 'monitoring' not in self.initialized_services:
                return False
            
            project_name = f"projects/{self.project_id}"
            metric_type = f"custom.googleapis.com/{settings.google_cloud_metrics_prefix}/{metric_name}"
            
            # Create time series data
            interval = monitoring_v3.TimeInterval({
                "end_time": {"seconds": int(datetime.utcnow().timestamp())}
            })
            
            point = monitoring_v3.Point({
                "interval": interval,
                "value": {"double_value": value}
            })
            
            # Create metric series
            series = monitoring_v3.TimeSeries()
            series.metric.type = metric_type
            series.resource.type = "global"
            
            if labels:
                for key, label_value in labels.items():
                    series.metric.labels[key] = label_value
            
            series.points = [point]
            
            # Write time series
            self.monitoring_client.create_time_series(
                name=project_name,
                time_series=[series]
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recording metric: {e}")
            return False
    
    async def get_system_metrics(self, hours_back: int = 24) -> Dict[str, Any]:
        """Retrieve system metrics from Cloud Monitoring"""
        try:
            if 'monitoring' not in self.initialized_services:
                return {}
            
            project_name = f"projects/{self.project_id}"
            
            # Define time range
            now = datetime.utcnow()
            start_time = now - timedelta(hours=hours_back)
            
            interval = monitoring_v3.TimeInterval({
                "start_time": {"seconds": int(start_time.timestamp())},
                "end_time": {"seconds": int(now.timestamp())}
            })
            
            # Query metrics
            request = monitoring_v3.ListTimeSeriesRequest(
                name=project_name,
                filter=f'metric.type=starts_with("custom.googleapis.com/{settings.google_cloud_metrics_prefix}")',
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            )
            
            results = self.monitoring_client.list_time_series(request=request)
            
            metrics = {}
            for result in results:
                metric_name = result.metric.type.split('/')[-1]
                metrics[metric_name] = {
                    'labels': dict(result.metric.labels),
                    'points': [(point.interval.end_time.seconds, point.value.double_value) 
                              for point in result.points]
                }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error retrieving metrics: {e}")
            return {}
    
    # === Pub/Sub for Real-time Events ===
    
    async def _publish_data_update(self, user_id: str, data: Dict[str, Any]):
        """Publish data update to Pub/Sub"""
        try:
            if 'pubsub' not in self.initialized_services:
                return
            
            topic_path = self.publisher.topic_path(
                settings.google_pubsub_project,
                settings.google_pubsub_topic_financial_data
            )
            
            message_data = json.dumps({
                'user_id': user_id,
                'data': data,
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': 'financial_data_update'
            }).encode('utf-8')
            
            future = self.publisher.publish(topic_path, message_data)
            await asyncio.wrap_future(future)
            
        except Exception as e:
            logger.error(f"Error publishing to Pub/Sub: {e}")
    
    async def publish_agent_event(self, agent_id: str, event_type: str, event_data: Dict[str, Any]):
        """Publish agent event to Pub/Sub"""
        try:
            if 'pubsub' not in self.initialized_services:
                return
            
            topic_path = self.publisher.topic_path(
                settings.google_pubsub_project,
                settings.google_pubsub_topic_agent_events
            )
            
            message_data = json.dumps({
                'agent_id': agent_id,
                'event_type': event_type,
                'event_data': event_data,
                'timestamp': datetime.utcnow().isoformat()
            }).encode('utf-8')
            
            future = self.publisher.publish(topic_path, message_data)
            await asyncio.wrap_future(future)
            
        except Exception as e:
            logger.error(f"Error publishing agent event: {e}")
    
    # === BigQuery Analytics ===
    
    async def store_transaction_analytics(self, transactions: List[Dict[str, Any]]) -> bool:
        """Store transaction data in BigQuery for analytics"""
        try:
            if 'bigquery' not in self.initialized_services:
                return False
            
            table_ref = self.bigquery_client.dataset(settings.google_bigquery_dataset).table(
                settings.google_bigquery_table_transactions
            )
            
            # Stream insert if enabled, otherwise batch insert
            if settings.google_bigquery_streaming_enabled:
                errors = self.bigquery_client.insert_rows_json(table_ref, transactions)
                if errors:
                    logger.error(f"BigQuery streaming errors: {errors}")
                    return False
            else:
                job = self.bigquery_client.load_table_from_json(transactions, table_ref)
                job.result()  # Wait for completion
            
            logger.info(f"✅ Stored {len(transactions)} transactions in BigQuery")
            return True
            
        except Exception as e:
            logger.error(f"Error storing BigQuery analytics: {e}")
            return False
    
    async def store_agent_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Store agent performance metrics in BigQuery"""
        try:
            if 'bigquery' not in self.initialized_services:
                return False
            
            table_ref = self.bigquery_client.dataset(settings.google_bigquery_dataset).table(
                settings.google_bigquery_table_agent_metrics
            )
            
            # Prepare metrics data
            metrics_row = {
                **metrics,
                'timestamp': datetime.utcnow().isoformat(),
                'project_id': self.project_id
            }
            
            errors = self.bigquery_client.insert_rows_json(table_ref, [metrics_row])
            if errors:
                logger.error(f"BigQuery metrics storage errors: {errors}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing agent metrics: {e}")
            return False
    
    # === Secret Management ===
    
    async def get_secret(self, secret_id: str, version: str = "latest") -> Optional[str]:
        """Retrieve secret from Google Secret Manager"""
        try:
            if 'secret_manager' not in self.initialized_services:
                return None
            
            project_id = settings.google_secret_manager_project or self.project_id
            name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
            
            response = self.secret_client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
            
        except Exception as e:
            logger.error(f"Error retrieving secret {secret_id}: {e}")
            return None
    
    # === System Health & Status ===
    
    async def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all Google Cloud services"""
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'project_id': self.project_id,
            'location': self.location,
            'services': {},
            'overall_health': 'healthy'
        }
        
        # Check each service
        for service_name, is_initialized in self.initialized_services.items():
            service_status = {
                'initialized': is_initialized,
                'status': 'healthy' if is_initialized else 'not_configured',
                'details': {}
            }
            
            # Add service-specific health checks
            try:
                if service_name == 'firestore' and is_initialized:
                    # Test Firestore connectivity
                    test_doc = self.firestore_client.collection('health_check').document('test')
                    test_doc.set({'timestamp': firestore.SERVER_TIMESTAMP})
                    service_status['details']['connectivity'] = 'ok'
                
                elif service_name == 'storage' and is_initialized:
                    # Test Storage connectivity
                    if self.bucket.exists():
                        service_status['details']['bucket_accessible'] = True
                    
                elif service_name == 'monitoring' and is_initialized:
                    service_status['details']['metrics_available'] = True
                
                elif service_name == 'bigquery' and is_initialized:
                    # Test BigQuery connectivity
                    datasets = list(self.bigquery_client.list_datasets())
                    service_status['details']['datasets_accessible'] = len(datasets) >= 0
                
            except Exception as e:
                service_status['status'] = 'error'
                service_status['error'] = str(e)
                status['overall_health'] = 'degraded'
            
            status['services'][service_name] = service_status
        
        return status

# Global instance
google_cloud_manager = GoogleCloudManager() 