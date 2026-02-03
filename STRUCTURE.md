# 📁 Project Structure

## Directory Organization

```
AgenticAI@UIUC/
│
├── 📁 agents/                    → AI agents and sending tools
│   ├── ai_email_agent_react_openai.py  ⭐ ReAct with OpenAI (RECOMMENDED)
│   ├── ai_email_agent_react.py         Alternative: ReAct with Claude
│   ├── ai_email_agent_openai.py        Traditional OpenAI agent
│   ├── ai_email_agent.py               Traditional Claude agent
│   ├── send_email_cli.py               Command line interface
│   └── bulk_send.py                    Bulk email sender
│
├── 📁 core/                      → Core email implementation
│   ├── email_agent.py                  SMTP email logic (Gmail)
│   └── email_agent_sendgrid.py         SendGrid alternative
│
├── 📁 docs/                      → Documentation
│   ├── GETTING_STARTED.md              ⭐ Start here!
│   ├── README_REACT.md                 ReAct pattern explained
│   ├── AGENT_COMPARISON.md             Compare all 4 agent types
│   ├── QUICKSTART.md                   Quick reference guide
│   ├── README_AI_AGENT.md              Traditional AI agent docs
│   └── README.md                       Overview
│
├── 📁 demos/                     → Demo scripts
│   ├── demo_react.py                   Compare Traditional vs ReAct
│   └── demo.py                         Email preview (no sending)
│
├── 📁 tests/                     → Test scripts
│   ├── test_react.py                   Test ReAct agent
│   ├── test_ai_agent.py                Test AI setup
│   └── troubleshoot_email.py           Email debugging tool
│
├── 📁 examples/                  → Example data files
│   ├── recipients_example.json         JSON format example
│   ├── recipients_example.csv          CSV format example
│   └── lecture01_recipients.json       Lecture 1 template
│
├── 📁 utils/                     → Utility scripts
│   └── setup.sh                        Automated setup script
│
├── 📄 .env                       → Your credentials (configured!)
├── 📄 .env.example               → Template for credentials
├── 📄 .gitignore                 → Git ignore rules
├── 📄 requirements.txt           → Python dependencies
├── 📄 README.md                  → Main readme
├── 📄 STRUCTURE.md               → This file
└── 🚀 run_agent.sh               → Quick launcher script

```

## Quick Access

### 🚀 Run Things

```bash
# Quick launcher (interactive menu)
./run_agent.sh

# Or run directly:
python agents/ai_email_agent_react_openai.py  # ReAct agent
python demos/demo_react.py                     # Demo
python agents/send_email_cli.py                # CLI
python agents/bulk_send.py                     # Bulk
```

### 📖 Read Documentation

```bash
# Start here
open docs/GETTING_STARTED.md

# Learn about ReAct
open docs/README_REACT.md

# Compare agents
open docs/AGENT_COMPARISON.md
```

### 🧪 Test & Debug

```bash
python tests/test_react.py              # Test ReAct agent
python tests/troubleshoot_email.py      # Debug email issues
```

## File Descriptions

### Agents (`agents/`)

- **ai_email_agent_react_openai.py** ⭐ - OpenAI with ReAct pattern (RECOMMENDED)
  - Shows AI reasoning transparently
  - Natural language interface
  - Full transparency into decisions

- **ai_email_agent_react.py** - Claude with ReAct pattern
  - Alternative to OpenAI version
  - Same transparency features

- **ai_email_agent_openai.py** - Traditional OpenAI agent
  - Faster execution
  - No reasoning shown
  - Natural language interface

- **ai_email_agent.py** - Traditional Claude agent
  - Alternative to OpenAI
  - Fast execution

- **send_email_cli.py** - Command line interface
  - No AI needed
  - Direct control
  - Scriptable

- **bulk_send.py** - Bulk email sender
  - Send to multiple recipients
  - Reads from JSON/CSV files
  - Efficient batch processing

### Core (`core/`)

- **email_agent.py** - Core SMTP implementation
  - Gmail/SMTP email sending
  - HTML template generation
  - CC and attachment support

- **email_agent_sendgrid.py** - SendGrid alternative
  - SendGrid API integration
  - Same interface as SMTP version

### Documentation (`docs/`)

- **GETTING_STARTED.md** ⭐ - Complete getting started guide
- **README_REACT.md** - Deep dive into ReAct pattern
- **AGENT_COMPARISON.md** - Compare all 4 agent types
- **QUICKSTART.md** - Quick reference guide
- **README_AI_AGENT.md** - Traditional AI agents
- **README.md** - Project overview

### Demos (`demos/`)

- **demo_react.py** - Interactive comparison of Traditional vs ReAct agents
- **demo.py** - Email preview without sending

### Tests (`tests/`)

- **test_react.py** - Test ReAct agent functionality
- **test_ai_agent.py** - Test AI agent setup
- **troubleshoot_email.py** - Email debugging tool

### Examples (`examples/`)

- **recipients_example.json** - JSON format example
- **recipients_example.csv** - CSV format example  
- **lecture01_recipients.json** - Lecture 1 template

### Utils (`utils/`)

- **setup.sh** - Automated setup script

## Import Paths

All Python files now need to be run from the project root:

```bash
# From project root
cd /Users/ash/Desktop/AgenticAI@UIUC

# Run agents
python agents/ai_email_agent_react_openai.py

# Run demos
python demos/demo_react.py

# Run tests
python tests/test_react.py
```

## Configuration Files

- **`.env`** - Your actual credentials (keep secret!)
- **`.env.example`** - Template for credentials
- **`requirements.txt`** - Python package dependencies
- **`.gitignore`** - Files to exclude from git

## Next Steps

1. **Read the docs**: Start with `docs/GETTING_STARTED.md`
2. **Try the demo**: Run `python demos/demo_react.py`
3. **Use the agent**: Run `python agents/ai_email_agent_react_openai.py`

---

**Need help?** Check `docs/GETTING_STARTED.md` or contact ashleyn4@illinois.edu
