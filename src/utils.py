"""
Utility functions for the Git MCP Server project
"""
import logging
import json
from datetime import datetime
import config

def setup_logging():
    """Setup logging configuration - only writes to file, no console output"""
    # Clear any existing log file and setup new logging
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(config.LOG_FILE, mode='w'),  # 'w' mode overwrites existing file
            # Removed StreamHandler() to disable console output
        ],
        force=True  # Force reconfiguration of logging
    )
    
    logger = logging.getLogger(__name__)
    return logger

def log_mcp_interaction(action, request, response=None):
    """Log MCP interactions"""
    logger = logging.getLogger('mcp_interactions')
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'request': request,
        'response': response
    }
    logger.info(json.dumps(log_entry, indent=2))
