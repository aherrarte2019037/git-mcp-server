"""
Utility functions for the Git MCP Server project
"""
import logging
import json
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('mcp_interactions.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

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
