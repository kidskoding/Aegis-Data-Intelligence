"""
AI Email Agent using ReAct (Reasoning + Acting) pattern with OpenAI.
The agent reasons about what to do, then acts with tools.
"""
import os
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from email_agent import EmailAgent
import openai

# Load environment variables
load_dotenv()


class ReActEmailAgentOpenAI:
    """An AI agent that uses ReAct pattern with OpenAI: Reason, then Act."""
    
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
                    "description": "Send a thank you email to a single lecture attendee. Use this when you need to send one email.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient_email": {
                                "type": "string",
                                "description": "The recipient's email address"
                            },
                            "recipient_name": {
                                "type": "string",
                                "description": "The recipient's name"
                            },
                            "lecture_topic": {
                                "type": "string",
                                "description": "The topic of the lecture"
                            },
                            "custom_message": {
                                "type": "string",
                                "description": "Additional custom message to include"
                            },
                            "lecture_link": {
                                "type": "string",
                                "description": "Link to lecture materials"
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
                    "description": "Send thank you emails to multiple lecture attendees at once. More efficient than sending one by one.",
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
    
    def process_request(self, user_query: str, verbose: bool = True) -> str:
        """
        Process a natural language request using ReAct pattern.
        
        Args:
            user_query: Natural language request from the user
            verbose: Whether to print reasoning steps
            
        Returns:
            str: Response from the AI agent
        """
        if verbose:
            print(f"\n{'='*70}")
            print("🧠 ReAct AI Email Agent (OpenAI)")
            print(f"{'='*70}\n")
            print(f"📝 Your Request: {user_query}\n")
            print(f"{'='*70}\n")
        
        # ReAct system prompt - encourages reasoning before acting
        system_prompt = """You are an AI email assistant for AgenticAI@UIUC lectures using the ReAct (Reasoning + Acting) framework.

IMPORTANT: Use this exact format for EVERY response:

Thought: [Your reasoning about what needs to be done]
Action: [The action you will take - either use a tool or provide final answer]
Observation: [What you learned from the action]

When solving a task:
1. Start with "Thought:" - analyze the request and plan your approach
2. Then "Action:" - either use a tool or give your final answer
3. After tool results, provide "Observation:" - reflect on what happened
4. Repeat Thought → Action → Observation until the task is complete

Context and defaults:
- Default CC: ashleyn4@illinois.edu
- Default lecture link: https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01
- Default lecture topic: "Introduction to AI Agents" (unless specified)
- Be professional and friendly

Example flow:
Thought: The user wants to send an email to john@test.com. I need to extract the recipient details and determine if it's a single email or multiple emails.
Action: I will use the send_email tool with the recipient information.
Observation: [After tool execution] The email was sent successfully to john@test.com.
Thought: The task is complete. I should inform the user.
Action: Final Answer: I've successfully sent a thank you email to john@test.com for attending the lecture!

Always show your reasoning process."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        iteration = 0
        max_iterations = 10
        
        while iteration < max_iterations:
            iteration += 1
            
            if verbose:
                print(f"🔄 Iteration {iteration}")
                print("-" * 70)
            
            # API call
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.1
            )
            
            response_message = response.choices[0].message
            
            # Display reasoning text
            if response_message.content:
                if verbose:
                    print(f"\n{response_message.content}\n")
            
            # If no tools are called, we're done
            if not response_message.tool_calls:
                if verbose:
                    print("=" * 70)
                    print("✅ Task Complete!")
                    print("=" * 70 + "\n")
                return response_message.content or ""
            
            # Add assistant's response to messages
            messages.append(response_message)
            
            # Process tool calls
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if verbose:
                    print(f"🔧 Action: Using tool '{function_name}'")
                    print(f"📋 Parameters:")
                    print(f"{json.dumps(function_args, indent=2)}\n")
                
                # Execute the tool
                if function_name == "send_email":
                    result = self._send_email_tool(**function_args)
                elif function_name == "send_bulk_emails":
                    result = self._send_bulk_emails_tool(**function_args)
                else:
                    result = {"error": f"Unknown tool: {function_name}"}
                
                if verbose:
                    if result.get("status") == "success":
                        print(f"✅ Result: {result.get('message', 'Success')}\n")
                    else:
                        print(f"❌ Result: {result.get('message', 'Failed')}\n")
                    print("-" * 70)
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        
        # If we hit max iterations
        return "Task completed after maximum iterations."


def main():
    """Interactive ReAct Email Agent with OpenAI."""
    print("=" * 70)
    print("🧠 ReAct AI Email Agent for AgenticAI@UIUC (OpenAI)")
    print("=" * 70)
    print("\nI use ReAct (Reasoning + Acting) to show my thought process!")
    print("Watch me reason through each step before taking action.\n")
    print("Examples:")
    print('  - "Send a thank you email to john@example.com for lecture 1"')
    print('  - "Email alice@test.com and bob@test.com about AI Agents"')
    print('  - "Thank student@illinois.edu for attending"')
    print("\nType 'quit' to exit\n")
    
    try:
        agent = ReActEmailAgentOpenAI()
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
            
            response = agent.process_request(user_input, verbose=True)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
