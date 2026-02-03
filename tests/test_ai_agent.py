#!/usr/bin/env python3
"""
Quick test of the AI Email Agent with a sample request.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Check for API keys
has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
has_openai = bool(os.getenv("OPENAI_API_KEY"))

print("=" * 70)
print("🧪 AI Email Agent - Quick Test")
print("=" * 70)

if not has_anthropic and not has_openai:
    print("\n❌ No AI API key found!")
    print("\nTo use the AI Email Agent, you need an API key:")
    print("\n📝 Option 1: Anthropic Claude (Recommended)")
    print("   1. Get key: https://console.anthropic.com/")
    print("   2. Add to .env: ANTHROPIC_API_KEY=your-key-here")
    print("   3. Run: python ai_email_agent.py")
    print("\n📝 Option 2: OpenAI GPT-4")
    print("   1. Get key: https://platform.openai.com/api-keys")
    print("   2. Add to .env: OPENAI_API_KEY=your-key-here")
    print("   3. Run: python ai_email_agent_openai.py")
    print("\n" + "=" * 70)
    exit(1)

if has_anthropic:
    print("\n✅ Anthropic API key found!")
    print("\nTesting AI Email Agent with Claude...\n")
    
    from ai_email_agent import AIEmailAgent
    
    agent = AIEmailAgent()
    
    # Test query
    test_query = "Send a test thank you email to test@example.com for attending Lecture 1 on AI Agents"
    
    print(f"Test Query: {test_query}\n")
    print("-" * 70)
    
    response = agent.process_request(test_query)
    
    print("-" * 70)
    print(f"\n✅ AI Agent Response:\n{response}\n")
    print("=" * 70)
    print("\n🎉 Success! The AI agent is working!")
    print("\nTo use interactively, run:")
    print("  python ai_email_agent.py")
    
elif has_openai:
    print("\n✅ OpenAI API key found!")
    print("\nTesting AI Email Agent with GPT-4...\n")
    
    from ai_email_agent_openai import AIEmailAgentOpenAI
    
    agent = AIEmailAgentOpenAI()
    
    # Test query
    test_query = "Send a test thank you email to test@example.com for attending Lecture 1 on AI Agents"
    
    print(f"Test Query: {test_query}\n")
    print("-" * 70)
    
    response = agent.process_request(test_query)
    
    print("-" * 70)
    print(f"\n✅ AI Agent Response:\n{response}\n")
    print("=" * 70)
    print("\n🎉 Success! The AI agent is working!")
    print("\nTo use interactively, run:")
    print("  python ai_email_agent_openai.py")
