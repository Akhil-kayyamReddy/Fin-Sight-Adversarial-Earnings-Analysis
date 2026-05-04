"""
Logging Configuration
Provides structured logging for all modules
"""

import logging
import sys
import json
from datetime import datetime
from typing import Optional
from pythonjsonlogger import jsonlogger
from backend.utils.config import get_settings


class StructuredFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record"""
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp
        log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Add log level
        log_record['level'] = record.levelname
        
        # Add module name
        log_record['module'] = record.name
        
        # Add function name and line number
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (typically __name__ from calling module)
    
    Returns:
        Configured logger instance
    """
    settings = get_settings()
    
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Remove existing handlers to prevent duplicates
    logger.handlers.clear()
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    formatter = StructuredFormatter(
        '%(timestamp)s %(level)s %(module)s %(function)s %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Set propagate to False to avoid duplicate logs
    logger.propagate = False
    
    return logger


class LogContext:
    """Context manager for adding contextual information to logs"""
    
    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
    
    def __enter__(self):
        """Enter context"""
        for key, value in self.context.items():
            self.logger = logging.LoggerAdapter(self.logger, {key: value})
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        if exc_type:
            self.logger.error(
                f"Error in context: {exc_type.__name__}",
                exc_info=True
            )
        return False


def log_operation(operation_name: str, logger: logging.Logger):
    """Decorator for logging function operations"""
    
    Args:
        operation_name: Name of the operation
        logger: Logger instance
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Starting operation: {operation_name}")
                result = func(*args, **kwargs)
                logger.info(f"Completed operation: {operation_name}")
                return result
            except Exception as e:
                logger.error(f"Error in {operation_name}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator
