# app/utils/security.py
from fastapi import Depends
from app.api_key_manager import validate_api_key

async def api_key_dependency(api_key: str = Depends(validate_api_key)):
    return api_key