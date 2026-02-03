# 🚀 Quick Start Guide

## What You Have

You now have **4 ways** to send thank you emails:

### 1. 🧠 ReAct AI Agent (BEST - Shows Reasoning!)
**AI explains its thinking, then acts!**

```bash
# Using OpenAI (Recommended)
python ai_email_agent_react_openai.py

# Or using Claude
python ai_email_agent_react.py
```

The agent will:
- 💭 **Think**: Analyze your request
- 🎯 **Plan**: Decide what to do
- 🔧 **Act**: Use tools
- 👀 **Observe**: Check results
- ✅ **Confirm**: Tell you it's done

**Need:** OpenAI API key (or Anthropic)
- Get it: https://platform.openai.com/api-keys
- Add to `.env`: `OPENAI_API_KEY=your-key`
- **Benefit**: Full transparency into AI decision-making!

---

### 2. 🤖 AI Agent (FAST - Natural Language)
**Just tell the AI what you want!**

```bash
python ai_email_agent.py
```

Then type:
```
💬 Send a thank you email to student@illinois.edu for attending lecture 1
```

**Need:** Anthropic API key (or OpenAI)
- Get it: https://console.anthropic.com/
- Add to `.env`: `ANTHROPIC_API_KEY=your-key`

---

### 3. 📧 Command Line Interface (SIMPLE)
**Specify parameters directly**

```bash
python send_email_cli.py \
  --email student@illinois.edu \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01" \
  --cc ashleyn4@illinois.edu
```

**Need:** Email credentials only (already configured!)

---

### 4. 📊 Bulk Sending (FOR MULTIPLE RECIPIENTS)
**Send to many people at once**

Create a file `recipients.json`:
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

Then run:
```bash
python bulk_send.py --file recipients.json
```

**Need:** Email credentials only

---

## Current Status

✅ Email credentials configured (Gmail SMTP)  
✅ Packages installed  
✅ Test email sent successfully to ashleyn4@illinois.edu  
❓ AI API key needed (for AI agent only)

## Next Steps

### Option A: Use AI Agent (Recommended)

1. Get Anthropic API key: https://console.anthropic.com/
2. Add to `.env`: 
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
3. Run: `python ai_email_agent.py`
4. Chat naturally: "Send email to student@test.com about lecture 1"

### Option B: Use CLI Directly

Already working! Just run:
```bash
python send_email_cli.py \
  --email RECIPIENT_EMAIL \
  --name "Student Name" \
  --topic "Lecture Topic" \
  --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01" \
  --cc ashleyn4@illinois.edu
```

### Option C: Bulk Send

1. Create a JSON or CSV file with recipients
2. Run: `python bulk_send.py --file your-file.json`

---

## Examples

### Send One Email (CLI)
```bash
python send_email_cli.py \
  --email john.doe@illinois.edu \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01" \
  --cc ashleyn4@illinois.edu
```

### Send One Email (AI Agent)
```bash
python ai_email_agent.py
# Then type: "Email john.doe@illinois.edu about lecture 1"
```

### Send Multiple Emails
```bash
python bulk_send.py --file lecture01_recipients.json
```

---

## Files Overview

- `ai_email_agent.py` - AI agent using Claude (natural language)
- `ai_email_agent_openai.py` - AI agent using OpenAI GPT-4
- `send_email_cli.py` - Simple command-line interface
- `bulk_send.py` - Bulk email sender
- `email_agent.py` - Core email logic (SMTP)
- `email_agent_sendgrid.py` - Alternative using SendGrid
- `demo.py` - Demo without sending real emails
- `.env` - Your credentials (keep secret!)

---

## Help & Docs

- **AI Agent**: See `README_AI_AGENT.md`
- **Full Docs**: See `README.md`
- **Examples**: See `recipients_example.json` and `recipients_example.csv`

---

## Troubleshooting

### Email not sending?
- Check `.env` has correct SMTP credentials
- Gmail users: make sure you're using App-Specific Password

### AI agent not working?
- Make sure you have `ANTHROPIC_API_KEY` in `.env`
- Get it from: https://console.anthropic.com/

### Need help?
- Check the README files
- Run `python demo.py` to see what emails look like
- Contact: ashleyn4@illinois.edu

---

**You're all set! 🎉**
