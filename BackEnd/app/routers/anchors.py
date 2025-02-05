# app/routers/anchors.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
from app.services.post_processor import format_teleprompter_text
from app.utils.security import api_key_dependency
import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(api_key_dependency)])
model, tokenizer = load_llm()

class TeleprompterRequest(BaseModel):
    event: str

@router.post("/anchors")
async def generate_teleprompter_script(request: TeleprompterRequest):
    try:
        logger.info(f"Generating teleprompter script for event: {request.event}")
        context = retrieve_context(request.event, top_k=2)
        prompt = PromptTemplates.rag_teleprompter(request.event, context)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=400,
            temperature=0.5,
            top_p=0.95,
            repetition_penalty=1.2
        )
        raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        processed_text = format_teleprompter_text(raw_text.split("SCRIPT:")[-1].strip())
        logger.info("Teleprompter script generated successfully.")
        return {
            "status": "success",
            "teleprompter_script": processed_text,
            "word_count": len(processed_text.split())
        }
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow - reduce input size")
        raise HTTPException(500, "GPU memory overflow - reduce input size")
    except Exception as e:
        logger.error(f"Teleprompter generation failed: {str(e)}")
        raise HTTPException(500, f"Teleprompter generation failed: {str(e)}")
