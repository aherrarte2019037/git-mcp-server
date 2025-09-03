"""
Configuration settings for the Git MCP Server project
"""
import os

# Anthropic API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# MCP Server Configuration
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8000

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
