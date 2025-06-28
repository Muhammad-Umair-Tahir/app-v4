import os
from agno.memory.v2 import Memory
from agno.memory.v2.db.mongodb import MongoMemoryDb
from agno.storage.mongodb import MongoDbStorage
from agno.models.google import Gemini
import uuid
import json
from agno.workflow import WorkflowRunResponseEvent
from typing import Iterator
import dotenv

dotenv.load_dotenv()

def shared_memory():
    
    memory = Memory(db=MongoMemoryDb( collection_name="shared_memories", db_url=os.getenv("MONGO_URI", "mongodb+srv://htahir861:DevF4e28db5%40@devcluster.zou3amg.mongodb.net/?retryWrites=true&w=majority&appName=DevCluster"), db_name="agno"), model=Gemini(os.getenv("GEMINI_MODEL", "gemini-2.5-flash")),)
    return memory

def shared_storage():
    return MongoDbStorage(collection_name="shared_storage", db_url=os.getenv("MONGO_URI", "mongodb+srv://htahir861:DevF4e28db5%40@devcluster.zou3amg.mongodb.net/?retryWrites=true&w=majority&appName=DevCluster"), db_name="agno")

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
