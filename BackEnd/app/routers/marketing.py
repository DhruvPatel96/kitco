# app/routers/marketing.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
from app.services.post_processor import analyze_marketing_strategy
from app.utils.security import api_key_dependency
import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(api_key_dependency)])
model, tokenizer = load_llm()

class MarketingRequest(BaseModel):
    event: str

@router.post("/marketing")
async def generate_marketing_strategy(request: MarketingRequest):
    try:
        logger.info(f"Generating marketing strategy for event: {request.event}")
        context = retrieve_context(request.event, top_k=2)
        prompt = PromptTemplates.rag_marketing(request.event, context)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=600,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.1
        )
        raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        processed_strategy = analyze_marketing_strategy(raw_text.split("STRATEGY:")[-1].strip())
        logger.info("Marketing strategy generated successfully.")
        return {
            "status": "success",
            "campaign_ideas": processed_strategy["ideas"],
            "analytics_suggestions": processed_strategy["analytics"]
        }
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow - reduce input size")
        raise HTTPException(500, "GPU memory overflow - reduce input size")
    except Exception as e:
        logger.error(f"Marketing strategy generation failed: {str(e)}")
        raise HTTPException(500, f"Marketing strategy generation failed: {str(e)}")
