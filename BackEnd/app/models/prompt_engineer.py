# app/models/prompt_engineer.py
class PromptTemplates:
    @staticmethod
    def rag_editorial(event: str, context: str) -> str:
        return f"""<s>[INST] <<SYS>>
You are a senior editor at Kitco News. Using only the latest gold and silver news from the past 24 hours provided below, generate a concise, factual financial news summary in AP style.
- Inverted pyramid structure
- 3-5 concise paragraphs
- Factual, unbiased tone with proper financial terminology
- Dates formatted as MM/DD/YYYY
<</SYS>>

RECENT NEWS: {context}

EVENT: {event}
ARTICLE: [/INST]"""

    @staticmethod
    def rag_video_script(event: str, context: str) -> str:
        return f"""<s>[INST] <<SYS>>
Create a professional video script for Kitco News. Using only the latest gold and silver news from the past 24 hours provided below, generate a video script that includes:
- Clear scene descriptions in [brackets]
- Presenter dialogue for a 45-60 second runtime
- SEO-optimized title and description
- 5-7 relevant tags
- A brand-appropriate tone
<</SYS>>

RECENT NEWS: {context}

EVENT: {event}
SCRIPT: [/INST]"""

    @staticmethod
    def rag_teleprompter(event: str, context: str) -> str:
        return f"""<s>[INST] <<SYS>>
Generate a teleprompter script for live broadcast for Kitco News. Using only the latest gold and silver news from the past 24 hours provided below, generate a clear and engaging script with:
- Short, clear sentences
- Conversational tone
- Emphasis markers in (parentheses)
- Natural pause indicators (...)
- Total word count between 150-200 words
<</SYS>>

RECENT NEWS: {context}

EVENT: {event}
SCRIPT: [/INST]"""

    @staticmethod
    def rag_marketing(event: str, context: str) -> str:
        return f"""<s>[INST] <<SYS>>
Develop real-time marketing strategies for Kitco News. Using only the latest gold and silver news from the past 24 hours provided below, generate:
- 3 campaign ideas targeting financial audiences
- Data-driven analytics suggestions
- Platform-specific recommendations
- Hashtag suggestions
- Performance metrics to track
<</SYS>>

RECENT NEWS: {context}

EVENT: {event}
STRATEGY: [/INST]"""

    @staticmethod
    def rag_social_media(event: str, context: str, platform: str) -> str:
        limit = 280 if platform.lower() == "twitter" else 600
        return f"""<s>[INST] <<SYS>>
Create {platform} content for Kitco News. Using only the latest gold and silver news from the past 24 hours provided below, generate content that:
- Adheres to platform-specific best practices
- Respects a character limit of {limit} characters
- Includes 3-5 relevant hashtags
- Uses appropriate emoji usage and engagement-driving questions
<</SYS>>

RECENT NEWS: {context}

EVENT: {event}
POST: [/INST]"""