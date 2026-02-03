# 🧠 ReAct AI Email Agent

## What is ReAct?

**ReAct = Reasoning + Acting**

Instead of just executing tools blindly, the agent:
1. **Thinks** about what needs to be done
2. **Plans** the approach
3. **Acts** by using tools
4. **Observes** the results
5. **Reflects** and decides next steps
6. **Repeats** until task is complete

This makes the AI's decision-making process **transparent and interpretable**.

## How It Works

### Traditional Agent (Black Box)
```
User: "Email john@test.com about lecture 1"
Agent: [silently uses tool]
Agent: "Done! ✅"
```

### ReAct Agent (Transparent)
```
User: "Email john@test.com about lecture 1"

Thought: The user wants to send a thank you email to john@test.com for 
         attending lecture 1. I need to use the send_email tool with the
         recipient's email and include lecture details.

Action: Using send_email tool with:
        - email: john@test.com
        - topic: Introduction to AI Agents
        - link: https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01
        - cc: ashleyn4@illinois.edu

Observation: Email sent successfully to john@test.com

Thought: The task is complete. I should confirm with the user.

Action: Final Answer: I've successfully sent a thank you email to 
        john@test.com for attending Lecture 1 on Introduction to AI Agents!
```

## Usage

### Run the ReAct Agent

```bash
# Using OpenAI (Recommended)
python ai_email_agent_react_openai.py

# Or using Anthropic Claude
python ai_email_agent_react.py
```

### Example Session

```
💬 You: Send email to alice@test.com and bob@test.com

🧠 ReAct AI Email Agent
======================================================================

📝 Your Request: Send email to alice@test.com and bob@test.com

======================================================================

🔄 Iteration 1
----------------------------------------------------------------------

Thought: The user wants to send emails to two recipients: alice@test.com 
and bob@test.com. Since there are multiple recipients, I should use the 
send_bulk_emails tool for efficiency. I'll include default lecture 
information and CC ashleyn4@illinois.edu.

Action: I will use the send_bulk_emails tool.

----------------------------------------------------------------------
🔧 Action: Using tool 'send_bulk_emails'
📋 Parameters:
{
  "recipients": [
    {
      "email": "alice@test.com",
      "name": "Alice",
      "lecture_topic": "Introduction to AI Agents",
      "lecture_link": "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
      "cc_email": "ashleyn4@illinois.edu"
    },
    {
      "email": "bob@test.com",
      "name": "Bob",
      "lecture_topic": "Introduction to AI Agents",
      "lecture_link": "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
      "cc_email": "ashleyn4@illinois.edu"
    }
  ]
}

✅ Result: Bulk send complete

----------------------------------------------------------------------
🔄 Iteration 2
----------------------------------------------------------------------

Observation: Successfully sent emails to both recipients (2 out of 2 
emails sent). The emails included information about the Introduction to 
AI Agents lecture and links to the course materials.

Thought: The task is complete. Both emails were sent successfully.

Action: Final Answer: I've successfully sent thank you emails to both 
Alice (alice@test.com) and Bob (bob@test.com) for attending the 
Introduction to AI Agents lecture! Both emails include the course 
materials link and Ashley has been CC'd. ✅

======================================================================
✅ Task Complete!
======================================================================
```

## Benefits of ReAct

### 1. **Transparency**
You can see exactly what the AI is thinking and why it makes decisions.

### 2. **Debugging**
If something goes wrong, you can see where the reasoning failed.

### 3. **Trust**
Understanding the AI's thought process builds confidence in its actions.

### 4. **Learning**
Watch how the AI breaks down complex tasks into steps.

### 5. **Control**
You can interrupt if you see the AI reasoning incorrectly.

## Comparison

| Feature | Traditional Agent | ReAct Agent |
|---------|------------------|-------------|
| Speed | Faster | Slightly slower |
| Transparency | ❌ Black box | ✅ Full visibility |
| Debugging | Hard | Easy |
| Cost | Lower | Slightly higher (more tokens) |
| Trust | Lower | Higher |
| Learning | None | Educational |

## When to Use ReAct

**Use ReAct when:**
- You want to understand the AI's reasoning
- Debugging complex workflows
- Building trust with users
- Educational purposes
- Critical tasks requiring transparency

**Use Traditional Agent when:**
- Speed is critical
- Simple, straightforward tasks
- Cost optimization is important
- You trust the AI's decisions

## Examples

### Example 1: Single Email
```
💬 You: Thank john@illinois.edu for coming to the lecture

Thought: Need to send one thank you email. I'll use send_email tool with
         default lecture information.

Action: Using send_email tool with john@illinois.edu

Observation: Email sent successfully

Thought: Task complete!

Final Answer: Done! ✅
```

### Example 2: Multiple Emails
```
💬 You: Email these students: alice@test.com, bob@test.com, carol@test.com

Thought: Three recipients detected. I should use send_bulk_emails for 
         efficiency rather than sending three separate emails.

Action: Using send_bulk_emails with 3 recipients

Observation: All 3 emails sent successfully

Thought: All emails delivered. Task complete.

Final Answer: Successfully sent thank you emails to all 3 students! ✅
```

### Example 3: Complex Request
```
💬 You: Send lecture materials to john@test.com and make sure to mention
        that office hours are tomorrow at 3pm

Thought: This requires sending an email with custom message about office
         hours. I'll include that in the custom_message parameter.

Action: Using send_email with custom message about office hours

Observation: Email sent with custom message included

Thought: Perfect! The email included both the lecture materials and the
         office hours reminder.

Final Answer: Sent! John will receive the materials and office hours info. ✅
```

## Setup

Same as the regular AI agent:

```bash
# 1. Make sure you have dependencies
pip install -r requirements.txt

# 2. Add OpenAI API key to .env
echo "OPENAI_API_KEY=your-key-here" >> .env

# 3. Run the ReAct agent
python ai_email_agent_react_openai.py

# Or use Anthropic Claude instead
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
python ai_email_agent_react.py
```

## Architecture

```
User Query
    ↓
┌─────────────────────────────────────────┐
│  1. THOUGHT: Analyze request            │
│     "User wants to email 2 people..."   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  2. ACTION: Choose tool                 │
│     "Use send_bulk_emails tool"         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  3. EXECUTE: Run tool                   │
│     [Email API called]                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  4. OBSERVATION: Review result          │
│     "2 emails sent successfully"        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  5. THOUGHT: Check if done              │
│     "Task complete!"                    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  6. FINAL ANSWER: Respond to user       │
│     "Emails sent! ✅"                   │
└─────────────────────────────────────────┘
```

## Tips

1. **Watch the reasoning** - The agent shows its thought process at each step
2. **Learn from it** - See how AI breaks down tasks
3. **Debug easily** - If something goes wrong, you know exactly where
4. **Trust the process** - Full transparency builds confidence

## Troubleshooting

### Agent loops forever?
- Check the system prompt
- Make sure the agent knows when to stop
- Set max_iterations limit (default: 10)

### Reasoning doesn't make sense?
- Try rephrasing your request
- Be more specific about what you want
- Check the logs to see where reasoning diverged

### Too slow?
- Use the regular agent (`ai_email_agent.py`) instead
- ReAct trades speed for transparency

---

**Enjoy transparent, interpretable AI! 🧠✨**
