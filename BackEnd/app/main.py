# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import editorial, video, anchors, marketing, social, feedback
from app.api_key_manager import router as api_key_router
from app.services.news_fetcher import fetch_and_store_articles
from app.models.faiss_indexer import build_and_save_index
import uvicorn
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app = FastAPI(
    title="Kitco AI Content Gateway",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev; restrict in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fetch_and_index_periodically():
    while True:
        logger.info("Periodic update: fetching articles and rebuilding FAISS index...")
        fetch_and_store_articles()
        build_and_save_index()
        await asyncio.sleep(5)  # Update every hour

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    fetch_and_store_articles()
    build_and_save_index()
    asyncio.create_task(fetch_and_index_periodically())

# Include routers
app.include_router(editorial.router, prefix="/api/v1/generate", tags=["Editorial"])
app.include_router(video.router, prefix="/api/v1/generate", tags=["Video Production"])
app.include_router(anchors.router, prefix="/api/v1/generate", tags=["Anchors"])
app.include_router(marketing.router, prefix="/api/v1/generate", tags=["Marketing"])
app.include_router(social.router, prefix="/api/v1/generate", tags=["Social Media"])
app.include_router(feedback.router, prefix="/api/v1", tags=["Feedback"])
app.include_router(api_key_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
