from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
# from routers.agent_router import viab_router
from agents.visualizer_agent import VisualizerAgent
from agents.interview_agent import InterviewAgent
from agents.boq_agent import BOQAgent
from agno.team.team import Team
from fastapi import File, UploadFile, Form, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from typing import List
import os
import base64
from datetime import datetime
import uuid
import shutil



VisualizerAgent = VisualizerAgent()
InterviewAgent = InterviewAgent()
BOQAgent = BOQAgent()

# viab_team = Team(
#     name="VIAB Team",
#     team_id="viab_team_123",
#     description="A team of specialized agents for visualization, interviews, and BOQ generation.",
#     members=[VisualizerAgent, InterviewAgent, BOQAgent],
#     mode="route"
# )

# Create FastAPI app
fastapi_app = FastAPIApp(
    # teams=[viab_team],
    agents=[VisualizerAgent, InterviewAgent, BOQAgent],
    name="VIAB",
    app_id="viab_123",
    description="VIAB is a versatile agent system designed to handle various tasks including visualization, interviews, and bill of quantities (BOQ) generation. It integrates multiple agents to provide comprehensive solutions.",
)

app = fastapi_app.get_app()

# Custom endpoint to analyze uploaded images
@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    message: str = Form("Analyze the uploaded image"),
    user_id: str = Form("default_user"),
    session_id: str = Form("")
):
    """
    Custom endpoint to receive image uploads, save them to user-specific folders,
    and pass them to the visualizer agent for analysis.
    """
    try:
        # Create user-specific upload directory
        user_upload_dir = f"uploads/{user_id}"
        os.makedirs(user_upload_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(user_upload_dir, unique_filename)
        
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        print(f"[DEBUG] File saved: {file_path} ({file_size} bytes)")
        
        # Pass the file to the visualizer agent
        analysis_result = ""
        try:
            # Use the visualizer agent's visualize method
            response_generator = VisualizerAgent.visualize(
                text=message,
                file_path=file_path,
                user_id=user_id,
                session_id=session_id
            )
            
            # Collect the response from the generator
            for event in response_generator:
                if hasattr(event, 'content') and event.content:
                    analysis_result += event.content
                elif hasattr(event, 'delta') and event.delta:
                    analysis_result += event.delta
        
        except Exception as agent_error:
            print(f"[ERROR] Agent analysis failed: {agent_error}")
            analysis_result = f"Analysis failed: {str(agent_error)}"
        
        # Return response with file info and analysis
        return JSONResponse(content={
            "status": "success",
            "message": "Image uploaded and analyzed successfully",
            "file_info": {
                "original_name": file.filename,
                "saved_path": file_path,
                "size_bytes": file_size,
                "content_type": file.content_type
            },
            "analysis": analysis_result,
            "user_id": user_id,
            "session_id": session_id
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
