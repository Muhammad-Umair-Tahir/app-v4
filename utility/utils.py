import os
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.models.google import Gemini
import uuid
import json
from agno.workflow import WorkflowRunResponseEvent
from typing import Iterator

def shared_memory():
    
    memory = Memory(db=SqliteMemoryDb( table_name="shared_memories", db_file=os.getenv("MEMORY_DB_FILE")), model=Gemini(os.getenv("GOOGLE_MODEL")))
    return memory

def shared_storage():
    return SqliteStorage(table_name="shared_storage", db_file=os.getenv("STORAGE_DB_FILE"))

def generate_user_id():
    """
    Generates a shorter ID using only the first 8 characters of UUID4.
    """
    return str(uuid.uuid4())[:8]

def generate_session_id():
    """
    Generates a unique session ID based on the current environment variable.
    """
    return str(uuid.uuid4())[:8]


def get_current_user():
    return generate_user_id()

def get_current_session():
    return generate_session_id()





def stream_text_response(events: Iterator[WorkflowRunResponseEvent]) -> Iterator[str]:
    """
    Stream the raw content of RunResponseEvent exactly as the terminal version would show it.
    """
    for event in events:
        if hasattr(event, "content") and isinstance(event.content, str):
            yield event.content  # no extra newline
