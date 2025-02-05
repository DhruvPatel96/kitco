# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = "kitco-secret-2024"
    # mongo_uri_kitco: str = "mongodb://localhost:27017/kitco"
    mongo_uri_kitco: str = "mongodb://mongodb:27017/kitco"
    # mongo_uri_news: str = "mongodb://localhost:27017/news_database"
    mongo_uri_news: str = "mongodb://mongodb:27017/news_database"
    admin_secret: str = "admin-secret-2025"  # Set a strong admin secret
    news_api_key: str = "b8f4e356325d4b86adfc262230dbfbc1"  # Your NewsAPI.org API key
    faiss_index_path: str = "faiss_index.index"  # Path to store the FAISS index

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()