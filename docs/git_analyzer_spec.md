# Git Analyzer MCP Server Specification

## Overview

The Git Analyzer MCP Server is a specialized Model Context Protocol server that provides advanced Git repository analysis capabilities. It offers comprehensive code quality metrics, smell detection, contributor analysis, and hotspot identification for software development teams.

## Features

- **Multi-dimensional Analysis**: Examines code, history, contributions, and patterns simultaneously
- **Complex Algorithms**: Implements code smell detection, cyclomatic complexity calculation, and coupling analysis
- **Massive Data Processing**: Capable of analyzing repositories with thousands of commits and files
- **Contextual Intelligence**: Generates personalized recommendations based on project context
- **External Tool Integration**: Connects with static analysis tools and specialized linters

## Methods

### 1. `analyze_repository`

**Description**: Complete repository analysis

**Parameters**:
- `repo_path` (string): Path to the Git repository
- `branch` (string, optional): Branch to analyze (default: "main")
- `depth` (number, optional): Analysis depth in commits (default: 100)

**Returns**: Comprehensive analysis including repository info, code metrics, smells, contributors, and hotspots

**Example**:
```json
{
  "name": "analyze_repository",
  "arguments": {
    "repo_path": ".",
    "branch": "main",
    "depth": 100
  }
}
```

### 2. `get_code_metrics`

**Description**: Obtains code quality metrics for a specific file

**Parameters**:
- `file_path` (string): Path to the file to analyze
- `metric_types` (array, optional): Types of metrics to calculate
  - `lines_of_code`: Count of non-empty, non-comment lines
  - `cyclomatic_complexity`: Complexity measurement
  - `maintainability_index`: Maintainability score (0-100)
  - `technical_debt`: Estimated technical debt
  - `code_coverage`: Code coverage percentage

**Returns**: Dictionary of calculated metrics

**Example**:
```json
{
  "name": "get_code_metrics",
  "arguments": {
    "file_path": "src/main.py",
    "metric_types": ["lines_of_code", "cyclomatic_complexity", "maintainability_index"]
  }
}
```

### 3. `detect_smells`

**Description**: Detects code smells and antipatterns

**Parameters**:
- `repo_path` (string): Path to the Git repository
- `sensitivity_level` (string, optional): Detection sensitivity
  - `low`: Basic smell detection
  - `medium`: Standard detection (default)
  - `high`: Comprehensive detection

**Returns**: Categorized list of code smells with severity and suggestions

**Example**:
```json
{
  "name": "detect_smells",
  "arguments": {
    "repo_path": ".",
    "sensitivity_level": "medium"
  }
}
```

### 4. `analyze_contributors`

**Description**: Analysis of contributions and ownership

**Parameters**:
- `repo_path` (string): Path to the Git repository
- `time_range` (string, optional): Time range for analysis
  - `1 month`: Last month
  - `6 months`: Last 6 months (default)
  - `1 year`: Last year

**Returns**: Contributor statistics including commits, lines changed, and ownership percentages

**Example**:
```json
{
  "name": "analyze_contributors",
  "arguments": {
    "repo_path": ".",
    "time_range": "1 year"
  }
}
```

### 5. `get_hotspots`

**Description**: Identifies problematic files

**Parameters**:
- `repo_path` (string): Path to the Git repository
- `threshold` (number, optional): Change frequency threshold (default: 0.8)

**Returns**: List of files with high change frequency and associated metrics

**Example**:
```json
{
  "name": "get_hotspots",
  "arguments": {
    "repo_path": ".",
    "threshold": 0.8
  }
}
```

### 6. `generate_report`

**Description**: Generates comprehensive analysis report

**Parameters**:
- `analysis_id` (string): ID of the analysis to report on
- `format` (string, optional): Report format (default: "json")
- `sections` (array, optional): Sections to include in the report
  - `repository_info`: Basic repository information
  - `code_metrics`: Code quality metrics
  - `code_smells`: Detected code smells
  - `contributors`: Contributor analysis
  - `hotspots`: Problematic files

**Returns**: Comprehensive report with summary and recommendations

**Example**:
```json
{
  "name": "generate_report",
  "arguments": {
    "analysis_id": "analysis_20241220_143022",
    "format": "json",
    "sections": ["repository_info", "code_metrics", "code_smells"]
  }
}
```

## Installation

### Prerequisites

- Python 3.8+
- Git repository access
- Required Python packages (see requirements.txt)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd git-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the server executable:
```bash
chmod +x src/mcp_servers/git_analyzer_server.py
```

## Usage

### Direct Execution

Run the server directly:
```bash
python3 src/mcp_servers/git_analyzer_server.py
```

### MCP Client Integration

The server can be integrated with MCP clients:

```python
from src.mcp_servers.git_analyzer_client import GitAnalyzerClient

# Initialize client
client = GitAnalyzerClient()
await client.start_analyzer_server()

# Analyze repository
result = await client.analyze_repository(".")
print(result)
```

### Chatbot Integration

The server is integrated with the MCP Chatbot for natural language interaction:

```
User: analyze repository
Bot: 🔍 Repository Analysis Complete
     📊 Analysis ID: analysis_20241220_143022
     🌿 Branch: main
     ...

User: detect smells
Bot: 🚨 Code Smells Detection
     📊 Summary:
     • Total Smells: 5
     • Files Analyzed: 12
     ...
```

## Response Format

All methods return responses in the following format:

```json
{
  "success": true,
  "data": {
    // Method-specific data
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Examples

### Complete Repository Analysis

```bash
# Analyze current repository
analyze repository

# Analyze specific repository
analyze repository /path/to/repo

# Analyze with specific branch and depth
analyze repository /path/to/repo main 50
```

### Code Metrics Analysis

```bash
# Get metrics for a specific file
get code metrics src/main.py

# Get specific metrics
get code metrics src/utils.py lines_of_code cyclomatic_complexity
```

### Code Smell Detection

```bash
# Detect smells in current repository
detect smells

# Detect smells with high sensitivity
detect smells . high
```

### Contributor Analysis

```bash
# Analyze contributors for the last year
analyze contributors

# Analyze contributors for specific time range
analyze contributors . 6 months
```

### Hotspot Identification

```bash
# Get hotspots with default threshold
get hotspots

# Get hotspots with custom threshold
get hotspots . 0.9
```

### Report Generation

```bash
# Generate report for specific analysis
generate report analysis_20241220_143022

# Generate report with specific sections
generate report analysis_20241220_143022 json repository_info code_metrics
```

## Technical Details

### Code Metrics Calculation

- **Lines of Code**: Counts non-empty, non-comment lines
- **Cyclomatic Complexity**: Measures code complexity based on control flow
- **Maintainability Index**: Calculated based on file size and complexity
- **Technical Debt**: Estimated based on complexity and file size
- **Code Coverage**: Placeholder for integration with coverage tools

### Code Smell Detection

- **Long Method**: Methods exceeding 50 lines
- **Long Parameter List**: Functions with more than 5 parameters
- **Duplicate Code**: Repeated code blocks (high sensitivity only)

### Contributor Analysis

- **Ownership Calculation**: Based on commit frequency
- **Lines Changed**: Tracks additions and deletions per contributor
- **Time Range Filtering**: Supports various time ranges

### Hotspot Identification

- **Change Frequency**: Based on commit history
- **Threshold-based**: Configurable sensitivity
- **Metrics Integration**: Combines change frequency with code metrics

## Error Handling

The server includes comprehensive error handling:

- **File Access Errors**: Graceful handling of missing files
- **Git Command Errors**: Proper error reporting for Git operations
- **Analysis Errors**: Detailed error messages for analysis failures
- **Parameter Validation**: Input validation and sanitization

## Performance Considerations

- **Caching**: Analysis results are cached for performance
- **Incremental Analysis**: Supports depth-based analysis
- **Memory Management**: Efficient handling of large repositories
- **Timeout Handling**: Prevents hanging on large operations

## Security

- **Path Validation**: Prevents directory traversal attacks
- **Input Sanitization**: Validates all input parameters
- **Process Isolation**: Runs in isolated subprocess environment

## License

This MCP server is licensed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please open an issue on the GitHub repository.
