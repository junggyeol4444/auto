"""Logger utility for Voice Service Integrated Suite."""
import os
import sys
from loguru import logger
from datetime import datetime


def setup_logger(log_dir="logs", log_level="INFO"):
    """
    Setup application logger.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # Add file handler
    log_file = os.path.join(log_dir, f"voice_service_{datetime.now().strftime('%Y%m%d')}.log")
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    return logger


def get_logger():
    """Get the configured logger instance."""
    return logger
