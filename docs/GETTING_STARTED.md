# 🚀 Getting Started with Your AI Email Agent

## ✅ Everything is Ready!

Your AI email agent is **fully configured** and ready to use with **OpenAI GPT-4**.

### Current Configuration

```
✅ Email: agenticaiuiuc@gmail.com (Gmail SMTP)
✅ AI Model: OpenAI GPT-4 Turbo  
✅ Pattern: ReAct (Reasoning + Acting)
✅ Test: Email sent successfully!
```

---

## 🎯 Choose Your Style

### Option 1: ReAct Agent (RECOMMENDED) 🧠

**Shows AI's thinking process!**

```bash
python ai_email_agent_react_openai.py
```

**What you'll see:**
```
💬 You: Email john@test.com about lecture 1

💭 Thought: User wants to email john@test.com. I'll use send_email 
           with lecture details and CC ashleyn4@illinois.edu.

🎯 Action: Using send_email tool

🔧 Executing...

👀 Observation: Email sent successfully!

💭 Thought: Task complete!

✅ Final Answer: Email sent to john@test.com! ✓
```

**Why use this?**
- See exactly how AI makes decisions
- Full transparency
- Educational
- Easy to debug

---

### Option 2: Command Line Interface 📧

**No AI needed - direct control!**

```bash
python send_email_cli.py \
  --email student@illinois.edu \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01" \
  --cc ashleyn4@illinois.edu
```

**Why use this?**
- No API costs
- Full control
- Scriptable
- Fast

---

### Option 3: Bulk Sending 📊

**Send to many people at once!**

1. Create `recipients.json`:
```json
[
  {
    "email": "student1@illinois.edu",
    "name": "Alice",
    "lecture_topic": "Introduction to AI Agents",
    "lecture_link": "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
    "cc_email": "ashleyn4@illinois.edu"
  },
  {
    "email": "student2@illinois.edu",
    "name": "Bob",
    "lecture_topic": "Introduction to AI Agents",
    "lecture_link": "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
    "cc_email": "ashleyn4@illinois.edu"
  }
]
```

2. Run:
```bash
python bulk_send.py --file recipients.json
```

**Why use this?**
- Efficient for classes
- Organized data
- Reusable lists

---

## 📝 Quick Examples

### Send One Email (Natural Language)
```bash
python ai_email_agent_react_openai.py
# Then type: "Send email to john@test.com about AI Agents lecture"
```

### Send One Email (CLI)
```bash
python send_email_cli.py \
  --email john@test.com \
  --name "John Doe" \
  --topic "AI Agents"
```

### Send Multiple Emails
```bash
python bulk_send.py --file my_students.json
```

---

## 🎬 Try the Demos First!

### Demo 1: See Email Preview
```bash
python demo.py
```
Shows what emails look like without sending anything.

### Demo 2: Compare Agents
```bash
python demo_react.py
```
Shows difference between traditional and ReAct agents.

### Demo 3: Test ReAct Agent
```bash
python test_react.py
```
Tests your ReAct agent with OpenAI.

---

## 📁 File Guide

### Main Agents
- `ai_email_agent_react_openai.py` ⭐ **Recommended** - OpenAI with reasoning
- `ai_email_agent_react.py` - Claude with reasoning  
- `send_email_cli.py` - Command line interface
- `bulk_send.py` - Bulk sender

### Core Logic
- `email_agent.py` - Email sending logic (SMTP)
- `email_agent_sendgrid.py` - Alternative SendGrid version

### Demos & Tests
- `demo.py` - Email preview demo
- `demo_react.py` - Compare agents
- `test_react.py` - Test ReAct agent

### Documentation
- `GETTING_STARTED.md` ⭐ **You are here**
- `README_REACT.md` - ReAct pattern explained
- `AGENT_COMPARISON.md` - Compare all agents
- `QUICKSTART.md` - Quick reference
- `README.md` - Main docs

---

## 💡 Common Tasks

### Task: Email One Student
**Use:** CLI or ReAct Agent
```bash
python send_email_cli.py --email student@test.com --name "Student"
```

### Task: Email Entire Class
**Use:** Bulk Sender
```bash
python bulk_send.py --file lecture01_students.json
```

### Task: See How AI Thinks
**Use:** ReAct Agent
```bash
python ai_email_agent_react_openai.py
```

### Task: No AI Costs
**Use:** CLI
```bash
python send_email_cli.py --email test@test.com
```

---

## 🔧 Configuration

Your `.env` file is already configured with:

```env
# Email (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=agenticaiuiuc@gmail.com
SENDER_PASSWORD=*** (configured)

# AI
OPENAI_API_KEY=*** (configured)
```

---

## ❓ Troubleshooting

### Email not sending?
- Check Gmail credentials in `.env`
- Make sure using App-Specific Password
- Test with: `python send_email_cli.py --email your@email.com`

### AI agent not working?
- Check OpenAI key in `.env`
- Verify key at: https://platform.openai.com/api-keys
- Test with: `python test_react.py`

### Want to see what happens without sending?
```bash
python demo.py
```

---

## 🎓 Next Steps

1. **Try the ReAct demo:**
   ```bash
   python demo_react.py
   ```

2. **Send a test email:**
   ```bash
   python ai_email_agent_react_openai.py
   # Type: "send test email to your@email.com"
   ```

3. **Read the docs:**
   - Start with `README_REACT.md`
   - Check `AGENT_COMPARISON.md` to pick the best agent

4. **Send real emails:**
   - Use CLI for individual emails
   - Use bulk for entire class

---

## 📚 Learn More

- **ReAct Pattern:** See how AI thinks before acting
- **Paper:** https://arxiv.org/abs/2210.03629
- **OpenAI Docs:** https://platform.openai.com/docs

---

**🎉 You're all set! Start by running `python demo_react.py`**

Questions? Check the documentation or contact ashleyn4@illinois.edu
