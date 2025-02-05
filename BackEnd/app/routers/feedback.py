# app/routers/feedback.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from pymongo import MongoClient
from app.config import settings
from app.utils.security import api_key_dependency
from app.services.regeneration import generate_regenerated_content

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(api_key_dependency)])

# Connect to MongoDB for storing feedback
client = MongoClient(settings.mongo_uri_kitco)
db = client["kitco"]
feedback_collection = db["feedback"]

class Feedback(BaseModel):
    team: str
    event: str
    original_response: str = Field(..., description="The AI generated response")
    feedback: str = Field(..., description="User feedback: good or bad")
    extra_prompt: str = Field(None, description="Extra instructions for regeneration (provided by user)")

@router.post("/feedback")
async def submit_feedback(feedback_data: Feedback):
    try:
        # Insert the feedback into MongoDB
        feedback_doc = feedback_data.dict()
        insert_result = feedback_collection.insert_one(feedback_doc)
        logger.info(f"Feedback stored with id: {insert_result.inserted_id}")

        # If the feedback is "bad", trigger regeneration
        if feedback_data.feedback.lower() == "bad":
            new_response = await generate_regenerated_content(
                team=feedback_data.team,
                event=feedback_data.event,
                original_response=feedback_data.original_response,
                feedback=feedback_data.feedback,
                extra_prompt=feedback_data.extra_prompt,
            )
            # Update the feedback document with the regenerated response
            feedback_collection.update_one(
                {"_id": insert_result.inserted_id},
                {"$set": {"regenerated_response": new_response}}
            )
            return {
                "status": "success",
                "message": "Feedback received; regeneration triggered.",
                "new_response": new_response
            }
        else:
            return {"status": "success", "message": "Feedback received."}
    except Exception as e:
        logger.error(f"Error handling feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
