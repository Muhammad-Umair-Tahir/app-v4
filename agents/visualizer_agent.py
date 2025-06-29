from agno.agent import Agent, RunResponseEvent
from agno.models.google import Gemini
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.media import Image
from agno.utils.pprint import pprint_run_response
import os
import dotenv
from typing import Iterator
import asyncio
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
            
            # CHAT HISTORY CONFIG
            add_history_to_messages=True,            
            # MEMORY CONFIG
            enable_user_memories=True,
                        
            debug_mode=True,
            expected_output="""  
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
        """
        Visualize and analyze image data based on provided text or file path.
        
        Args:
            text: Text description or analysis request
            file_path: Path to the image file to analyze
            user_id: User identifier for session management
            session_id: Session identifier for conversation continuity
            
        Returns:
            Iterator[RunResponseEvent]: Streaming response events with analysis results
        """
        print(f"[DEBUG]: Visualizing data - text: {text}, file_path: {file_path}")

        try:
            if file_path:
                # If file path is provided, analyze the image file
                print(f"[DEBUG]: Using file path: {file_path}")
                
                # Check if file exists
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Image file not found: {file_path}")
                
                # Create analysis prompt
                analysis_prompt = text or "Analyze the provided image file in depth and return your analysis as instructed"
                
                # Run analysis with image
                response: Iterator[RunResponseEvent] = self.run(
                    analysis_prompt, 
                    images=[Image(filepath=file_path)], 
                    user_id=user_id, 
                    session_id=session_id, 
                    stream=True
                )
                
                return response
                
            elif text:
                # If only text is provided, process text-based visualization request
                print(f"[DEBUG]: Processing text-based request: {text}")
                
                response: Iterator[RunResponseEvent] = self.run(
                    text,
                    user_id=user_id,
                    session_id=session_id,
                    stream=True
                )
                
                return response
                
            else:
                raise ValueError("Either text or file_path must be provided")
                
        except Exception as e:
            print(f"[ERROR] Visualization failed: {e}")
            raise e

def main():
    """Main function for testing the Visualizer agent."""
    agent = VisualizerAgent()
    
    print("🎨 Visualizer Agent - Test Mode")
    print("Options:")
    print("1. Enter text for analysis")
    print("2. Provide image file path")
    print("3. Type 'exit' to quit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("Enter your request or image path: ")
            
            if user_input.lower() == 'exit':
                print("Thank you for using the Visualizer Agent. Goodbye!")
                break
            
            if not user_input.strip():
                print("Please enter some text or an image path.")
                continue
            
            # Check if input is a file path
            if os.path.exists(user_input) and os.path.isfile(user_input):
                # Input is a file path
                print(f"\n🖼️ Analyzing image: {user_input}")
                print("-" * 40)
                
                response_generator = agent.visualize(file_path=user_input)
                
            else:
                # Input is text
                print(f"\n📝 Processing text request...")
                print("-" * 40)
                
                response_generator = agent.visualize(text=user_input)
            
            # Process streaming response using pprint_run_response
            pprint_run_response(response_generator, markdown=True)
            
            print("\n" + "-" * 40)
            print("✅ Analysis completed!")
            print()
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with different input.\n")

if __name__ == "__main__":
    main()