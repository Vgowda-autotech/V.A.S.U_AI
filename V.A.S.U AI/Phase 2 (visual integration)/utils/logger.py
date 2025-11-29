import logging
import sys
import os
from pathlib import Path

def setup_logger(name="VASU", log_file="vasu.log", level=logging.INFO):
    """Configures and returns a logger instance."""
    
    # Ensure logs directory exists
    # We use absolute path relative to this file to be safe
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers if logger is already setup
    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File Handler
        file_handler = logging.FileHandler(log_dir / log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

def get_logger(name):
    """Returns a logger with the specified name."""
    # Ensure the main logger is set up at least once
    if not logging.getLogger("VASU").handlers:
        setup_logger()
        
    return logging.getLogger(f"VASU.{name}")