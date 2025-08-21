import os
import json
import psycopg2
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import CheckpointTuple
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage

# Load environment variables
DB_URL = os.getenv("DATABASE_URL")

class SimplePostgresCheckpointer:
    """PostgreSQL checkpointer for conversation storage with proper history retrieval."""
    
    def __init__(self, db_url):
        self.db_url = db_url
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the checkpoints table exists."""
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT NOT NULL,
                    checkpoint_ns TEXT NOT NULL DEFAULT '',
                    checkpoint_id TEXT NOT NULL,
                    checkpoint JSONB NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
                )
            ''')
            conn.commit()
        finally:
            conn.close()
    
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
                DO UPDATE SET checkpoint = EXCLUDED.checkpoint, metadata = EXCLUDED.metadata
            ''', (thread_id, '', checkpoint_id, json.dumps(checkpoint, default=str), json.dumps(metadata)))
            conn.commit()
        finally:
            conn.close()
        
        return {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}
    
    def get_tuple(self, config):
        """Retrieve the latest checkpoint for a thread."""
        thread_id = config['configurable']['thread_id']
        
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT checkpoint_id, checkpoint, metadata FROM checkpoints 
                WHERE thread_id = %s AND checkpoint_ns = %s
                ORDER BY created_at DESC LIMIT 1
            ''', (thread_id, ''))
            
            result = cursor.fetchone()
            if result:
                checkpoint_id, checkpoint_data, metadata = result
                
                # Handle both JSON string and dict cases
                if isinstance(checkpoint_data, str):
                    checkpoint = json.loads(checkpoint_data)
                else:
                    checkpoint = checkpoint_data  # Already a dict from JSONB
                
                # Handle metadata similarly
                if isinstance(metadata, str):
                    metadata_dict = json.loads(metadata) if metadata else {}
                else:
                    metadata_dict = metadata if metadata else {}
                
                # Return a proper CheckpointTuple
                return CheckpointTuple(
                    config={"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}},
                    checkpoint=checkpoint,
                    metadata=metadata_dict,
                    parent_config=None,
                    pending_writes=None
                )
            return None
        finally:
            conn.close()
    
    def list(self, config, **kwargs):
        """List checkpoints for a thread."""
        thread_id = config['configurable']['thread_id']
        
        conn = psycopg2.connect(self.db_url)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT checkpoint_id, checkpoint, metadata FROM checkpoints 
                WHERE thread_id = %s AND checkpoint_ns = %s
                ORDER BY created_at DESC
            ''', (thread_id, ''))
            
            results = []
            for row in cursor.fetchall():
                checkpoint_id, checkpoint_data, metadata = row
                
                # Handle both JSON string and dict cases
                if isinstance(checkpoint_data, str):
                    checkpoint = json.loads(checkpoint_data)
                else:
                    checkpoint = checkpoint_data  # Already a dict from JSONB
                
                # Handle metadata similarly
                if isinstance(metadata, str):
                    metadata_dict = json.loads(metadata) if metadata else {}
                else:
                    metadata_dict = metadata if metadata else {}
                
                # Return proper CheckpointTuple objects
                results.append(CheckpointTuple(
                    config={"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}},
                    checkpoint=checkpoint,
                    metadata=metadata_dict,
                    parent_config=None,
                    pending_writes=None
                ))
            return results
        finally:
            conn.close()
    
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