import os
import json
import psycopg2
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
DB_URL = os.getenv("DATABASE_URL")

class SimplePostgresCheckpointer:
    """Minimal PostgreSQL checkpointer for conversation storage."""
    
    def __init__(self, db_url):
        self.db_url = db_url
    
    def get_next_version(self, current, channel):
        return (current or 0) + 1
    
    def put(self, config, checkpoint, metadata, new_versions):
        thread_id = config['configurable']['thread_id']
        checkpoint_id = str(hash(str(checkpoint)))
        
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO checkpoints (thread_id, checkpoint_ns, checkpoint_id, checkpoint, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (thread_id, checkpoint_ns, checkpoint_id) 
                DO UPDATE SET checkpoint = EXCLUDED.checkpoint
            ''', (thread_id, '', checkpoint_id, json.dumps(checkpoint, default=str), json.dumps(metadata)))
            conn.commit()
        finally:
            conn.close()
        
        return {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}
    
    def get_tuple(self, config):
        return None  # Simplified - not needed for basic storage
    
    def list(self, config, **kwargs):
        return []  # Simplified - not needed for basic storage
    
    def put_writes(self, config, writes, task_id):
        pass  # Simplified - not needed for basic storage

def create_checkpointer():
    """Create and return a properly configured checkpointer."""
    if not DB_URL:
        print("Warning: DATABASE_URL not set, using MemorySaver instead")
        return MemorySaver()
    
    try:
        print("✓ PostgreSQL checkpointer created successfully!")
        return SimplePostgresCheckpointer(DB_URL)
    except Exception as e:
        print(f"Error creating PostgreSQL checkpointer: {e}")
        print("Using MemorySaver as fallback...")
        return MemorySaver()

# Create the checkpointer
memory_saver = create_checkpointer()

