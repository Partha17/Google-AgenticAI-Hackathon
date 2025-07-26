"""
Google Cloud Scheduler Manager
Automated workflow scheduling for the Financial Multi-Agent System
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import croniter

# Google Cloud Scheduler imports
from google.cloud import scheduler
from google.cloud.scheduler_v1 import CloudSchedulerClient
from google.cloud.scheduler_v1.types import Job, PubsubTarget, HttpTarget, AppEngineHttpTarget
from google.protobuf import timestamp_pb2

# Additional imports
from config import settings

logger = logging.getLogger(__name__)

class GoogleSchedulerManager:
    """Manager for Google Cloud Scheduler automated workflows"""
    
    def __init__(self):
        self.project_id = settings.google_cloud_project
        self.location = settings.google_cloud_scheduler_location
        self.timezone = settings.google_cloud_scheduler_timezone
        
        # Initialize scheduler client
        self.client = CloudSchedulerClient()
        self.parent = f"projects/{self.project_id}/locations/{self.location}"
        
        # Track scheduled jobs
        self.scheduled_jobs = {}
        
        # Pre-defined financial workflows
        self.financial_workflows = {
            "daily_data_collection": {
                "schedule": "0 9 * * MON-FRI",  # 9 AM weekdays
                "description": "Daily financial data collection from Fi MCP server",
                "target_type": "pubsub",
                "payload": {"workflow": "collect_financial_data", "scope": "daily"}
            },
            "weekly_portfolio_analysis": {
                "schedule": "0 10 * * MON",  # 10 AM every Monday
                "description": "Weekly comprehensive portfolio analysis",
                "target_type": "pubsub",
                "payload": {"workflow": "comprehensive_analysis", "scope": "weekly"}
            },
            "monthly_risk_assessment": {
                "schedule": "0 11 1 * *",  # 11 AM first day of month
                "description": "Monthly risk assessment and stress testing",
                "target_type": "pubsub",
                "payload": {"workflow": "risk_assessment", "scope": "monthly"}
            },
            "quarterly_rebalancing": {
                "schedule": "0 12 1 */3 *",  # 12 PM first day of quarter
                "description": "Quarterly portfolio rebalancing analysis",
                "target_type": "pubsub",
                "payload": {"workflow": "portfolio_rebalancing", "scope": "quarterly"}
            },
            "real_time_monitoring": {
                "schedule": "*/15 * * * *",  # Every 15 minutes
                "description": "Real-time market monitoring and alerts",
                "target_type": "pubsub",
                "payload": {"workflow": "market_monitoring", "scope": "realtime"}
            },
            "end_of_day_reporting": {
                "schedule": "0 17 * * MON-FRI",  # 5 PM weekdays
                "description": "End of day financial reporting and analysis",
                "target_type": "pubsub",
                "payload": {"workflow": "end_of_day_report", "scope": "daily"}
            }
        }
        
        logger.info("✅ Google Scheduler Manager initialized")
    
    # === Job Creation and Management ===
    
    async def create_scheduled_job(self, job_name: str, schedule: str, target_config: Dict[str, Any], 
                                 description: str = "", timezone: str = None) -> Dict[str, Any]:
        """Create a new scheduled job"""
        try:
            job_id = f"financial-{job_name}"
            job_path = f"{self.parent}/jobs/{job_id}"
            
            # Use default timezone if not specified
            if not timezone:
                timezone = self.timezone
            
            # Create job configuration
            job = Job(
                name=job_path,
                description=description or f"Financial workflow: {job_name}",
                schedule=schedule,
                time_zone=timezone
            )
            
            # Configure target based on type
            target_type = target_config.get("type", "pubsub")
            
            if target_type == "pubsub":
                job.pubsub_target = self._create_pubsub_target(target_config)
            elif target_type == "http":
                job.http_target = self._create_http_target(target_config)
            elif target_type == "app_engine":
                job.app_engine_http_target = self._create_app_engine_target(target_config)
            else:
                return {"success": False, "error": f"Unsupported target type: {target_type}"}
            
            # Create the job
            created_job = self.client.create_job(parent=self.parent, job=job)
            
            # Track the job
            self.scheduled_jobs[job_name] = {
                "job_id": job_id,
                "job_path": job_path,
                "schedule": schedule,
                "target_config": target_config,
                "created_at": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            logger.info(f"✅ Created scheduled job: {job_name}")
            
            return {
                "success": True,
                "job": {
                    "name": job_name,
                    "job_id": job_id,
                    "job_path": job_path,
                    "schedule": schedule,
                    "next_run": self._calculate_next_run(schedule, timezone)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating scheduled job {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_pubsub_target(self, config: Dict[str, Any]) -> PubsubTarget:
        """Create Pub/Sub target configuration"""
        topic_name = config.get("topic", settings.google_pubsub_topic_agent_events)
        topic_path = f"projects/{self.project_id}/topics/{topic_name}"
        
        payload = config.get("payload", {})
        
        return PubsubTarget(
            topic_name=topic_path,
            data=json.dumps(payload).encode('utf-8'),
            attributes=config.get("attributes", {})
        )
    
    def _create_http_target(self, config: Dict[str, Any]) -> HttpTarget:
        """Create HTTP target configuration"""
        return HttpTarget(
            uri=config.get("url"),
            http_method=config.get("method", "POST"),
            headers=config.get("headers", {}),
            body=json.dumps(config.get("payload", {})).encode('utf-8')
        )
    
    def _create_app_engine_target(self, config: Dict[str, Any]) -> AppEngineHttpTarget:
        """Create App Engine target configuration"""
        return AppEngineHttpTarget(
            relative_uri=config.get("relative_uri", "/"),
            http_method=config.get("method", "POST"),
            headers=config.get("headers", {}),
            body=json.dumps(config.get("payload", {})).encode('utf-8')
        )
    
    # === Financial Workflow Management ===
    
    async def setup_financial_workflows(self) -> Dict[str, Any]:
        """Set up all pre-defined financial workflows"""
        try:
            results = {}
            
            for workflow_name, workflow_config in self.financial_workflows.items():
                target_config = {
                    "type": workflow_config["target_type"],
                    "topic": settings.google_pubsub_topic_agent_events,
                    "payload": workflow_config["payload"]
                }
                
                result = await self.create_scheduled_job(
                    job_name=workflow_name,
                    schedule=workflow_config["schedule"],
                    target_config=target_config,
                    description=workflow_config["description"]
                )
                
                results[workflow_name] = result
            
            successful_workflows = sum(1 for r in results.values() if r.get("success"))
            
            logger.info(f"✅ Set up {successful_workflows}/{len(self.financial_workflows)} financial workflows")
            
            return {
                "success": True,
                "workflows_created": successful_workflows,
                "total_workflows": len(self.financial_workflows),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error setting up financial workflows: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_custom_workflow(self, workflow_name: str, cron_schedule: str, 
                                   workflow_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create custom financial workflow"""
        try:
            # Validate cron schedule
            if not self._validate_cron_schedule(cron_schedule):
                return {"success": False, "error": "Invalid cron schedule format"}
            
            # Prepare payload
            payload = {
                "workflow": workflow_type,
                "parameters": parameters or {},
                "created_by": "user",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            target_config = {
                "type": "pubsub",
                "topic": settings.google_pubsub_topic_agent_events,
                "payload": payload
            }
            
            result = await self.create_scheduled_job(
                job_name=f"custom_{workflow_name}",
                schedule=cron_schedule,
                target_config=target_config,
                description=f"Custom workflow: {workflow_name}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating custom workflow {workflow_name}: {e}")
            return {"success": False, "error": str(e)}
    
    # === Job Management ===
    
    async def pause_job(self, job_name: str) -> Dict[str, Any]:
        """Pause a scheduled job"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Pause the job
            self.client.pause_job(name=job_path)
            
            # Update status
            self.scheduled_jobs[job_name]["status"] = "paused"
            
            logger.info(f"✅ Paused job: {job_name}")
            return {"success": True, "status": "paused"}
            
        except Exception as e:
            logger.error(f"Error pausing job {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def resume_job(self, job_name: str) -> Dict[str, Any]:
        """Resume a paused job"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Resume the job
            self.client.resume_job(name=job_path)
            
            # Update status
            self.scheduled_jobs[job_name]["status"] = "active"
            
            logger.info(f"✅ Resumed job: {job_name}")
            return {"success": True, "status": "active"}
            
        except Exception as e:
            logger.error(f"Error resuming job {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_job(self, job_name: str) -> Dict[str, Any]:
        """Delete a scheduled job"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Delete the job
            self.client.delete_job(name=job_path)
            
            # Remove from tracking
            del self.scheduled_jobs[job_name]
            
            logger.info(f"✅ Deleted job: {job_name}")
            return {"success": True, "status": "deleted"}
            
        except Exception as e:
            logger.error(f"Error deleting job {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def run_job_now(self, job_name: str) -> Dict[str, Any]:
        """Manually trigger a job to run immediately"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Run the job immediately
            self.client.run_job(name=job_path)
            
            logger.info(f"✅ Manually triggered job: {job_name}")
            return {"success": True, "status": "triggered"}
            
        except Exception as e:
            logger.error(f"Error running job {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    # === Job Monitoring ===
    
    async def get_job_status(self, job_name: str) -> Dict[str, Any]:
        """Get detailed status of a specific job"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Get job details from Cloud Scheduler
            job = self.client.get_job(name=job_path)
            
            job_info = {
                "name": job_name,
                "schedule": job.schedule,
                "time_zone": job.time_zone,
                "state": job.state.name,
                "description": job.description,
                "last_attempt_time": None,
                "next_run_time": None
            }
            
            # Add execution times if available
            if job.last_attempt_time:
                job_info["last_attempt_time"] = job.last_attempt_time.strftime("%Y-%m-%d %H:%M:%S")
            
            if job.schedule:
                job_info["next_run_time"] = self._calculate_next_run(job.schedule, job.time_zone)
            
            return {
                "success": True,
                "job": job_info
            }
            
        except Exception as e:
            logger.error(f"Error getting job status {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def list_all_jobs(self) -> Dict[str, Any]:
        """List all scheduled jobs"""
        try:
            # Get jobs from Cloud Scheduler
            jobs = self.client.list_jobs(parent=self.parent)
            
            job_list = []
            for job in jobs:
                job_name = job.name.split("/")[-1]
                
                job_info = {
                    "name": job_name,
                    "schedule": job.schedule,
                    "state": job.state.name,
                    "description": job.description,
                    "time_zone": job.time_zone
                }
                
                if job.last_attempt_time:
                    job_info["last_run"] = job.last_attempt_time.strftime("%Y-%m-%d %H:%M:%S")
                
                if job.schedule:
                    job_info["next_run"] = self._calculate_next_run(job.schedule, job.time_zone)
                
                job_list.append(job_info)
            
            return {
                "success": True,
                "jobs": job_list,
                "total_jobs": len(job_list)
            }
            
        except Exception as e:
            logger.error(f"Error listing jobs: {e}")
            return {"success": False, "error": str(e)}
    
    # === Schedule Management ===
    
    async def update_job_schedule(self, job_name: str, new_schedule: str) -> Dict[str, Any]:
        """Update the schedule of an existing job"""
        try:
            if job_name not in self.scheduled_jobs:
                return {"success": False, "error": f"Job {job_name} not found"}
            
            if not self._validate_cron_schedule(new_schedule):
                return {"success": False, "error": "Invalid cron schedule format"}
            
            job_path = self.scheduled_jobs[job_name]["job_path"]
            
            # Get current job
            job = self.client.get_job(name=job_path)
            
            # Update schedule
            job.schedule = new_schedule
            
            # Update the job
            updated_job = self.client.update_job(job=job)
            
            # Update local tracking
            self.scheduled_jobs[job_name]["schedule"] = new_schedule
            
            logger.info(f"✅ Updated schedule for job {job_name}: {new_schedule}")
            
            return {
                "success": True,
                "job_name": job_name,
                "new_schedule": new_schedule,
                "next_run": self._calculate_next_run(new_schedule, job.time_zone)
            }
            
        except Exception as e:
            logger.error(f"Error updating job schedule {job_name}: {e}")
            return {"success": False, "error": str(e)}
    
    # === Utility Methods ===
    
    def _validate_cron_schedule(self, schedule: str) -> bool:
        """Validate cron schedule format"""
        try:
            croniter.croniter(schedule)
            return True
        except Exception:
            return False
    
    def _calculate_next_run(self, schedule: str, timezone: str = None) -> str:
        """Calculate next run time for a cron schedule"""
        try:
            if not timezone:
                timezone = self.timezone
            
            cron = croniter.croniter(schedule, datetime.utcnow())
            next_run = cron.get_next(datetime)
            return next_run.strftime("%Y-%m-%d %H:%M:%S UTC")
            
        except Exception as e:
            logger.error(f"Error calculating next run: {e}")
            return "Unknown"
    
    # === Workflow Templates ===
    
    def get_workflow_templates(self) -> Dict[str, Any]:
        """Get available workflow templates"""
        templates = {
            "data_collection": {
                "name": "Data Collection",
                "description": "Collect financial data from various sources",
                "suggested_schedules": [
                    {"name": "Hourly", "cron": "0 * * * *"},
                    {"name": "Daily at 9 AM", "cron": "0 9 * * *"},
                    {"name": "Weekdays at market open", "cron": "30 9 * * MON-FRI"}
                ]
            },
            "portfolio_analysis": {
                "name": "Portfolio Analysis",
                "description": "Comprehensive portfolio performance analysis",
                "suggested_schedules": [
                    {"name": "Daily after market close", "cron": "0 17 * * MON-FRI"},
                    {"name": "Weekly on Monday", "cron": "0 10 * * MON"},
                    {"name": "Monthly on 1st", "cron": "0 11 1 * *"}
                ]
            },
            "risk_assessment": {
                "name": "Risk Assessment",
                "description": "Portfolio risk analysis and stress testing",
                "suggested_schedules": [
                    {"name": "Weekly on Friday", "cron": "0 16 * * FRI"},
                    {"name": "Monthly on 1st", "cron": "0 12 1 * *"},
                    {"name": "Quarterly", "cron": "0 14 1 */3 *"}
                ]
            },
            "market_monitoring": {
                "name": "Market Monitoring",
                "description": "Real-time market monitoring and alerts",
                "suggested_schedules": [
                    {"name": "Every 5 minutes", "cron": "*/5 * * * *"},
                    {"name": "Every 15 minutes", "cron": "*/15 * * * *"},
                    {"name": "Every hour", "cron": "0 * * * *"}
                ]
            }
        }
        
        return templates
    
    # === System Status ===
    
    async def get_scheduler_status(self) -> Dict[str, Any]:
        """Get comprehensive scheduler system status"""
        try:
            all_jobs = await self.list_all_jobs()
            
            if all_jobs.get("success"):
                jobs = all_jobs["jobs"]
                
                active_jobs = sum(1 for job in jobs if job.get("state") == "ENABLED")
                paused_jobs = sum(1 for job in jobs if job.get("state") == "PAUSED")
                
                status = {
                    "scheduler_available": True,
                    "total_jobs": len(jobs),
                    "active_jobs": active_jobs,
                    "paused_jobs": paused_jobs,
                    "project_id": self.project_id,
                    "location": self.location,
                    "timezone": self.timezone,
                    "financial_workflows_configured": len(self.financial_workflows),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                status = {
                    "scheduler_available": False,
                    "error": all_jobs.get("error"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting scheduler status: {e}")
            return {
                "scheduler_available": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Global instance
google_scheduler_manager = GoogleSchedulerManager() 