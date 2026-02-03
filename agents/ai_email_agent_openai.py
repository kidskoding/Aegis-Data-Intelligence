"""
AI-powered Email Agent that uses OpenAI GPT to understand requests and send emails.
"""
import os
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from email_agent import EmailAgent
import openai

# Load environment variables
load_dotenv()


class AIEmailAgentOpenAI:
    """An AI agent that uses OpenAI GPT to understand requests and send emails."""
    
    def __init__(self):
        self.email_agent = EmailAgent()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing OpenAI API key. Please set OPENAI_API_KEY in .env file"
            )
        self.client = openai.OpenAI(api_key=api_key)
        
        # Define the email tools for OpenAI
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send a thank you email to lecture attendees. Use this when the user asks to send emails, thank students, or contact attendees.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient_email": {
                                "type": "string",
                                "description": "The recipient's email address"
                            },
                            "recipient_name": {
                                "type": "string",
                                "description": "The recipient's name (default: 'Student')"
                            },
                            "lecture_topic": {
                                "type": "string",
                                "description": "The topic of the lecture"
                            },
                            "custom_message": {
                                "type": "string",
                                "description": "Additional custom message to include in the email"
                            },
                            "lecture_link": {
                                "type": "string",
                                "description": "Link to lecture materials (slides, code, etc.)"
                            },
                            "cc_email": {
                                "type": "string",
                                "description": "Email address to CC"
                            }
                        },
                        "required": ["recipient_email"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_bulk_emails",
                    "description": "Send thank you emails to multiple lecture attendees at once. Use this when the user provides multiple recipients.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipients": {
                                "type": "array",
                                "description": "List of recipient objects",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string"},
                                        "name": {"type": "string"},
                                        "lecture_topic": {"type": "string"},
                                        "custom_message": {"type": "string"},
                                        "lecture_link": {"type": "string"},
                                        "cc_email": {"type": "string"}
                                    },
                                    "required": ["email"]
                                }
                            }
                        },
                        "required": ["recipients"]
                    }
                }
            }
        ]
    
    def _send_email_tool(self, **kwargs) -> Dict[str, Any]:
        """Execute the send_email tool."""
        return self.email_agent.send_thank_you_email(**kwargs)
    
    def _send_bulk_emails_tool(self, recipients: List[Dict]) -> Dict[str, Any]:
        """Execute the send_bulk_emails tool."""
        return self.email_agent.send_bulk_thank_you_emails(recipients)
    
    def process_request(self, user_query: str) -> str:
        """
        Process a natural language request and send emails accordingly.
        
        Args:
            user_query: Natural language request from the user
            
        Returns:
            str: Response from the AI agent
        """
        print(f"\n🤖 AI Agent processing your request...\n")
        
        # System prompt to guide the AI
        system_prompt = """You are an AI email assistant for AgenticAI@UIUC lectures. Your job is to:
1. Understand natural language requests about sending thank you emails to lecture attendees
2. Extract relevant information (recipients, lecture topics, materials links, etc.)
3. Use the email tools to send professional thank you emails
4. Default CC to ashleyn4@illinois.edu unless specified otherwise
5. Default lecture link to https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01 unless specified otherwise
6. Be friendly and professional in your responses

When users mention sending emails, always use the appropriate tool to actually send them."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # Initial API call
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Process tool calls
        while response_message.tool_calls:
            messages.append(response_message)
            
            # Execute tools
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Using tool: {function_name}")
                print(f"📋 Input: {json.dumps(function_args, indent=2)}\n")
                
                # Execute the appropriate tool
                if function_name == "send_email":
                    result = self._send_email_tool(**function_args)
                elif function_name == "send_bulk_emails":
                    result = self._send_bulk_emails_tool(**function_args)
                else:
                    result = {"error": f"Unknown tool: {function_name}"}
                
                print(f"✅ Tool result: {json.dumps(result, indent=2)}\n")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Continue the conversation
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            response_message = response.choices[0].message
        
        return response_message.content


def main():
    """Interactive AI Email Agent."""
    print("=" * 70)
    print("🤖 AI Email Agent for AgenticAI@UIUC (OpenAI)")
    print("=" * 70)
    print("\nI can understand natural language requests and send emails for you!")
    print("\nExamples:")
    print('  - "Send a thank you email to john@example.com for attending lecture 1"')
    print('  - "Email these students: alice@test.com, bob@test.com about AI Agents"')
    print('  - "Thank everyone who came to today\'s lecture"')
    print("\nType 'quit' to exit\n")
    
    try:
        agent = AIEmailAgentOpenAI()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have OPENAI_API_KEY in your .env file.")
        print("Get your API key from: https://platform.openai.com/api-keys")
        return
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent.process_request(user_input)
            print(f"\n🤖 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
