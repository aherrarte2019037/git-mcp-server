#!/usr/bin/env python3
"""
Demo script for the Git MCP Server project
This script demonstrates all the functionality required for the project
"""
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.main import Chatbot
from chatbot.init_mcp_servers import initialize_mcp_servers

def run_demo():
    """Run the complete demo scenario"""
    print("🚀 Git MCP Server Project Demo")
    print("=" * 50)
    
    # Create a temporary directory for the demo
    demo_dir = tempfile.mkdtemp(prefix="git_mcp_demo_")
    print(f"📁 Demo directory: {demo_dir}")
    
    try:
        # Initialize chatbot
        print("\n🤖 Initializing Chatbot...")
        chatbot = Chatbot()
        initialize_mcp_servers(chatbot)
        
        # Change to demo directory
        original_cwd = os.getcwd()
        os.chdir(demo_dir)
        
        print("\n📋 Demo Scenario: Complete Git Repository Workflow")
        print("-" * 50)
        
        # Step 1: Initialize Git Repository
        print("\n1️⃣ Initializing Git Repository...")
        response = chatbot.process_message("init repository")
        print(f"Response: {response}")
        
        # Step 2: Create README file
        print("\n2️⃣ Creating README file...")
        readme_content = """# Git MCP Demo Project

This is a demonstration project for the Git MCP Server.

## Features
- Git repository management
- File operations
- Repository analysis

## Usage
This project demonstrates the integration of MCP servers with a chatbot.
"""
        response = chatbot.process_message(f'create file README.md "{readme_content}"')
        print(f"Response: {response}")
        
        # Step 3: Create a Python file
        print("\n3️⃣ Creating Python file...")
        python_content = """#!/usr/bin/env python3
\"\"\"
Demo Python file for Git MCP Server
\"\"\"

def hello_world():
    \"\"\"Print hello world message\"\"\"
    print("Hello, Git MCP Server!")

def calculate_sum(a, b):
    \"\"\"Calculate sum of two numbers\"\"\"
    return a + b

if __name__ == "__main__":
    hello_world()
    result = calculate_sum(5, 3)
    print(f"5 + 3 = {result}")
"""
        response = chatbot.process_message(f'create file demo.py "{python_content}"')
        print(f"Response: {response}")
        
        # Step 4: List files
        print("\n4️⃣ Listing files...")
        response = chatbot.process_message("list files")
        print(f"Response: {response}")
        
        # Step 5: Add files to Git
        print("\n5️⃣ Adding files to Git...")
        response = chatbot.process_message("add file README.md")
        print(f"Response: {response}")
        
        response = chatbot.process_message("add file demo.py")
        print(f"Response: {response}")
        
        # Step 6: Check Git status
        print("\n6️⃣ Checking Git status...")
        response = chatbot.process_message("git status")
        print(f"Response: {response}")
        
        # Step 7: Create initial commit
        print("\n7️⃣ Creating initial commit...")
        response = chatbot.process_message('commit "Initial commit: Add README and demo Python file"')
        print(f"Response: {response}")
        
        # Step 8: Analyze repository with Git Analyzer
        print("\n8️⃣ Analyzing repository with Git Analyzer...")
        response = chatbot.process_message("analyze repository")
        print(f"Response: {response}")
        
        # Step 9: Get commit statistics
        print("\n9️⃣ Getting commit statistics...")
        response = chatbot.process_message("commit stats")
        print(f"Response: {response}")
        
        # Step 10: Get file statistics
        print("\n🔟 Getting file statistics...")
        response = chatbot.process_message("file stats")
        print(f"Response: {response}")
        
        # Step 11: Generate comprehensive report
        print("\n1️⃣1️⃣ Generating comprehensive report...")
        response = chatbot.process_message("generate report")
        print(f"Response: {response}")
        
        # Step 12: Read a file
        print("\n1️⃣2️⃣ Reading README file...")
        response = chatbot.process_message("read file README.md")
        print(f"Response: {response}")
        
        print("\n✅ Demo completed successfully!")
        print(f"📁 Demo files created in: {demo_dir}")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Return to original directory
        os.chdir(original_cwd)
        
        # Clean up demo directory (optional)
        try:
            shutil.rmtree(demo_dir)
            print(f"🧹 Cleaned up demo directory: {demo_dir}")
        except:
            print(f"⚠️ Could not clean up demo directory: {demo_dir}")

def run_interactive_demo():
    """Run interactive demo where user can test commands"""
    print("\n🎮 Interactive Demo Mode")
    print("=" * 30)
    print("You can now test the chatbot interactively!")
    print("Try commands like:")
    print("- 'init repository'")
    print("- 'create file test.txt Hello World'")
    print("- 'list files'")
    print("- 'analyze repository'")
    print("- 'quit' to exit")
    print("-" * 30)
    
    # Initialize chatbot
    chatbot = Chatbot()
    initialize_mcp_servers(chatbot)
    
    # Run interactive mode
    chatbot.run_interactive()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_demo()
    else:
        run_demo()
        
        # Ask if user wants to run interactive demo
        print("\n" + "=" * 50)
        response = input("Would you like to run the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            run_interactive_demo()
