"""
Centralized logging configuration for Financial Multi-Agent System
Provides file and console logging with rotation and proper formatting
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

class FinancialSystemLogger:
    """Centralized logger for the Financial Multi-Agent System"""
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_level = getattr(logging, log_level.upper())
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Create main log file path
        log_file = self.log_dir / "financial_system.log"
        
        # Create custom formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # File handler with rotation (10MB max, keep 5 files)
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        
        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to root logger
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Setup specific loggers for different components
        self._setup_component_loggers()
        
        # Log startup message
        startup_logger = logging.getLogger('system.startup')
        startup_logger.info("="*80)
        startup_logger.info("Financial Multi-Agent System - Logging Initialized")
        startup_logger.info(f"Log file: {log_file}")
        startup_logger.info(f"Log level: {logging.getLevelName(self.log_level)}")
        startup_logger.info("="*80)
    
    def _setup_component_loggers(self):
        """Setup loggers for specific components"""
        # System components
        loggers = [
            'system.startup',
            'system.shutdown', 
            'mcp.server',
            'mcp.client',
            'dashboard.app',
            'dashboard.enhanced',
            'adk.orchestrator',
            'adk.agents',
            'data.collector',
            'ai.analysis',
            'database.operations',
            'api.requests'
        ]
        
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(self.log_level)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger for a specific component"""
        return logging.getLogger(name)
    
    def log_system_info(self):
        """Log system information"""
        info_logger = logging.getLogger('system.info')
        info_logger.info(f"Python version: {os.sys.version}")
        info_logger.info(f"Working directory: {os.getcwd()}")
        info_logger.info(f"Log directory: {self.log_dir.absolute()}")
    
    def log_error_with_context(self, logger_name: str, error: Exception, context: str = ""):
        """Log error with full context"""
        error_logger = logging.getLogger(logger_name)
        error_logger.error(f"ERROR in {context}: {type(error).__name__}: {error}")
        error_logger.debug(f"Full traceback:", exc_info=True)

# Global logger instance
_logger_instance = None

def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> FinancialSystemLogger:
    """Setup global logging configuration"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = FinancialSystemLogger(log_dir, log_level)
        _logger_instance.log_system_info()
    return _logger_instance

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a component (auto-setup if needed)"""
    global _logger_instance
    if _logger_instance is None:
        setup_logging()
    return _logger_instance.get_logger(name)

def log_startup(component: str, message: str):
    """Log startup message"""
    logger = get_logger('system.startup')
    logger.info(f"[{component}] {message}")

def log_shutdown(component: str, message: str):
    """Log shutdown message"""
    logger = get_logger('system.shutdown')
    logger.info(f"[{component}] {message}")

def log_error(component: str, error: Exception, context: str = ""):
    """Log error with context"""
    global _logger_instance
    if _logger_instance is None:
        setup_logging()
    _logger_instance.log_error_with_context(f'{component}.error', error, context)

# Component-specific logger getters
def get_mcp_logger() -> logging.Logger:
    return get_logger('mcp.client')

def get_dashboard_logger() -> logging.Logger:
    return get_logger('dashboard.app')

def get_adk_logger() -> logging.Logger:
    return get_logger('adk.orchestrator')

def get_data_logger() -> logging.Logger:
    
    return get_logger('data.collector')

def get_ai_logger() -> logging.Logger:
    return get_logger('ai.analysis')

def get_db_logger() -> logging.Logger:
    return get_logger('database.operations') 