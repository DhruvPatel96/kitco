# app/routers/video.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
from app.services.post_processor import format_video_metadata
from app.utils.security import api_key_dependency
import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(api_key_dependency)])
model, tokenizer = load_llm()

class VideoRequest(BaseModel):
    event: str

@router.post("/video")
async def generate_video_content(request: VideoRequest):
    try:
        logger.info(f"Generating video content for event: {request.event}")
        context = retrieve_context(request.event, top_k=2)
        prompt = PromptTemplates.rag_video_script(request.event, context)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=700,
            temperature=0.65,
            top_p=0.85,
            repetition_penalty=1.15
        )
        raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        processed_content = format_video_metadata(raw_text.split("SCRIPT:")[-1].strip())
        logger.info("Video content generated successfully.")
        return {
            "status": "success",
            "script": processed_content["script"],
            "metadata": processed_content["metadata"]
        }
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow - reduce input size")
        raise HTTPException(500, "GPU memory overflow - reduce input size")
    except Exception as e:
        logger.error(f"Video content generation failed: {str(e)}")
        raise HTTPException(500, f"Video content generation failed: {str(e)}")
