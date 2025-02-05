# app/routers/editorial.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
from app.utils.security import api_key_dependency
from app.services.post_processor import clean_generated_text
import logging
import torch

router = APIRouter(dependencies=[Depends(api_key_dependency)])
model, tokenizer = load_llm()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EditorialRequest(BaseModel):
    event: str

@router.post("/editorial")
async def generate_article(request: EditorialRequest):
    try:
        if not request.event:
            raise HTTPException(status_code=400, detail="Event description is required.")

        logger.info(f"Generating content for event: {request.event}")

        # Retrieve relevant articles using FAISS
        context = retrieve_context(request.event, top_k=3)

        # Construct LLM prompt with retrieved context
        prompt = PromptTemplates.rag_editorial(request.event, context)

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )

        raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean up the generated text
        cleaned_text = clean_generated_text(raw_text)

        logger.info("Generated article successfully.")
        return {"status": "success", "content": cleaned_text, "model": "Llama-3.2-3B-Instruct"}

    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow - reduce input size")
        raise HTTPException(500, "GPU memory overflow - reduce input size")
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(500, f"Internal Server Error: {str(e)}")
