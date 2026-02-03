# AI Email Agent for Lecture Thank You Messages

An AI agent that automatically sends professional thank you emails to lecture attendees.

## 🧠 NEW: ReAct AI Agent (Reasoning + Acting)

**The AI shows its thinking, then acts! Full transparency!**

```
💬 You: Send a thank you email to john@example.com for attending lecture 1

💭 Thought: User wants to email john@example.com. I'll use send_email tool 
           with lecture 1 details and CC ashleyn4@illinois.edu.

🔧 Action: Using send_email tool...

👀 Observation: Email sent successfully!

✅ Done! Email sent to john@example.com
```

**See the AI's reasoning at every step!**
- 📖 [README_REACT.md](README_REACT.md) - ReAct documentation
- 📖 [README_AI_AGENT.md](README_AI_AGENT.md) - Traditional AI agent

## Try it First!

Want to see what the agent does before setting up email credentials?

```bash
python demo.py
```

This runs an interactive demo showing email previews without sending anything.

## Features

- ✉️ Send personalized thank you emails to lecture attendees
- 📧 Support for both SMTP and SendGrid APIs
- 🎨 Beautiful HTML email templates
- 📊 Bulk email sending capability
- 🔧 Customizable messages and lecture topics

## Quick Start

### Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your email credentials

# Activate virtual environment
source venv/bin/activate

# Send a test email
python send_email_cli.py --email your-email@example.com --name "Test User"
```

## Manual Setup

### 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Email Credentials

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your actual credentials:

#### Option A: Using SMTP (Gmail, Outlook, etc.)

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App-Specific Password: https://myaccount.google.com/apppasswords
3. Use the app-specific password (not your regular Gmail password)

#### Option B: Using SendGrid

```env
SENDGRID_API_KEY=your-sendgrid-api-key
SENDER_EMAIL=your-verified-sender@example.com
```

**For SendGrid:**
1. Sign up at https://sendgrid.com
2. Create an API key in Settings > API Keys
3. Verify your sender email address

## Usage

### Using SMTP Version

```python
from email_agent import EmailAgent

# Initialize the agent
agent = EmailAgent()

# Send a single thank you email
result = agent.send_thank_you_email(
    recipient_email="student@example.com",
    recipient_name="John Doe",
    lecture_topic="Introduction to AI Agents",
    custom_message="We look forward to seeing you in the next session!"
)

print(result)
```

### Using SendGrid Version

```python
from email_agent_sendgrid import SendGridEmailAgent

# Initialize the agent
agent = SendGridEmailAgent()

# Send a single thank you email
result = agent.send_thank_you_email(
    recipient_email="student@example.com",
    recipient_name="John Doe",
    lecture_topic="Introduction to AI Agents"
)

print(result)
```

### Bulk Email Sending

```python
recipients = [
    {
        "email": "student1@example.com",
        "name": "Alice Smith",
        "lecture_topic": "Machine Learning Basics"
    },
    {
        "email": "student2@example.com",
        "name": "Bob Johnson",
        "lecture_topic": "Machine Learning Basics"
    }
]

result = agent.send_bulk_thank_you_emails(recipients)
print(result)
```

## Running the Example

```bash
# For SMTP version
python email_agent.py

# For SendGrid version
python email_agent_sendgrid.py
```

## Command Line Interface (CLI)

### Send a Single Email

```bash
# Basic usage
python send_email_cli.py --email student@example.com

# With all options
python send_email_cli.py \
  --email student@example.com \
  --name "John Doe" \
  --topic "Introduction to AI Agents" \
  --message "We look forward to seeing you next time!" \
  --provider smtp
```

### Bulk Send Emails

Create a CSV or JSON file with recipient data (see `recipients_example.csv` or `recipients_example.json`), then:

```bash
# From CSV file
python bulk_send.py --file recipients.csv --provider smtp

# From JSON file
python bulk_send.py --file recipients.json --provider sendgrid
```

**CSV Format:**
```csv
email,name,lecture_topic,custom_message
student@example.com,John Doe,AI Basics,See you next week!
```

**JSON Format:**
```json
[
  {
    "email": "student@example.com",
    "name": "John Doe",
    "lecture_topic": "AI Basics",
    "custom_message": "See you next week!"
  }
]
```

## Email Template

The agent sends professionally formatted emails with:
- Personalized greeting
- Lecture topic (if provided)
- Thank you message
- Custom message (optional)
- HTML styling for better presentation

## API Response Format

```json
{
  "status": "success",
  "message": "Thank you email sent successfully to student@example.com",
  "recipient": "student@example.com"
}
```

## Security Notes

- Never commit your `.env` file to version control
- Use app-specific passwords for Gmail (not your main password)
- Keep your API keys secure
- The `.env` file is already in `.gitignore`

## Troubleshooting

### Gmail SMTP Issues
- Make sure 2FA is enabled
- Use an app-specific password, not your regular password
- Allow less secure apps if needed (not recommended)

### SendGrid Issues
- Verify your sender email address in SendGrid dashboard
- Check that your API key has mail send permissions
- Ensure you're within your SendGrid sending limits

## License

MIT License - Feel free to use and modify as needed!
