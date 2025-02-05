# app/services/news_fetcher.py
from newsapi import NewsApiClient  # Ensure you installed newsapi-python
from pymongo import MongoClient, errors
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_articles():
    """Fetches the latest financial news and stores them in MongoDB."""
    logger.info("Fetching latest news articles...")

    # Initialize NewsApiClient with your NewsAPI.org API key
    newsapi = NewsApiClient(api_key=settings.news_api_key)

    try:
        # Fetch articles from NewsAPI.org using the 'everything' endpoint
        response = newsapi.get_everything(
            q='gold OR silver',
            language='en',
            sort_by='publishedAt',
            page_size=100
        )

        if response.get('status') == 'ok' and response.get('articles'):
            articles = response['articles']
            new_articles = []

            # Connect to MongoDB using the news database URI
            client = MongoClient(settings.mongo_uri_news)
            db = client['news_database']
            collection = db['articles']

            # Ensure a unique index on the 'url' field to prevent duplicate entries
            collection.create_index('url', unique=True)

            for article in articles:
                article_data = {
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "content": article.get("content", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("publishedAt", ""),
                    "source": article.get("source", {}).get("name", "")
                }
                try:
                    collection.insert_one(article_data)
                    new_articles.append(article_data)
                except errors.DuplicateKeyError:
                    continue  # Skip duplicates

            if new_articles:
                logger.info(f"Inserted {len(new_articles)} new articles into MongoDB.")
            else:
                logger.info("No new articles inserted (duplicates or empty data).")

            return new_articles
        else:
            logger.warning("No articles found or API request failed.")
            return []

    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}")
        return []