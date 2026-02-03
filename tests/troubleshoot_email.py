#!/usr/bin/env python3
"""
Email troubleshooting script
"""
from email_agent import EmailAgent
import sys

print("=" * 70)
print("🔍 EMAIL TROUBLESHOOTING")
print("=" * 70)

# Get recipient email
if len(sys.argv) > 1:
    recipient = sys.argv[1]
else:
    recipient = input("\nEnter your email address to test: ").strip()

if not recipient:
    print("❌ No email address provided")
    sys.exit(1)

print(f"\n📧 Sending test email to: {recipient}")
print("-" * 70)

try:
    agent = EmailAgent()
    
    print(f"\n✅ Configuration:")
    print(f"   SMTP Server: {agent.smtp_server}:{agent.smtp_port}")
    print(f"   Sender: {agent.sender_email}")
    print(f"   Recipient: {recipient}")
    
    print(f"\n📤 Sending email...")
    
    result = agent.send_thank_you_email(
        recipient_email=recipient,
        recipient_name="Test User",
        lecture_topic="Email System Test",
        lecture_link="https://github.com/AgenticAI-UIUC/Spring26/tree/main/Lecture-01",
        custom_message="If you received this email, the system is working! Check spam/junk if you don't see it in your inbox."
    )
    
    print(f"\n{'='*70}")
    if result['status'] == 'success':
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print("="*70)
        print("\n📋 What to check:")
        print("   1. ✉️  Check your INBOX")
        print("   2. 📁 Check SPAM/JUNK folder")
        print("   3. 🔍 Search for 'agenticaiuiuc@gmail.com'")
        print("   4. ⏰ Wait 1-2 minutes for delivery")
        print("   5. 🚫 Check if your email blocks external senders")
        print("\n💡 Common Issues:")
        print("   • University email systems may have delays")
        print("   • First email from new sender often goes to spam")
        print("   • Gmail: Check 'Promotions' or 'Social' tabs")
        print("   • Outlook: Check 'Other' or 'Junk' folders")
        print("\n🔧 If still not receiving:")
        print("   • Try a different email address (Gmail, Outlook)")
        print("   • Add agenticaiuiuc@gmail.com to contacts")
        print("   • Check email filtering rules")
        print(f"\n{'='*70}")
    else:
        print(f"❌ SEND FAILED: {result['message']}")
        print("="*70)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
