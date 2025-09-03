# Git Analyzer MCP Server Specification

## Overview

The Git Analyzer MCP Server is a custom Model Context Protocol server that provides comprehensive analysis of Git repositories. It offers statistical analysis, metrics calculation, and report generation capabilities for Git repositories.

## Server Information

- **Name**: Git Analyzer MCP Server
- **Version**: 1.0.0
- **Protocol**: MCP (Model Context Protocol)
- **Language**: Python 3.9+
- **Dependencies**: GitPython, subprocess, os, datetime

## Available Methods

### 1. get_repo_info

**Description**: Retrieves basic information and statistics about a Git repository.

**Parameters**:
- `repo_path` (string, optional): Path to the repository. Defaults to current directory.

**Returns**:
```json
{
  "success": true,
  "data": {
    "repository_path": ".",
    "analysis_timestamp": "2024-01-15T10:30:00",
    "statistics": {
      "total_commits": 42,
      "total_files": 15,
      "lines_of_code": 1250,
      "repository_size": "2.5M",
      "current_branch": "main",
      "last_commit": {
        "hash": "a1b2c3d4",
        "author": "John Doe",
        "email": "john@example.com",
        "date": "2024-01-15",
        "message": "Add new feature"
      }
    }
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Not a git repository",
  "data": null
}
```

### 2. get_commit_stats

**Description**: Analyzes commit statistics for a specified time period.

**Parameters**:
- `repo_path` (string, optional): Path to the repository. Defaults to current directory.
- `days` (integer, optional): Number of days to analyze. Defaults to 30.

**Returns**:
```json
{
  "success": true,
  "data": {
    "repository_path": ".",
    "analysis_timestamp": "2024-01-15T10:30:00",
    "statistics": {
      "total_commits": 12,
      "period_days": 30,
      "commits_per_day": 0.4,
      "top_contributors": [
        ["John Doe", 8],
        ["Jane Smith", 4]
      ],
      "recent_commits": [
        {
          "hash": "a1b2c3d4",
          "author": "John Doe",
          "date": "2024-01-15"
        }
      ]
    }
  }
}
```

### 3. get_file_stats

**Description**: Provides detailed file statistics and analysis.

**Parameters**:
- `repo_path` (string, optional): Path to the repository. Defaults to current directory.

**Returns**:
```json
{
  "success": true,
  "data": {
    "repository_path": ".",
    "analysis_timestamp": "2024-01-15T10:30:00",
    "statistics": {
      "total_files": 15,
      "total_size_bytes": 2621440,
      "total_size_mb": 2.5,
      "file_extensions": {
        ".py": 8,
        ".md": 3,
        ".txt": 2,
        ".json": 2
      },
      "largest_files": [
        {
          "file": "src/main.py",
          "size": 1024000,
          "size_mb": 1.0
        }
      ]
    }
  }
}
```

### 4. generate_report

**Description**: Generates a comprehensive repository analysis report.

**Parameters**:
- `repo_path` (string, optional): Path to the repository. Defaults to current directory.
- `format` (string, optional): Report format. Options: "json", "text". Defaults to "json".

**Returns** (JSON format):
```json
{
  "success": true,
  "format": "json",
  "data": {
    "repository_analysis": {
      "repository_path": ".",
      "generated_at": "2024-01-15T10:30:00",
      "repository_info": { /* get_repo_info data */ },
      "commit_statistics": { /* get_commit_stats data */ },
      "file_statistics": { /* get_file_stats data */ }
    }
  }
}
```

**Returns** (Text format):
```text
# Git Repository Analysis Report

**Repository:** .
**Generated:** 2024-01-15T10:30:00

## Repository Overview
- **Total Commits:** 42
- **Total Files:** 15
- **Lines of Code:** 1250
- **Repository Size:** 2.5M
- **Current Branch:** main

## Recent Activity (Last 30 Days)
- **Commits:** 12
- **Commits per Day:** 0.4
- **Top Contributors:**
  - John Doe: 8 commits
  - Jane Smith: 4 commits

## File Statistics
- **Total Files:** 15
- **Total Size:** 2.5 MB
- **File Extensions:**
  - .py: 8 files
  - .md: 3 files
  - .txt: 2 files

## Largest Files
  - src/main.py: 1.0 MB
  - docs/README.md: 0.5 MB
```

## Error Handling

All methods return a consistent error format:

```json
{
  "success": false,
  "error": "Error description",
  "data": null
}
```

Common error scenarios:
- Repository not found
- Not a Git repository
- Permission denied
- Command timeout
- Invalid parameters

## Usage Examples

### Python Integration

```python
from git_analyzer_server import GitAnalyzerMCPServer

# Initialize server
analyzer = GitAnalyzerMCPServer("/path/to/repo")

# Get repository information
info = analyzer.get_repo_info()
if info["success"]:
    print(f"Total commits: {info['data']['statistics']['total_commits']}")

# Get commit statistics
stats = analyzer.get_commit_stats(days=7)
if stats["success"]:
    print(f"Commits this week: {stats['data']['statistics']['total_commits']}")

# Generate text report
report = analyzer.generate_report(format="text")
if report["success"]:
    print(report["data"])
```

### Chatbot Integration

```python
# Through the chatbot interface
response = chatbot.process_message("analyze repository")
response = chatbot.process_message("commit stats")
response = chatbot.process_message("file stats")
response = chatbot.process_message("generate report")
```

## Performance Considerations

- **Timeout**: All Git commands have a 30-second timeout
- **Memory**: Large repositories may require significant memory for analysis
- **Disk I/O**: File operations are optimized for minimal disk access
- **Caching**: Results are not cached; each call performs fresh analysis

## Security

- **Path Validation**: All file paths are validated to prevent directory traversal
- **Command Injection**: Git commands are executed through subprocess with proper escaping
- **Permission Checks**: Repository access is validated before operations

## Dependencies

- **Git**: Must be installed and accessible in PATH
- **Python 3.9+**: Required for subprocess and pathlib features
- **Standard Library**: os, subprocess, datetime, json

## Installation

1. Ensure Git is installed on the system
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Import and initialize the server:
   ```python
   from git_analyzer_server import GitAnalyzerMCPServer
   analyzer = GitAnalyzerMCPServer()
   ```

## Testing

The server can be tested using the demo script:

```bash
python demo.py
```

This will create a temporary repository and test all available methods.

## Logging

All operations are logged with the following information:
- Method called
- Parameters provided
- Success/failure status
- Execution time
- Error details (if applicable)

Logs are written to the standard MCP interaction log file.
