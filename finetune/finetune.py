import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

# Load JSON dataset
with open("finetune_dataset.json", "r") as f:
    data = json.load(f)

# Convert to Hugging Face format
hf_data = Dataset.from_list([
    {"input": item["input"], "output": item["output"]} for item in data
])

# Load tokenizer & base model
base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # Replace with the actual HF model ID you have access to
tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_fast=True)
tokenizer.pad_token = tokenizer.eos_token

def format(example):
    text = f"{example['input'].strip()}\n{example['output'].strip()}"
    return tokenizer(text, padding="max_length", truncation=True, max_length=512)

tokenized = hf_data.map(format)

# Load model with 4-bit quantization
model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16
)

# Prepare for LoRA
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # common in LLaMA, adjust if needed
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Set training arguments
training_args = TrainingArguments(
    output_dir="./lora-finetuned-llama",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2,
    bf16=True,
    optim="paged_adamw_8bit"
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()

model.save_pretrained("lora-finetuned-llama")
tokenizer.save_pretrained("lora-finetuned-llama")
