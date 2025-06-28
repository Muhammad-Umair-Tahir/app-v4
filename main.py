from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
# from routers.agent_router import viab_router
from agents.visualizer_agent import VisualizerAgent
from agents.interview_agent import InterviewAgent
from agents.boq_agent import BOQAgent
from agno.team.team import Team
from fastapi import File, UploadFile, Form, HTTPException
from typing import List
import os
import base64
from datetime import datetime
import uuid



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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
