#!/bin/bash
# Quick launcher script for the AI Email Agent

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                       ║"
echo "║             🧠 AI EMAIL AGENT - AgenticAI@UIUC                       ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose an option:"
echo ""
echo "  1. 🧠 ReAct Agent (OpenAI) - Shows AI reasoning"
echo "  2. 🎭 Demo - Compare Traditional vs ReAct"
echo "  3. 📧 CLI - Send single email"
echo "  4. 📊 Bulk - Send to multiple recipients"
echo "  5. 🧪 Test - Test the system"
echo "  6. 🔍 Troubleshoot - Debug email issues"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
  1)
    echo ""
    echo "🧠 Starting ReAct Agent..."
    python agents/ai_email_agent_react_openai.py
    ;;
  2)
    echo ""
    echo "🎭 Starting demo..."
    python demos/demo_react.py
    ;;
  3)
    echo ""
    read -p "Recipient email: " email
    read -p "Recipient name: " name
    read -p "Lecture topic: " topic
    python agents/send_email_cli.py \
      --email "$email" \
      --name "$name" \
      --topic "$topic" \
      --link "https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01"
    ;;
  4)
    echo ""
    read -p "Path to recipient file (JSON/CSV): " file
    python agents/bulk_send.py --file "$file"
    ;;
  5)
    echo ""
    echo "🧪 Running tests..."
    python tests/test_react.py
    ;;
  6)
    echo ""
    read -p "Email address to test: " email
    python tests/troubleshoot_email.py "$email"
    ;;
  *)
    echo "Invalid choice"
    ;;
esac
