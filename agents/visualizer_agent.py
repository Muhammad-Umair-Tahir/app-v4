from agno.agent import Agent, RunResponseEvent
from agno.models.google import Gemini
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.media import Image
from agno.utils.pprint import pprint_run_response
import os
import dotenv
from typing import Iterator
from utility.utils import shared_memory, shared_storage

dotenv.load_dotenv()


class VisualizerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VisualizerAgent",
            agent_id="visualizer_agent",
            model=Gemini(id=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")),
            memory=shared_memory(),
            storage=shared_storage(),
            description="This agent visualizes data and generates images based on the provided information.",
            instructions="""Use this agent to visualize data and generate images. It can process various types of data and create analysis of visual representations.
            You have to go in depth and analyze every part of the image every pixel in detail and return your result as expected output
            """,
            # user_id="user_123",
            # session_id="session_123",
            # CHAT HISTORY CONFIG
            add_history_to_messages=True,
            num_history_runs= 5,
            read_chat_history= True,
            
            # MEMORY CONFIG
            enable_agentic_memory=True,
            enable_user_memories=True,
            enable_session_summaries= True,
            
            debug_mode=True,
            expected_output = """  
            🧾 Floor Plan Summary

            This is a commercial/residential floor plan for a single-level office space, designed for efficient workflow and accessibility. The image includes well-defined areas such as a large open workspace, a reception zone, and meeting utilities. The layout promotes natural movement and collaborative design.

            - 🏢 Type: Commercial/Residential
            - 📐 Total Area: 3,600 sqft
            - 🧭 Orientation: North-facing

            🔍 Room Breakdown:

            1. **Reception (300 sqft)**
            - Reception desk
            - Waiting chairs
            - Glass partition

            2. **Open Workspace (1,800 sqft)**
            - 12 Work desks
            - 20 Chairs
            - Storage cabinets

            3. **Meeting Room (400 sqft)**
            - Conference table
            - 8 Chairs
            - Whiteboard
            - TV screen

            4. **Pantry (150 sqft)**
            - Sink, Microwave, Fridge
            - Dining table

            5. **Restroom (150 sqft)**
            - 2 Toilets
            - 2 Sinks
            - Mirror
            6. **Utility Room (100 sqft)**
            - Storage for cleaning supplies
            """
            )
    
    def visualize(self, text: str = None, file_path: str = None, user_id: str = None, session_id: str = None) -> Iterator[RunResponseEvent]:
        # Placeholder for visualization logic
        print(f"[DEBUG]: Visualizing data - text: {text}, file_path: {file_path}")

        if file_path:
            # If file path is provided, read the file and create Image from path
            print(f"[DEBUG]: Using file path: {file_path}")
            return self.run("Analyze the provided image file in depth and return your analysis as instructed", 
                           images=[Image(filepath=file_path)], user_id=user_id, session_id=session_id, detail="auto", stream=True)
            
    
    
    
    
    
    
    
if __name__ == "__main__":
    agent = VisualizerAgent()
    image=r"D:\Agno\New folder\WhatsApp Image 2025-06-24 at 21.15.51_32265026.jpg"
    agent.visualize(image)
    
        