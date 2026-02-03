#!/usr/bin/env python3
"""
Simple CLI for the Email Agent.
"""
import argparse
import json
import sys
from email_agent import EmailAgent
from email_agent_sendgrid import SendGridEmailAgent


def main():
    parser = argparse.ArgumentParser(
        description="Send thank you emails to lecture attendees"
    )
    
    parser.add_argument(
        "--email",
        required=True,
        help="Recipient email address"
    )
    
    parser.add_argument(
        "--name",
        default="Student",
        help="Recipient name (default: Student)"
    )
    
    parser.add_argument(
        "--topic",
        help="Lecture topic"
    )
    
    parser.add_argument(
        "--message",
        help="Custom message to include"
    )
    
    parser.add_argument(
        "--link",
        help="Link to lecture materials"
    )
    
    parser.add_argument(
        "--cc",
        help="Email address to CC"
    )
    
    parser.add_argument(
        "--provider",
        choices=["smtp", "sendgrid"],
        default="smtp",
        help="Email provider to use (default: smtp)"
    )
    
    args = parser.parse_args()
    
    # Initialize the appropriate agent
    try:
        if args.provider == "sendgrid":
            agent = SendGridEmailAgent()
        else:
            agent = EmailAgent()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease check your .env file configuration.")
        sys.exit(1)
    
    # Send the email
    print(f"📧 Sending thank you email to {args.email}...")
    
    result = agent.send_thank_you_email(
        recipient_email=args.email,
        recipient_name=args.name,
        lecture_topic=args.topic,
        custom_message=args.message,
        lecture_link=args.link,
        cc_email=args.cc
    )
    
    # Display result
    if result["status"] == "success":
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
