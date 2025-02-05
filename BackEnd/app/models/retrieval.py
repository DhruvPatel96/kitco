# app/retrieval.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from app.config import settings
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB connection for news retrieval
client = MongoClient(settings.mongo_uri_news)
db = client["news_database"]
collection = db["articles"]

# Load the embedding model
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def load_recent_documents():
    """
    Load news articles from MongoDB that are published in the last 24 hours.
    Assumes published_at is in ISO 8601 format: '%Y-%m-%dT%H:%M:%SZ'.
    """
    recent_threshold = datetime.utcnow() - timedelta(days=1)
    documents = []
    for doc in collection.find({}, {"_id": 0, "title": 1, "description": 1, "content": 1, "published_at": 1}):
        published_str = doc.get("published_at", "")
        try:
            published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            logger.warning(f"Failed to parse published_at for document: {published_str}. Error: {e}")
            continue
        if published_dt >= recent_threshold:
            documents.append(f"{doc.get('title', '')} {doc.get('description', '')} {doc.get('content', '')}")
    logger.info(f"Loaded {len(documents)} recent documents (last 24 hours) from MongoDB.")
    return documents

def build_index():
    """Builds FAISS index from recent news articles."""
    logger.info("Building FAISS index from recent documents...")
    documents = load_recent_documents()
    if not documents:
        logger.warning("No recent documents found in MongoDB. FAISS index will be empty.")
        return None, documents
    embeddings = EMBEDDING_MODEL.encode(documents, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))
    logger.info(f"FAISS index built with {len(documents)} documents.")
    return index, documents

# Global index and document list (built at startup)
INDEX, DOCUMENTS = build_index()

def retrieve_context(query: str, top_k: int = 2) -> str:
    """
    Retrieves the most relevant documents based on the query.
    Only recent articles (last 24 hours) are used.
    """
    global INDEX, DOCUMENTS
    if INDEX is None or not DOCUMENTS:
        INDEX, DOCUMENTS = build_index()
        if INDEX is None:
            return "No relevant data available."
    query_embedding = EMBEDDING_MODEL.encode([query], convert_to_numpy=True)
    distances, indices = INDEX.search(query_embedding.astype(np.float32), top_k)
    retrieved_docs = [DOCUMENTS[i] for i in indices[0] if i < len(DOCUMENTS)]
    return " ".join(retrieved_docs)