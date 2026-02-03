# 🤖 AI Email Agent - Natural Language Interface

An intelligent agent that understands natural language requests and automatically sends emails using LLM technology.

## What is This?

Instead of manually specifying email parameters, just **tell the AI what you want** in plain English:

```
"Send a thank you email to john@example.com for attending lecture 1"
```

The AI will understand your request, extract the details, and send the email automatically!

## Features

- 🧠 **Natural Language Understanding** - Just describe what you want
- 🔧 **Tool Use** - AI uses email API as a tool
- 📧 **Smart Defaults** - Automatically uses AgenticAI@UIUC context
- 🎯 **Context Aware** - Knows about your lectures and materials
- 💬 **Conversational** - Interactive chat interface

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get an AI API Key

You have two options:

**Option A: Anthropic Claude (Recommended)**
- Get API key: https://console.anthropic.com/
- Add to `.env`: `ANTHROPIC_API_KEY=your-key-here`
- Use: `python ai_email_agent.py`

**Option B: OpenAI GPT-4**
- Get API key: https://platform.openai.com/api-keys
- Add to `.env`: `OPENAI_API_KEY=your-key-here`
- Use: `python ai_email_agent_openai.py`

### 3. Configure Email (Already Done!)

Make sure your `.env` has email credentials (SMTP or SendGrid).

## Usage

### Interactive Mode

```bash
# Using Claude
python ai_email_agent.py

# Using OpenAI
python ai_email_agent_openai.py
```

Then just chat with the AI:

```
💬 You: Send a thank you email to john@example.com for attending lecture 1
🤖 Agent: I've sent a thank you email to john@example.com! ✅

💬 You: Email alice@test.com and bob@test.com about today's AI Agents lecture
🤖 Agent: Done! I've sent emails to both Alice and Bob. ✅
```

## Example Requests

### Single Email
```
"Send a thank you email to student@illinois.edu for coming to lecture"
"Thank john.doe@example.com for attending the AI Agents session"
```

### Multiple Emails
```
"Email these students: alice@test.com, bob@test.com, carol@test.com"
"Send thank you emails to john@a.com and jane@b.com for the lecture"
```

### With Details
```
"Email student@test.com about Lecture 1 on Introduction to AI Agents, 
include the GitHub link, and CC ashleyn4@illinois.edu"
```

### Contextual
```
"Thank everyone who came to today's lecture"
"Send lecture materials to all attendees"
```

## How It Works

1. **You speak naturally**: "Send an email to john@example.com"
2. **AI understands**: Extracts recipient, topic, message
3. **AI uses tools**: Calls the email API with correct parameters
4. **Email sent**: Professional thank you email delivered
5. **AI confirms**: "Done! Email sent to john@example.com ✅"

## Smart Defaults

The AI agent automatically includes:
- ✅ Default CC: `ashleyn4@illinois.edu`
- ✅ Default lecture link: `https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01`
- ✅ Professional thank you message
- ✅ Proper email formatting

## Architecture

```
User Query → LLM (Claude/GPT-4) → Tool Call → Email API → Email Sent
              ↑                                               ↓
              └──────────── Confirmation ────────────────────┘
```

The AI has access to two tools:
1. `send_email` - Send to one recipient
2. `send_bulk_emails` - Send to multiple recipients

## Cost

- **Anthropic Claude**: ~$0.01-0.03 per request
- **OpenAI GPT-4**: ~$0.02-0.05 per request

Very affordable for typical usage!

## Comparison: Traditional vs AI Agent

**Traditional CLI:**
```bash
python send_email_cli.py \
  --email student@example.com \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --link "https://github.com/..." \
  --cc "ashleyn4@illinois.edu"
```

**AI Agent:**
```
💬 You: Email John Doe at student@example.com about the AI Agents lecture
```

Much easier! 🎉

## Troubleshooting

### "Missing API key" error
- Make sure you've added `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` to `.env`
- Get keys from console.anthropic.com or platform.openai.com

### Email not sending
- Check that your email credentials (SMTP_SERVER, SENDER_EMAIL, etc.) are in `.env`
- Refer to main README.md for email setup

### AI not understanding
- Be more specific: include email addresses, lecture numbers, topics
- Example: "Email john@test.com about Lecture 1" works better than "send email"

## Examples in Action

```
💬 You: send thank you to alice@test.com for attending

🤖 AI Agent processing your request...

🔧 Using tool: send_email
📋 Input: {
  "recipient_email": "alice@test.com",
  "recipient_name": "Alice",
  "lecture_topic": "Introduction to AI Agents",
  "lecture_link": "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
  "cc_email": "ashleyn4@illinois.edu"
}

✅ Tool result: {
  "status": "success",
  "message": "Thank you email sent successfully to alice@test.com"
}

🤖 Agent: I've successfully sent a thank you email to alice@test.com! 
The email includes information about the Introduction to AI Agents lecture 
and a link to the materials. Ashley has been CC'd on the email. ✅
```

## Next Steps

1. Try the interactive mode with sample emails
2. Send real emails to your lecture attendees
3. Customize the system prompt in the code for your specific needs
4. Integrate with your attendance system for automatic emails

Enjoy your AI-powered email assistant! 🚀
