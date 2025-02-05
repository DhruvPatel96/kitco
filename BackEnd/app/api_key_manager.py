# app/api_key_manager.py
import secrets
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from pymongo import MongoClient
from app.config import settings

router = APIRouter()

# Connect to MongoDB for API keys (using the kitco DB)
client = MongoClient(settings.mongo_uri_kitco)
db = client["kitco"]
api_keys_collection = db["api_keys"]

class APIKeyResponse(BaseModel):
    api_key: str

def generate_api_key() -> str:
    """Generates a secure 32-character hex API key."""
    return secrets.token_hex(16)

@router.post("/admin/generate-api-key", response_model=APIKeyResponse)
async def create_api_key(admin_secret: str = Header(..., alias="X-Admin-Secret")):
    """
    Generates a new API key.
    Requires an admin secret header for authorization.
    """
    if admin_secret != settings.admin_secret:
        raise HTTPException(status_code=403, detail="Not authorized to generate API keys")
    new_key = generate_api_key()
    api_keys_collection.insert_one({"api_key": new_key})
    return APIKeyResponse(api_key=new_key)

@router.get("/admin/list-api-keys")
async def list_api_keys(admin_secret: str = Header(..., alias="X-Admin-Secret")):
    """
    Lists all stored API keys (for admin use).
    """
    if admin_secret != settings.admin_secret:
        raise HTTPException(status_code=403, detail="Not authorized")
    keys = [doc["api_key"] for doc in api_keys_collection.find({}, {"_id": 0})]
    return {"api_keys": keys}

def validate_api_key(api_key: str = Header(..., alias="X-API-Key")):
    """
    Dependency function to validate the provided API key.
    Checks against the database.
    """
    if not api_keys_collection.find_one({"api_key": api_key}):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key