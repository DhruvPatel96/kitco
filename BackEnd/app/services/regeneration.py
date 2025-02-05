# app/services/regeneration.py
import torch
from app.models.llm_loader import load_llm
from app.models.prompt_engineer import PromptTemplates
from app.models.retrieval import retrieve_context
import logging

logger = logging.getLogger(__name__)

async def generate_regenerated_content(
    team: str,
    event: str,
    original_response: str,
    feedback: str,
    extra_prompt: str = None,
) -> str:
    try:
        model, tokenizer = load_llm()
        context = retrieve_context(event, top_k=3)

        if team.lower() == "editorial":
            base_prompt = PromptTemplates.rag_editorial(event, context)
        elif team.lower() == "video":
            base_prompt = PromptTemplates.rag_video_script(event, context)
        elif team.lower() == "anchors":
            base_prompt = PromptTemplates.rag_teleprompter(event, context)
        elif team.lower() == "marketing":
            base_prompt = PromptTemplates.rag_marketing(event, context)
        elif team.lower() == "social":
            base_prompt = PromptTemplates.rag_social_media(event, context, platform="twitter")
        else:
            base_prompt = f"Generate content for the event: {event}.\nContext: {context}"

        regeneration_prompt = (
            f"{base_prompt}\n\n"
            f"Original Response: {original_response}\n\n"
            f"User Feedback: {feedback}"
        )
        if extra_prompt:
            regeneration_prompt += f"\nAdditional Instruction: {extra_prompt}"

        logger.info("Regeneration prompt constructed. Generating new response...")

        inputs = tokenizer(regeneration_prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        new_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logger.info("Regenerated response generated successfully.")
        return new_text
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU memory overflow during regeneration.")
        return "Error: GPU memory overflow during regeneration."
    except Exception as e:
        logger.error(f"Error in regeneration: {str(e)}")
        return f"Error during regeneration: {str(e)}"
