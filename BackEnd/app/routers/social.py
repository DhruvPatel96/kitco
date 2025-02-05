# app/routers/social.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
from app.services.post_processor import optimize_social_post
from app.utils.security import api_key_dependency
import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(api_key_dependency)])
model, tokenizer = load_llm()

class SocialRequest(BaseModel):
    event: str
    platform: str = "twitter"

@router.post("/social")
async def generate_social_content(request: SocialRequest):
    try:
        logger.info(f"Generating social media content for event: {request.event} on platform: {request.platform}")
        context = retrieve_context(request.event, top_k=2)
        prompt = PromptTemplates.rag_social_media(request.event, context, request.platform)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        max_tokens = 280 if request.platform.lower() == "twitter" else 600
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.75,
            top_p=0.92,
            repetition_penalty=1.05
        )
        raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        processed_post = optimize_social_post(raw_text.split("POST:")[-1].strip(), request.platform)
        logger.info("Social media content generated successfully.")
        return {
            "status": "success",
            "platform": request.platform,
            "content": processed_post["text"],
            "hashtags": processed_post["hashtags"],
            "character_count": len(processed_post["text"])
        }
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow - reduce input size")
        raise HTTPException(500, "GPU memory overflow - reduce input size")
    except Exception as e:
        logger.error(f"Social content generation failed: {str(e)}")
        raise HTTPException(500, f"Social content generation failed: {str(e)}")
