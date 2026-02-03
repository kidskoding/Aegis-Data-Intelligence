#!/usr/bin/env python3
"""
Bulk send thank you emails from a CSV or JSON file.
"""
import argparse
import json
import csv
import sys
from email_agent import EmailAgent
from email_agent_sendgrid import SendGridEmailAgent


def load_recipients_from_csv(filepath: str) -> list[dict]:
    """Load recipients from a CSV file."""
    recipients = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients.append({
                "email": row["email"],
                "name": row.get("name", "Student"),
                "lecture_topic": row.get("lecture_topic"),
                "custom_message": row.get("custom_message")
            })
    return recipients


def load_recipients_from_json(filepath: str) -> list[dict]:
    """Load recipients from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Bulk send thank you emails to lecture attendees"
    )
    
    parser.add_argument(
        "--file",
        required=True,
        help="Path to CSV or JSON file with recipient data"
    )
    
    parser.add_argument(
        "--provider",
        choices=["smtp", "sendgrid"],
        default="smtp",
        help="Email provider to use (default: smtp)"
    )
    
    args = parser.parse_args()
    
    # Load recipients
    try:
        if args.file.endswith('.csv'):
            recipients = load_recipients_from_csv(args.file)
        elif args.file.endswith('.json'):
            recipients = load_recipients_from_json(args.file)
        else:
            print("❌ Error: File must be .csv or .json")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    
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
    
    # Send bulk emails
    print(f"📧 Sending thank you emails to {len(recipients)} recipients...")
    
    result = agent.send_bulk_thank_you_emails(recipients)
    
    # Display summary
    print("\n" + "="*50)
    print(f"✅ Successfully sent: {result['successful']}")
    print(f"❌ Failed: {result['failed']}")
    print(f"📊 Total: {result['total']}")
    print("="*50)
    
    # Show details for failed emails
    if result['failed'] > 0:
        print("\nFailed emails:")
        for detail in result['details']:
            if detail['status'] == 'error':
                print(f"  - {detail['recipient']}: {detail['message']}")


if __name__ == "__main__":
    main()
