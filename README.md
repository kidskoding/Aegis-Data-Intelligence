# 🧠 AI Email Agent - AgenticAI@UIUC

An intelligent email agent using the ReAct pattern (Reasoning + Acting) with OpenAI GPT-4, designed to send professional thank you emails to lecture attendees.

## ✨ Features

- 🧠 **ReAct Pattern** - AI shows its reasoning before acting
- 🤖 **OpenAI GPT-4** - Industry-standard AI integration
- 📧 **Multiple Interfaces** - ReAct, Traditional AI, CLI, and Bulk sending
- 🔍 **Full Transparency** - See exactly how AI makes decisions
- 📝 **Professional Templates** - Beautiful HTML email formatting
- ⚙️ **Fully Configured** - Ready to use out of the box

## 🚀 Quick Start

### 1. See the Demo
```bash
python demos/demo_react.py
```

### 2. Run the ReAct Agent (Recommended)
```bash
python agents/ai_email_agent_react_openai.py
```

Then type:
```
💬 You: Send email to student@illinois.edu about lecture 1
```

### 3. Or Use CLI (No AI needed)
```bash
python agents/send_email_cli.py \
  --email student@illinois.edu \
  --name "Student Name" \
  --topic "AI Agents Lecture"
```

## 📁 Project Structure

```
AgenticAI@UIUC/
├── agents/              → AI agents and sending tools
│   ├── ai_email_agent_react_openai.py  ⭐ ReAct with OpenAI
│   ├── ai_email_agent_react.py         ← ReAct with Claude
│   ├── ai_email_agent_openai.py        ← Traditional OpenAI
│   ├── ai_email_agent.py               ← Traditional Claude
│   ├── send_email_cli.py               ← Command line tool
│   └── bulk_send.py                    ← Bulk sender
│
├── core/                → Core email logic
│   ├── email_agent.py                  ← SMTP implementation
│   └── email_agent_sendgrid.py         ← SendGrid implementation
│
├── docs/                → Documentation
│   ├── GETTING_STARTED.md              ⭐ Start here
│   ├── README_REACT.md                 ← ReAct pattern explained
│   ├── AGENT_COMPARISON.md             ← Compare all agents
│   ├── QUICKSTART.md                   ← Quick reference
│   └── README_AI_AGENT.md              ← Traditional AI docs
│
├── demos/               → Demo scripts
│   ├── demo_react.py                   ← Compare agents
│   └── demo.py                         ← Email preview
│
├── tests/               → Test scripts
│   ├── test_react.py                   ← Test ReAct agent
│   ├── test_ai_agent.py                ← Test AI setup
│   └── troubleshoot_email.py           ← Email debugging
│
├── examples/            → Example data
│   ├── recipients_example.json
│   ├── recipients_example.csv
│   └── lecture01_recipients.json
│
├── utils/               → Utilities
│   └── setup.sh                        ← Setup script
│
├── .env                 → Your credentials (configured!)
├── .env.example         → Template
├── requirements.txt     → Dependencies
└── README.md            → This file
```

## 📖 Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** ⭐ - Complete getting started guide
- **[README_REACT.md](docs/README_REACT.md)** - ReAct pattern deep dive
- **[AGENT_COMPARISON.md](docs/AGENT_COMPARISON.md)** - Compare all 4 agent types
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick reference guide

## 🧠 What is ReAct?

**ReAct = Reasoning + Acting**

The agent shows you exactly how it thinks:

```
💬 You: "Email john@test.com"

💭 Thought: User wants to email john@test.com. I'll use send_email 
           with lecture details and CC ashleyn4@illinois.edu.

🎯 Action: Using send_email tool

🔧 Executing...

👀 Observation: Email sent successfully!

💭 Thought: Task complete!

✅ Final Answer: Email sent! ✓
```

## 🎯 Usage Examples

### Example 1: ReAct Agent
```bash
python agents/ai_email_agent_react_openai.py
# Type: "send email to john@test.com about AI Agents lecture"
```

### Example 2: Command Line
```bash
python agents/send_email_cli.py \
  --email john@test.com \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01"
```

### Example 3: Bulk Send
```bash
python agents/bulk_send.py --file examples/lecture01_recipients.json
```

## ⚙️ Configuration

Already configured in `.env`:
```env
# Email
SMTP_SERVER=smtp.gmail.com
SENDER_EMAIL=agenticaiuiuc@gmail.com
SENDER_PASSWORD=*** (configured)

# AI
OPENAI_API_KEY=*** (configured)
```

## 🔧 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the setup script
./utils/setup.sh
```

## 🧪 Testing

```bash
# Test ReAct agent
python tests/test_react.py

# Test AI setup
python tests/test_ai_agent.py

# Troubleshoot email
python tests/troubleshoot_email.py your@email.com
```

## 📚 Learn More

- **Research Paper**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- **OpenAI Docs**: https://platform.openai.com/docs
- **Project Docs**: Start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## 🎓 Course Information

- **Course**: AgenticAI@UIUC
- **Lecture Materials**: https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01
- **Contact**: ashleyn4@illinois.edu

## 📝 License

MIT License - Feel free to use and modify!

---

**🎉 Your AI email agent is ready!** Start with `python demos/demo_react.py` to see it in action.
