# MCP Git Server Project

This is a comprehensive project implementing MCP (Model Context Protocol) servers for filesystem, Git operations, and advanced Git repository analysis.

## Features

### Core MCP Servers
- **Filesystem MCP Server** - File operations (read, write, list)
- **Git MCP Server** - Git operations (status, add, commit, log, branch)
- **Git Analyzer MCP Server** - Advanced repository analysis

### AI-Powered Chatbot
- Natural language command detection
- Context-aware conversations
- Multi-server integration
- Real-time analysis and reporting

## Git Analyzer MCP Server

The project includes a sophisticated **Git Analyzer MCP Server** that provides:

- **Repository Analysis**: Complete codebase analysis with metrics
- **Code Quality Metrics**: Lines of code, cyclomatic complexity, maintainability
- **Code Smell Detection**: Long methods, parameter lists, duplicate code
- **Contributor Analysis**: Commit statistics, ownership percentages
- **Hotspot Identification**: Files with high change frequency
- **Report Generation**: Comprehensive analysis reports

### Quick Start with Git Analyzer

```bash
# Navigate to Git Analyzer directory
cd git_analyzer_mcp_server/

# Run automatic installation
python3 setup.py

# Start interactive demo
python3 start.py interactive
```

### Available Commands
- `analizar repositorio` - Complete repository analysis
- `obtener metricas <archivo>` - File-specific metrics
- `detectar smells` - Code smell detection
- `analizar contribuidores` - Contributor analysis
- `obtener hotspots` - Problematic file identification
- `generar reporte <analysis_id>` - Generate detailed reports

## Project Structure

```
├── src/                          # Main chatbot implementation
│   ├── mcp_servers/             # MCP server clients
│   └── chatbot/                 # Chatbot components
├── git_analyzer_mcp_server/     # Standalone Git Analyzer MCP Server
│   ├── server/                  # MCP server implementation
│   ├── client/                  # MCP client
│   ├── executor/                # Command executor
│   ├── docs/                    # Documentation
│   ├── examples/                # Usage examples
│   └── start.py                 # Quick start script
└── main.py                      # Main entry point
```

## Installation

### Main Project
```bash
pip install -r requirements.txt
python3 main.py
```

### Git Analyzer MCP Server (Standalone)
```bash
cd git_analyzer_mcp_server/
python3 setup.py
python3 start.py
```

## Documentation

- **Main Project**: See `src/` directory for implementation details
- **Git Analyzer**: Complete documentation in `git_analyzer_mcp_server/docs/`
- **Installation Guide**: `git_analyzer_mcp_server/INSTALACION.md`
- **Integration Guide**: `git_analyzer_mcp_server/docs/guia_implementacion.md`

## Created by
MCP Chatbot with Anthropic Claude
