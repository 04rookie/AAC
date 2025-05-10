from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pandas as pd
from datasets import Dataset, concatenate_datasets
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
import torch

# Load your previously fine-tuned model
model_path = "./empathetic_flan_t5"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Load the new dataset
data = pd.read_csv("./new_dataset.csv")  # Change path as needed

# Preprocess
data['input_text'] = data.apply(lambda row: f"emotion: {row['context']} context: {row['prompt']}", axis=1)
data['target_text'] = data['utterance']

def tokenize_function(examples):
    inputs = tokenizer(
        examples["input_text"], max_length=512, truncation=True, padding="max_length"
    )
    targets = tokenizer(
        examples["target_text"], max_length=128, truncation=True, padding="max_length"
    ).input_ids
    labels = [
        [(label if label != tokenizer.pad_token_id else -100) for label in target]
        for target in targets
    ]
    inputs["labels"] = labels
    return inputs

def chunk_dataframe(df, chunk_size):
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i+chunk_size]

tokenized_datasets = []
for chunk in chunk_dataframe(data, chunk_size=200):
    ds = Dataset.from_pandas(chunk)
    tokenized = ds.map(tokenize_function, batched=True)
    tokenized_datasets.append(tokenized)

tokenized_dataset = concatenate_datasets(tokenized_datasets)

# Define training args
training_args = Seq2SeqTrainingArguments(
    output_dir="./results_continued",
    eval_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=2,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    predict_with_generate=True,
    logging_dir="./logs_continued",
    logging_steps=100,
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

split_dataset = tokenized_dataset.train_test_split(test_size=0.1)
train_dataset = split_dataset["train"]
eval_dataset = split_dataset["test"]

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Continue training
trainer.train()

# Save the updated model
model.save_pretrained("./empathetic_flan_t5_continued")
tokenizer.save_pretrained("./empathetic_flan_t5_continued")

# Example inference
def generate_response(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    output_ids = model.generate(input_ids)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

print(generate_response("emotion: negative context: I was left out at school"))
