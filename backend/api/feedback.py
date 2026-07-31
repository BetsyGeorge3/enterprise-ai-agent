from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    rating: int  # e.g. 1 = thumbs down, 5 = thumbs up
    comment: str | None = None

@router.post("")
def submit_feedback(request: FeedbackRequest):
    # Placeholder — will store in Cosmos DB / evaluation dataset later
    return {"status": "feedback recorded", "data": request}