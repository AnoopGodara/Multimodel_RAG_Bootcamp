import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from src.utils.resource_manager import ResourceManager

logger = logging.getLogger(__name__)

class LocalLLM:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalLLM, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self):
        if self.initialized: return
        
        # Use a even smaller model if RAM is extremely tight
        model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        logger.info(f"Loading LLM {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        # CPU-friendly loading
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            low_cpu_mem_usage=True,
            torch_dtype=torch.float32,
            device_map="cpu"
        )
        self.initialized = True

    def generate(self, prompt: str, max_new_tokens: int = 512):
        if not self.initialized: self.initialize()
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant for Automotive Ergonomics. Answer based only on context provided."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt")

        with torch.no_grad():
            generated_ids = self.model.generate(**model_inputs, max_new_tokens=max_new_tokens)
        
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
