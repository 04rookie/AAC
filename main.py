from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from rag import add_context, retrieve_context, delete_context
from sentence_transformers import SentenceTransformer, util
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
import nltk
import torch
import json
import csv
from pathlib import Path

nltk.download("punkt")
nltk.download("wordnet")

# Load Mistral 7B Instruct model

device = "cuda" if torch.cuda.is_available() else "cpu"
mistral_models_path = Path.home().joinpath('mistral_models', '7B-Instruct-v0.3')
model_name = str(mistral_models_path)  # now pointing to local path

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto"
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device == "cuda" else -1)

model_cos_sim = SentenceTransformer("all-MiniLM-L6-v2")

def build_prompt(user_input, context_block):
    return f"""
<|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:
{context_block}
<|end|><|user|>{user_input}<|end|><|assistant|>
Provide 4 short, helpful responses in plain text. Each response should be:
1. One positive sentence.
2. One negative sentence.
3. One neutral sentence.
4. One exploratory sentence.

Write them as **exactly 4 sentences**, each on a new line, without bullet points or numbering. The responses should relate to the context I have shared with you. Do not add any extra text or formatting.
<|end|>
""".strip()

def start_conversation():
    while True:
        user_input = input("Person: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        relevant_context = retrieve_context(user_input)
        context_block = "\n".join(relevant_context)
        print(context_block)

        prompt = build_prompt(user_input, context_block)
        outputs = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
        response = outputs[0]["generated_text"].split("<|assistant|>")[-1].strip()
        
        options = [line.strip() for line in response.split("\n") if line.strip()]
        for i, opt in enumerate(options):
            print(f"{i}. {opt}")
        you = int(input("Select a response option: "))
        print("You selected?", you, options[you])
        add_context(f"Person: {user_input}\nAAC: {options[you]}")

def generate_core_response(user_input="", context_block="", ground_truth=""):
    prompt = build_prompt(user_input, context_block)
    outputs = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    response = outputs[0]["generated_text"].split("<|assistant|>")[-1].strip()
    
    options = [line.strip() for line in response.split("\n") if line.strip()]
    for i, option in enumerate(options):
        embedding_a = model_cos_sim.encode(ground_truth, convert_to_tensor=True)
        embedding_b = model_cos_sim.encode(option, convert_to_tensor=True)
        similarity_score = util.cos_sim(embedding_a, embedding_b).item()
        m_score = meteor_score([word_tokenize(ground_truth)], word_tokenize(option))
        with open('existing.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_input, option, ground_truth, similarity_score, m_score])

def evaluate_model():
    with open("anonymized_dialogues.json", 'r') as f:
        test = json.load(f)

    for count, (k, v) in enumerate(test.items()):
        print("Progress:", round(count / len(test), 2))
        for i in range(0, len(v) - 2, 2):
            add_context(f"Person: {v[i]}\nAAC: {v[i+1]}")
        relevant_context = retrieve_context(v[-2])
        context_block = "\n".join(relevant_context)
        generate_core_response(v[-2], context_block, ground_truth=v[-1])
        delete_context()

if __name__ == "__main__":
    start_conversation()
    # evaluate_model()
