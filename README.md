# Git MCP Server Project

A comprehensive Model Context Protocol (MCP) server implementation for Git repository analysis, integrated with a chatbot that uses Anthropic's Claude API.

## 🎯 Project Overview

This project implements a chatbot that integrates multiple MCP servers to provide:
- **Filesystem operations** (read, write, list, delete files)
- **Git repository management** (init, add, commit, status)
- **Advanced Git repository analysis** (statistics, metrics, reports)

## 🚀 Features

### Chatbot Core (15% of project grade)
- ✅ **LLM API Integration**: Connects to Anthropic's Claude API
- ✅ **Context Management**: Maintains conversation context across interactions
- ✅ **MCP Interaction Logging**: Logs all MCP server interactions

### MCP Servers Integration (30% of project grade)
- ✅ **Filesystem MCP Server**: File operations (read, write, list, delete)
- ✅ **Git MCP Server**: Git operations (init, add, commit, status, log)
- ✅ **Custom Git Analyzer MCP Server**: Repository analysis and statistics

### Custom MCP Server (15% of project grade)
- ✅ **Repository Analysis**: Basic repository information and statistics
- ✅ **Commit Statistics**: Analysis of commit history and contributors
- ✅ **File Statistics**: File count, size, and extension analysis
- ✅ **Report Generation**: Comprehensive reports in JSON and text formats

## 📋 Requirements

- Python 3.9+
- Anthropic API key
- Git installed on system

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd git-mcp-server
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## 🎮 Usage

### Quick Start

**Run the chatbot**:
```bash
python main.py
```

### Available Commands

#### Filesystem Operations
- `read file <filename>` - Read a file
- `list files` - List directory contents
- `create file <filename> <content>` - Create a new file

#### Git Operations
- `init repository` - Initialize a new Git repository
- `add file <filename>` - Add file to Git staging area
- `commit "message"` - Create a commit with message
- `git status` - Check repository status

#### Git Analyzer Operations
- `analyze repository` - Get basic repository information
- `commit stats` - Get commit statistics (last 30 days)
- `file stats` - Get file statistics
- `generate report` - Generate comprehensive repository report

### Example Session

```
🤖 Git MCP Chatbot - Type 'quit' to exit, 'clear' to clear context
============================================================

👤 You: init repository
🤖 Bot: Git repository initialized successfully.

👤 You: create file README.md "# My Project\nThis is a demo project."
🤖 Bot: File 'README.md' created successfully with 2 lines.

👤 You: add file README.md
🤖 Bot: File 'README.md' added to staging area.

👤 You: commit "Initial commit"
🤖 Bot: Commit created successfully: Initial commit

👤 You: analyze repository
🤖 Bot: Repository Analysis:
- Total Commits: 1
- Total Files: 1
- Lines of Code: 2
- Repository Size: 1.0K
- Current Branch: main
- Last Commit: Initial commit
```

## 🏗️ Project Structure

```
git-mcp-server/
├── main.py                          # Main entry point
├── demo.py                          # Demo script
├── requirements.txt                 # Dependencies
├── README.md                       # This file
└── src/
    ├── config.py                   # Configuration settings
    ├── utils.py                    # Utility functions
    ├── chatbot/
    │   ├── main.py                 # Main chatbot class
    │   ├── anthropic_client.py     # Anthropic API client
    │   ├── context_manager.py      # Context management
    │   └── init_mcp_servers.py     # MCP server initialization
    └── mcp_servers/
        ├── filesystem_client.py    # Filesystem MCP client
        ├── git_client.py          # Git MCP client
        └── git_analyzer_server.py # Custom Git analyzer MCP server
```

## 🔧 MCP Server Specifications

### Git Analyzer MCP Server

**Purpose**: Provides comprehensive analysis of Git repositories including statistics, metrics, and reports.

**Available Methods**:

1. **`get_repo_info(repo_path=".")`**
   - Returns basic repository information
   - Parameters: `repo_path` (string) - Path to repository
   - Returns: Repository statistics, commit count, file count, size, current branch

2. **`get_commit_stats(repo_path=".", days=30)`**
   - Returns commit statistics for specified period
   - Parameters: `repo_path` (string), `days` (int) - Analysis period
   - Returns: Commit count, contributors, activity patterns

3. **`get_file_stats(repo_path=".")`**
   - Returns file statistics and analysis
   - Parameters: `repo_path` (string) - Path to repository
   - Returns: File count, size, extensions, largest files

4. **`generate_report(repo_path=".", format="json")`**
   - Generates comprehensive repository report
   - Parameters: `repo_path` (string), `format` (string) - "json" or "text"
   - Returns: Complete analysis report

**Example Usage**:
```python
# Initialize the server
analyzer = GitAnalyzerMCPServer()

# Get repository information
info = analyzer.get_repo_info()
print(f"Total commits: {info['data']['statistics']['total_commits']}")

# Generate text report
report = analyzer.generate_report(format="text")
print(report['data'])
```

## 📊 Usage Scenarios

### Complete Repository Workflow
The chatbot can demonstrate:
1. Initialize Git repository
2. Create files
3. Add files to Git
4. Create commits
5. Analyze repository with Git Analyzer
6. Generate comprehensive reports

## 🔍 Logging

All MCP interactions are logged to `mcp_interactions.log` with detailed information about:
- Request/response data
- Timestamps
- Error handling
- Performance metrics

## 🧪 Testing

Run the chatbot to verify all functionality:
```bash
python main.py
```

The chatbot will:
- Initialize all MCP servers
- Provide interactive interface
- Execute all MCP operations
- Display results

## 📝 API Integration

### Anthropic Claude API
- Uses Claude-3-Haiku model for cost efficiency
- Maintains conversation context
- Handles API errors gracefully
- Logs all interactions

### MCP Protocol
- Implements standard MCP communication
- JSON-RPC based messaging
- Error handling and validation
- Comprehensive logging

## 🚀 Future Enhancements

Potential improvements for the full project:
- Remote MCP server deployment
- Advanced code analysis (complexity, smells)
- Integration with external tools (linters, analyzers)
- Web interface
- Real-time collaboration features

## 📄 License

This project is developed for educational purposes as part of a university course.

## 👥 Author

Developed as part of the "Uso de un protocolo existente" course project.

---

**Note**: This project represents the partial delivery (45% of total grade) covering steps 1-5 of the project requirements, including the custom MCP server development, testing, and GitHub availability.