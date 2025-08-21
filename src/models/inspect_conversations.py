"""
Conversation Inspector for PostgreSQL Database
This module allows you to view and inspect conversations stored in the PostgreSQL database.
"""

import os
import json
import psycopg2
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it

# Load environment variables
DB_URL = os.getenv("DATABASE_URL")

class ConversationInspector:
    """Inspector class to view conversations stored in PostgreSQL."""
    
    def __init__(self, db_url=None):
        self.db_url = db_url or DB_URL
        
        # If still no DB_URL, try to import from the connect_database module
        if not self.db_url:
            try:
                from connect_database import memory_saver
                if hasattr(memory_saver, 'db_url'):
                    self.db_url = memory_saver.db_url
                    print("✓ Using database connection from connect_database module")
                else:
                    print("❌ No database URL found. Please:")
                    print("   1. Set DATABASE_URL environment variable, or")
                    print("   2. Create a .env file with DATABASE_URL, or") 
                    print("   3. Ensure your database is properly configured")
                    return
            except Exception as e:
                print(f"❌ Could not connect to database: {e}")
                print("Please ensure:")
                print("   1. DATABASE_URL is set in environment variables")
                print("   2. PostgreSQL is running")
                print("   3. Database credentials are correct")
                return
        
        if not self.db_url:
            raise ValueError("DATABASE_URL not found. Please set it in your environment variables or .env file.")
    
    def list_all_threads(self):
        """List all conversation thread IDs in the database."""
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT thread_id, COUNT(*) as checkpoint_count, 
                       MIN(created_at) as first_message, MAX(created_at) as last_message
                FROM checkpoints 
                GROUP BY thread_id 
                ORDER BY last_message DESC
            ''')
            
            threads = cursor.fetchall()
            print("📋 Available Conversation Threads:")
            print("-" * 80)
            
            if not threads:
                print("No conversations found in the database.")
                return []
            
            for thread_id, count, first, last in threads:
                print(f"Thread ID: {thread_id}")
                print(f"  Checkpoints: {count}")
                print(f"  First message: {first}")
                print(f"  Last message: {last}")
                print("-" * 80)
            
            return [thread[0] for thread in threads]
        finally:
            conn.close()
    
    def get_conversation(self, thread_id):
        """Retrieve and display a specific conversation."""
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT checkpoint, created_at FROM checkpoints 
                WHERE thread_id = %s AND checkpoint_ns = ''
                ORDER BY created_at DESC LIMIT 1
            ''', (thread_id,))
            
            result = cursor.fetchone()
            if result:
                checkpoint_data, created_at = result
                
                # Handle both JSON string and dict cases
                if isinstance(checkpoint_data, str):
                    checkpoint = json.loads(checkpoint_data)
                else:
                    checkpoint = checkpoint_data  # Already a dict from JSONB
                
                return checkpoint, created_at
            return None, None
        finally:
            conn.close()
    
    def display_conversation(self, thread_id):
        """Display a conversation in a readable format."""
        checkpoint, created_at = self.get_conversation(thread_id)
        
        if not checkpoint:
            print(f"❌ No conversation found for thread ID: {thread_id}")
            return
        
        print(f"💬 Conversation: {thread_id}")
        print(f"📅 Last updated: {created_at}")
        print("=" * 80)
        
        # Extract messages from checkpoint
        if 'channel_values' in checkpoint and 'messages' in checkpoint['channel_values']:
            messages = checkpoint['channel_values']['messages']
        elif 'messages' in checkpoint:
            messages = checkpoint['messages']
        else:
            print("❌ No messages found in this conversation.")
            return
        
        # Display each message
        for i, message in enumerate(messages, 1):
            self._display_message(message, i)
        
        print("=" * 80)
        print(f"Total messages: {len(messages)}")
    
    def _display_message(self, message, index):
        """Display a single message in a readable format."""
        # Handle different message formats
        if isinstance(message, dict):
            msg_type = message.get('type', 'unknown')
            content = message.get('content', '')
            
            if msg_type == 'system':
                icon = "⚙️"
                sender = "SYSTEM"
            elif msg_type == 'human':
                icon = "👤"
                sender = "HUMAN"
            elif msg_type == 'ai':
                icon = "🤖"
                sender = "AI"
            else:
                icon = "❓"
                sender = msg_type.upper()
        else:
            # Handle LangChain message objects
            if hasattr(message, 'type'):
                msg_type = message.type
                content = getattr(message, 'content', str(message))
                
                if msg_type == 'system':
                    icon = "⚙️"
                    sender = "SYSTEM"
                elif msg_type == 'human':
                    icon = "👤"
                    sender = "HUMAN"
                elif msg_type == 'ai':
                    icon = "🤖"
                    sender = "AI"
                else:
                    icon = "❓"
                    sender = msg_type.upper()
            else:
                icon = "❓"
                sender = "UNKNOWN"
                content = str(message)
        
        print(f"{index}. {icon} {sender}:")
        # Truncate very long content for readability
        if len(content) > 500:
            print(f"   {content[:500]}...")
            print(f"   [Content truncated - {len(content)} total characters]")
        else:
            print(f"   {content}")
        print()
    
    def search_conversations(self, keyword):
        """Search for conversations containing a specific keyword."""
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT thread_id, checkpoint, created_at 
                FROM checkpoints 
                WHERE checkpoint::text ILIKE %s
                ORDER BY created_at DESC
            ''', (f'%{keyword}%',))
            
            results = cursor.fetchall()
            print(f"🔍 Search results for '{keyword}':")
            print("-" * 60)
            
            if not results:
                print("No conversations found containing that keyword.")
                return []
            
            found_threads = []
            for thread_id, checkpoint_data, created_at in results:
                print(f"Thread: {thread_id} (Last updated: {created_at})")
                found_threads.append(thread_id)
            
            return found_threads
        finally:
            conn.close()


def main():
    """Main function to demonstrate usage."""
    try:
        inspector = ConversationInspector()
        
        print("🔍 Conversation Database Inspector")
        print("=" * 50)
        
        while True:
            print("\nChoose an option:")
            print("1. List all conversation threads")
            print("2. View specific conversation")
            print("3. Search conversations by keyword")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                inspector.list_all_threads()
            
            elif choice == "2":
                thread_id = input("Enter thread ID to view: ").strip()
                if thread_id:
                    inspector.display_conversation(thread_id)
            
            elif choice == "3":
                keyword = input("Enter keyword to search for: ").strip()
                if keyword:
                    found_threads = inspector.search_conversations(keyword)
                    if found_threads:
                        view_choice = input("\nView a specific conversation? (y/n): ").strip().lower()
                        if view_choice == 'y':
                            thread_id = input("Enter thread ID to view: ").strip()
                            if thread_id in found_threads:
                                inspector.display_conversation(thread_id)
            
            elif choice == "4":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
