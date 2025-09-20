#!/usr/bin/env python3
"""
Main entry point for the Git MCP Server project
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import setup_logging
from chatbot.main import main

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    main()