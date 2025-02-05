# app/models/llm_loader.py 
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
from huggingface_hub import login
import os

HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Module-level cache variables
_model = None
_tokenizer = None

def get_device_config():
    try:
        if torch.cuda.is_available():
            return {"device": "cuda", "dtype": torch.float16}
        elif torch.backends.mps.is_available():
            return {"device": "mps", "dtype": torch.float16}
        else:
            return {"device": "cpu", "dtype": torch.float32}
    except Exception as e:
        logger.warning(f"Hardware detection failed: {str(e)}")
        return {"device": "cpu", "dtype": torch.float32}

def load_llm():
    global _model, _tokenizer
    if _model is not None and _tokenizer is not None:
        logger.info("Model already loaded. Returning cached model and tokenizer.")
        return _model, _tokenizer

    model_id = "meta-llama/Llama-3.2-3B-Instruct"
    try:
        login(token="TOKEN")
        config = get_device_config()
        logger.info(f"Using device: {config['device'].upper()}")
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            device_map=config["device"],
            torch_dtype=config["dtype"],
            low_cpu_mem_usage=True
        )
        if config["device"] == "mps":
            _model = _model.to("mps")
            torch.mps.empty_cache()
    except Exception as e:
        logger.warning(f"Error loading model on {config['device']}: {str(e)}")
        logger.info("Falling back to CPU with float32 precision")
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            device_map="cpu",
            torch_dtype=torch.float32
        )

    _tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        padding_side="left"
    )
    if _tokenizer.pad_token is None:
        _tokenizer.pad_token = _tokenizer.eos_token

    return _model, _tokenizer

if __name__ == "__main__":
    model, tokenizer = load_llm()
    prompt = ("Generate a concise, factual financial news summary for the event: "
              "Gold prices surge after Fed meeting.")
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.7
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info("Generated text:")
    logger.info(generated_text)