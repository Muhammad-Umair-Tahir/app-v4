from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from agents.interview_agent import InterviewAgent
from agents.visualizer_agent import VisualizerAgent
from fastapi import File, UploadFile
from utility.utils import get_current_user, get_current_session, stream_text_response

interview_agent = InterviewAgent()
visualizer_agent = VisualizerAgent()

viab_router = APIRouter()

@viab_router.post("/interview")
async def start_interview(
    data: str,
    user_id: str = Depends(get_current_user),
    session_id: str = Depends(get_current_session)
):
    response_stream = interview_agent.interview(data, user_id=user_id, session_id=session_id)
    return StreamingResponse(stream_text_response(response_stream), media_type="text/plain")

@viab_router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    text: str = None,
    user_id: str = Depends(get_current_user),
    session_id: str = Depends(get_current_session)
):
    # Read the image file
    image_bytes = await file.read()

    # Send it to the agent
    response_stream = visualizer_agent.analyze_image(image_bytes, user_id=user_id, session_id=session_id)

    return StreamingResponse(stream_text_response(response_stream), media_type="text/plain")
