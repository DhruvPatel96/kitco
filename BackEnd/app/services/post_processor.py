import re
from typing import Dict, Any


def enforce_ap_style(text: str) -> str:
    """Post-process text to enforce AP style guidelines"""
    replacements = {
        r"\b(\d+) percent\b": r"\1%",
        r"\$(\d+) million": r"US$\1 million",
        r"(\d+)-year": r"\1 year",
        r"(\d{1,2})/(\d{1,2})/(\d{4})": date_replacer
    }

    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    return text


def date_replacer(match: re.Match) -> str:
    """Convert MM/DD/YYYY to Month Day, Year format"""
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    month = months[int(match.group(1)) - 1]
    return f"{month} {match.group(2)}, {match.group(3)}"


def format_video_metadata(raw_text: str) -> dict:
    """Extract video script components from raw LLM output"""
    sections = raw_text.split("\n\n")
    return {
        "script": "\n\n".join(sections[:-1]),
        "metadata": {
            "title": sections[-1].split("Title: ")[-1].split("\n")[0],
            "description": sections[-1].split("Description: ")[-1].split("\n")[0],
            "tags": [tag.strip() for tag in sections[-1].split("Tags: ")[-1].split(",")]
        }
    }


def format_teleprompter_text(text: str) -> str:
    """Format teleprompter script for readability"""
    return "\n".join([f"{idx + 1}. {line.strip()}"
                      for idx, line in enumerate(text.split("\n"))])


def analyze_marketing_strategy(text: str) -> dict:
    """Parse marketing strategy into structured format"""
    return {
        "ideas": text.split("Campaign Ideas:")[-1].split("Analytics Suggestions:")[0].strip().split("\n"),
        "analytics": text.split("Analytics Suggestions:")[-1].strip().split("\n")
    }


def optimize_social_post(text: str, platform: str) -> dict:
    """Optimize social post for specific platforms"""
    hashtags = [word for word in text.split() if word.startswith("#")]
    content = " ".join([word for word in text.split() if not word.startswith("#")])

    if platform == "twitter":
        content = content[:277] + "..." if len(content) > 280 else content
    elif platform == "linkedin":
        content = f"{content}\n\n#finance #markets"

    return {
        "text": content,
        "hashtags": list(set(hashtags))[:5]  # Max 5 hashtags
    }


# app/services/post_processor.py (add this function)
def clean_generated_text(raw_text: str) -> str:
    """
    Cleans up the generated text by removing any prompt artifacts or system messages.
    """
    # Remove everything before the final "[/INST]" marker
    if "[/INST]" in raw_text:
        raw_text = raw_text.split("[/INST]")[-1].strip()

    # Remove any remaining system messages or unwanted tags
    cleanup_patterns = [
        r"<s>\[INST\].*?\[/INST\]",  # Remove any remaining [INST] blocks
        r"<<SYS>>.*?<</SYS>>",  # Remove any system messages
        r"ARTICLE:",  # Remove "ARTICLE:" label
        r"SCRIPT:",  # Remove "SCRIPT:" label
        r"POST:",  # Remove "POST:" label
        r"STRATEGY:",  # Remove "STRATEGY:" label
    ]

    for pattern in cleanup_patterns:
        raw_text = re.sub(pattern, "", raw_text, flags=re.DOTALL)

    # Remove extra whitespace and newlines
    raw_text = re.sub(r"\s+", " ", raw_text).strip()

    return raw_text