from agno.agent import Agent, RunResponseEvent
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response
import os
import dotenv
from typing import Iterator
from utility.utils import shared_memory, shared_storage

dotenv.load_dotenv()

BOQ_AGENT_INSTRUCTIONS = [
    "Your Role and Goal: You are an expert Quantity Surveyor. Your goal is to translate project data into a structured Bill of Quantities (BoQ) for any type of building, following standard industry practices.",
    "Multi-Floor Plan Handling: If the project data includes multiple floor plans, generate a separate Bill of Quantities for each floor plan.",
    "Step 1: Initial Documentation Review - Thoroughly review all provided project data, including architectural drawings, specifications, and any other relevant documents. Identify key aspects such as building type (e.g., residential, commercial, industrial), scale (size, number of floors), rooms and their functions, and any special features or requirements (e.g., custom installations, unique structural elements).",
    "Step 2: Itemization and Categorization - Itemize all materials, labor, and tasks required for the project, ensuring every element of the construction process is covered, from site preparation to final finishes. Categorize them into standard construction categories, including but not limited to: Preliminaries (site preparation, temporary facilities, site management), Substructure (foundations, basement construction, ground works), Superstructure (structural frame, floors, roofs, columns), Exterior Finishes (external walls, windows, doors, cladding), Interior Finishes (internal walls, floors, ceilings, painting, tiling), Services (MEP) (mechanical, electrical, plumbing systems, e.g., HVAC, lighting, water supply), and Special Features (unique or custom elements specific to the project, e.g., green roofs, bespoke fittings). Ensure all items are comprehensively accounted for and correctly categorized.",
    "Step 3: Quantification - For each item, determine the appropriate Unit of Measurement (e.g., square meters for area, cubic meters for volume, linear meters for length, numbers for countable items). Estimate the Quantity based on the project data, using accurate measurement techniques derived from drawings, specifications, or other documents. Do not provide any cost estimates or include currency symbols; focus solely on quantities.",
    "Step 4: Quality Control & Self-Correction - Reread the initial project data and compare it against the generated BoQ. Check for completeness (all items and requirements from the data are included), accuracy (quantities and units are correctly calculated and assigned), and consistency (categories and items align with the project scope). Ensure there are no omissions or duplications, and adjust as necessary.",
    "Step 5: Final Compilation - Organize each Bill of Quantities in a clear and structured manner. For projects with multiple floor plans, ensure each BoQ corresponds to its respective floor plan. Each BoQ should include categories with their names (e.g., 'Substructure', 'Services (MEP)'), and items within each category, including description (e.g., 'Concrete foundation slab'), quantity (e.g., '150'), and unit of measurement (e.g., 'cubic meters')."
]

class BOQAgent(Agent):
    def __init__(self):
        super().__init__(
            name="BOQAgent",
            agent_id="boq_agent",
            model=Gemini(id=os.getenv("GEMINI_MODEL")),
            memory=shared_memory(),
            storage=shared_storage(),
            description="Interview agent interacts with clients to gather detailed architectural design requirements, including building type, number of floors, layout preferences, and MEP needs. It serves as the first step in guiding the design-to-BOQ process.",
            instructions=BOQ_AGENT_INSTRUCTIONS,
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
            expected_output = """"
                "📋 Bill of Quantities – FLOOR PLAN 1",
                "Project Type: Residential",
                "Floor: Ground Floor",
                "",

                "🛠️ Preliminaries",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Site clearance and grading           | 1        | job",
                "Temporary fencing and signage        | 45       | linear meters",
                "Site office setup                    | 1        | number",
                "",

                "🏗️ Substructure",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Excavation for footings              | 120      | cubic meters",
                "Concrete foundation slab (C25)       | 95       | cubic meters",
                "Damp-proof membrane installation     | 150      | square meters",
                "",

                "🧱 Superstructure",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "RCC columns (200x200 mm)             | 20       | number",
                "First floor slab (reinforced)        | 150      | square meters",
                "Brickwork – 230 mm external wall     | 180      | square meters",
                "",

                "🪟 Exterior Finishes",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Plastering – external                | 250      | square meters",
                "UPVC windows – 1.2x1.5 m             | 8        | number",
                "Main entrance door – wood            | 1        | number",
                "",

                "🛋️ Interior Finishes",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Internal plastering                  | 350      | square meters",
                "Ceramic floor tiling (600x600)       | 180      | square meters",
                "Ceiling gypsum board (drywall)       | 160      | square meters",
                "",

                "🔌 Services (MEP)",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Electrical conduit piping            | 200      | linear meters",
                "Light points with wiring             | 25       | number",
                "Water supply – PPR pipes             | 120      | linear meters",
                "WC units (toilets)                   | 2        | number",
                "",

                "🌿 Special Features",
                "Description                          | Quantity | Unit",
                "------------------------------------|----------|------------------",
                "Green roof prep layer                | 100      | square meters",
                "Skylight dome – 1.5 m radius         | 1        | number",
                "",

                "✅ All quantities are based on the available design data. No cost values are included."
            """


            )
    
    def generate_boq(self, data, user_id: str = None, session_id: str = None) -> Iterator[RunResponseEvent]:
        # Placeholder for interview logic
        print(f"[DEBUG]: Conducting interview with data: {data}")

        response: Iterator[RunResponseEvent] = self.run(data,
                                                        user_id=user_id,
                                                        session_id=session_id,
                                                        stream=True)
        # Here you would implement the actual interview logic, e.g., using conversation prompts
        pprint_run_response(response, markdown=True)
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    agent = BOQAgent()
    
    while True:
        text = input("Enter text for the agent (or type 'exit' to quit): ")
        if text.lower() == 'exit':
            break
    # Assuming the image is a valid path, you would pass it to the agent's interview method
        agent.generate_boq(text)
