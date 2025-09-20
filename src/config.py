"""
Configuration settings for the Git MCP Server project
"""
import os

# Anthropic API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# MCP Server Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT")

# Logging Configuration
LOG_LEVEL = os.getenv("MCP_LOG_LEVEL")
LOG_FORMAT = os.getenv("MCP_LOG_FORMAT")
LOG_FILE = os.getenv("MCP_LOG_FILE")