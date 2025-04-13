from peft import PeftModel
from transformers import AutoModelForCausalLM

base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # or wherever your base model came from
merged_path = "./merged-llama"

base_model = AutoModelForCausalLM.from_pretrained(base_model_id, torch_dtype=torch.float16)
model = PeftModel.from_pretrained(base_model, "lora-finetuned-llama")
merged_model = model.merge_and_unload()
merged_model.save_pretrained(merged_path)