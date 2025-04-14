from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pandas as pd
from datasets import Dataset
from transformers import Seq2SeqTrainingArguments
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainer, DataCollatorForSeq2Seq
from datasets import concatenate_datasets
import torch
model_name = "google/flan-t5-base"
# Load the CSV file
data = pd.read_csv("./empatheticdialogues/valid.csv", on_bad_lines='skip')
# print(data.head())

unique_values = data['context'].unique()
# print(unique_values)

emotion_to_class = {
    "terrified": "negative",
    "surprised": "explorative",
    "excited": "positive",
    "disgusted": "negative",
    "caring": "positive",
    "sentimental": "neutral",
    "sad": "negative",
    "embarrassed": "negative",
    "afraid": "negative",
    "impressed": "positive",
    "grateful": "positive",
    "joyful": "positive",
    "proud": "positive",
    "hopeful": "positive",
    "faithful": "positive",
    "lonely": "negative",
    "confident": "positive",
    "annoyed": "negative",
    "anticipating": "explorative",
    "furious": "negative",
    "jealous": "negative",
    "nostalgic": "neutral",
    "apprehensive": "negative",
    "guilty": "negative",
    "ashamed": "negative",
    "prepared": "neutral",
    "anxious": "negative",
    "content": "neutral",
    "angry": "negative",
    "devastated": "negative",
    "trusting": "positive",
    "disappointed": "negative"
}

# help(Seq2SeqTrainingArguments)

data['sentiment_class'] = data['context'].map(emotion_to_class)
# print(data[['context', 'sentiment_class']].head())
# data = data[:100]

# model_name = "google/flan-t5-base"  # Replace with flan-t5-small or larger variants if needed
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = torch.device("mps")  # instead of MPS
model = model.to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess_data(row):
    input_text = f"emotion: {row['context']} context: {row['prompt']}"
    target_text = row['utterance']
    return input_text, target_text

data['input_text'], data['target_text'] = zip(*data.apply(preprocess_data, axis=1))
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    # Tokenize input text
    inputs = tokenizer(
        examples["input_text"], max_length=512, truncation=True, padding="max_length"
    )
    
    # Tokenize target text (labels)
    targets = tokenizer(
        examples["target_text"], max_length=128, truncation=True, padding="max_length"
    ).input_ids

    # Replace padding token IDs with -100 for labels
    labels = [
        [(label if label != tokenizer.pad_token_id else -100) for label in target]
        for target in targets
    ]

    # Add labels to the inputs dictionary
    inputs["labels"] = labels

    return inputs


# dataset = Dataset.from_pandas(data)
# tokenized_dataset = dataset.map(tokenize_function, batched=True)
def chunk_dataframe(df, chunk_size):
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i+chunk_size]

tokenized_datasets = []

# Let's say you want 200 rows at a time
for chunk in chunk_dataframe(data, chunk_size=200):
    ds = Dataset.from_pandas(chunk)
    tokenized = ds.map(tokenize_function, batched=True)
    tokenized_datasets.append(tokenized)

# Concatenate them together
tokenized_dataset = concatenate_datasets(tokenized_datasets)

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=2,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_steps=100,
)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = torch.device("mps")  # instead of MPS
model = model.to(device)
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

trainer.train()
model.save_pretrained("./empathetic_flan_t5")
device = torch.device("cpu")  # instead of MPS
model = model.to(device)
tokenizer.save_pretrained("./empathetic_flan_t5")

def generate_response(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Example usage
input_example = "emotion: negative context: I lost my job and feel hopeless."
print(generate_response(input_example))
