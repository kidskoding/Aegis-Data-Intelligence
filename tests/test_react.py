#!/usr/bin/env python3
"""
Quick test of the ReAct AI Email Agent.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Check for API keys
has_openai = bool(os.getenv("OPENAI_API_KEY"))
has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

print("=" * 70)
print("🧪 ReAct Email Agent - Quick Test")
print("=" * 70)

if not has_openai and not has_anthropic:
    print("\n❌ No AI API key found!")
    print("\nTo use the ReAct AI Email Agent, you need an API key:")
    print("\n📝 Option 1: OpenAI (Recommended)")
    print("   1. Get key: https://platform.openai.com/api-keys")
    print("   2. Add to .env: OPENAI_API_KEY=your-key-here")
    print("   3. Run: python ai_email_agent_react_openai.py")
    print("\n📝 Option 2: Anthropic Claude")
    print("   1. Get key: https://console.anthropic.com/")
    print("   2. Add to .env: ANTHROPIC_API_KEY=your-key-here")
    print("   3. Run: python ai_email_agent_react.py")
    print("\n" + "=" * 70)
    exit(1)

if has_openai:
    print("\n✅ OpenAI API key found!")
    print("\nTesting ReAct Email Agent with OpenAI GPT-4...\n")
    
    from ai_email_agent_react_openai import ReActEmailAgentOpenAI
    
    agent = ReActEmailAgentOpenAI()
    
    # Test query
    test_query = "Send a test thank you email to test@example.com for attending Lecture 1 on AI Agents"
    
    print(f"Test Query: {test_query}\n")
    print("-" * 70)
    
    response = agent.process_request(test_query)
    
    print("-" * 70)
    print(f"\n✅ ReAct Agent Response:\n{response}\n")
    print("=" * 70)
    print("\n🎉 Success! The ReAct agent is working with OpenAI!")
    print("\nNotice how the agent:")
    print("  💭 Showed its thinking")
    print("  🎯 Explained its actions")
    print("  👀 Observed the results")
    print("  ✅ Confirmed completion")
    print("\nTo use interactively, run:")
    print("  python ai_email_agent_react_openai.py")
    
elif has_anthropic:
    print("\n✅ Anthropic API key found!")
    print("\nTesting ReAct Email Agent with Claude...\n")
    
    from ai_email_agent_react import ReActEmailAgent
    
    agent = ReActEmailAgent()
    
    # Test query
    test_query = "Send a test thank you email to test@example.com for attending Lecture 1 on AI Agents"
    
    print(f"Test Query: {test_query}\n")
    print("-" * 70)
    
    response = agent.process_request(test_query)
    
    print("-" * 70)
    print(f"\n✅ ReAct Agent Response:\n{response}\n")
    print("=" * 70)
    print("\n🎉 Success! The ReAct agent is working with Claude!")
    print("\nNotice how the agent:")
    print("  💭 Showed its thinking")
    print("  🎯 Explained its actions")
    print("  👀 Observed the results")
    print("  ✅ Confirmed completion")
    print("\nTo use interactively, run:")
    print("  python ai_email_agent_react.py")
