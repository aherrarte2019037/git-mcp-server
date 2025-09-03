# Setup Instructions for Git MCP Server

## Quick Setup Guide

### 1. Prerequisites
- Python 3.9 or higher
- Git installed on your system
- Anthropic API key

### 2. Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd git-mcp-server
   ```

2. **Create and activate virtual environment**:
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

### 3. Running the Project

**Run the chatbot**:
```bash
python main.py
```

### 4. Testing the Installation

The chatbot will:
- Initialize all MCP servers
- Provide interactive interface
- Test all MCP server functionality
- Display results

If the chatbot starts successfully, your installation is complete!

### 5. Troubleshooting

**Common Issues**:

1. **"ANTHROPIC_API_KEY not found"**:
   - Make sure you've set the environment variable
   - Get your API key from https://console.anthropic.com/

2. **"Git command not found"**:
   - Install Git on your system
   - Make sure Git is in your PATH

3. **Import errors**:
   - Make sure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

4. **Permission errors**:
   - Make sure you have write permissions in the project directory
   - Check file permissions for the demo directory

### 6. Project Structure

```
git-mcp-server/
├── main.py                    # Main entry point
├── demo.py                    # Demo script
├── requirements.txt           # Dependencies
├── README.md                  # Main documentation
├── SETUP_INSTRUCTIONS.md     # This file
└── src/
    ├── chatbot/              # Chatbot implementation
    ├── mcp_servers/          # MCP server implementations
    └── docs/                 # Additional documentation
```

### 7. Available Commands

Once running, you can use these commands:

**Filesystem Operations**:
- `read file <filename>`
- `list files`
- `create file <filename> <content>`

**Git Operations**:
- `init repository`
- `add file <filename>`
- `commit "message"`
- `git status`

**Git Analyzer Operations**:
- `analyze repository`
- `commit stats`
- `file stats`
- `generate report`

### 8. Getting Help

- Check the main README.md for detailed documentation
- Run the chatbot to see all functionality
- Check the logs in `mcp_interactions.log` for debugging

### 9. Next Steps

After successful setup:
1. Try the interactive chatbot
2. Test with your own repositories
3. Explore the code to understand the implementation
4. Check the MCP server specifications in `docs/`

---

**Note**: This project represents the partial delivery (45% of total grade) covering steps 1-5 of the project requirements.
