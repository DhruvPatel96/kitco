# app/faiss_indexer.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_and_save_index():
    """Builds FAISS index from stored news articles and saves it to disk."""
    logger.info("Building FAISS index...")
    client = MongoClient(settings.mongo_uri_news)
    db = client['news_database']
    collection = db['articles']

    documents = [f"{doc['title']} {doc['description']} {doc['content']}"
                 for doc in collection.find() if doc.get('content')]
    if not documents:
        logger.warning("No documents found in MongoDB. FAISS index will not be built.")
        return

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(documents, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))
    faiss.write_index(index, settings.faiss_index_path)
    logger.info(f"FAISS index built and saved with {len(documents)} documents.")

def append_to_index(new_articles):
    """Appends new articles to the FAISS index dynamically."""
    client = MongoClient(settings.mongo_uri_news)
    db = client['news_database']
    collection = db['articles']
    documents = [f"{doc['title']} {doc['description']} {doc['content']}"
                 for doc in new_articles if doc.get('content')]
    if not documents:
        return
    model = SentenceTransformer('all-MiniLM-L6-v2')
    new_embeddings = model.encode(documents, convert_to_numpy=True)
    index = faiss.read_index(settings.faiss_index_path)
    index.add(new_embeddings.astype(np.float32))
    faiss.write_index(index, settings.faiss_index_path)
    logger.info(f"Updated FAISS index with {len(documents)} new articles.")