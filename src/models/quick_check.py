"""
Quick Conversation Checker
A simple script to quickly check the latest conversation or a specific thread ID.
"""

import os
import sys
from dotenv import load_dotenv
from inspect_conversations import ConversationInspector

load_dotenv()


def quick_check(thread_id=None):
    """Quick check for the latest conversation or a specific thread."""
    try:
        inspector = ConversationInspector()
        
        if thread_id:
            print(f"🔍 Checking conversation: {thread_id}")
            inspector.display_conversation(thread_id)
        else:
            print("🔍 Finding latest conversations...")
            threads = inspector.list_all_threads()
            
            if threads:
                print(f"\n📋 Displaying latest conversation: {threads[0]}")
                inspector.display_conversation(threads[0])
            else:
                print("❌ No conversations found in database.")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if a thread ID was provided as command line argument
    thread_id = sys.argv[1] if len(sys.argv) > 1 else None
    quick_check(thread_id)
