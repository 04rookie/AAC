from gpt4all import GPT4All
from rag_store import add_context, retrieve_context, delete_context
import re
import json
import csv
import nltk
from nltk.translate.meteor_score import meteor_score
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load local LLaMA model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
model_cos_sim = SentenceTransformer("all-MiniLM-L6-v2")
nltk.download('wordnet')
nltk.download('punkt_tab')

model_path = "./empathetic_flan_t5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model_t5 = AutoModelForSeq2SeqLM.from_pretrained(model_path)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model_t5 = model_t5.to(device)

types = ["positive", "negative", "neutral", "exploratory"]
def start_conversation():
    # Start interactive chat
    with model.chat_session():
        while True:
            user_input = input("Person: ")

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            # Get context from RAG
            relevant_context = retrieve_context(user_input)
            context_block = "\n".join(relevant_context)
            print(context_block)
            # Build prompt
            prompt = f"<|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:\n{context_block}\n<|end|><|user|>{user_input}<|end|><|assistant|>Provide 4 short, helpful responses. One positive, one negative, one neutral and one exploratory. The responses should be related to context I have shared with you. Give them to me in 4 lines ONLY. So that it is easy to extract:\n"
            prompt = f"""
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
            """

            # Get response
            response = model.generate(prompt, max_tokens=500)
            # print("Assistant:", response.strip())
            options_raw = response.strip().split("\n")
            options = []
            for option in options_raw:
                if option.strip() != "":
                    options.append(option.strip())
            for i in range(len(options)):
                print(f"{i}. {options[i].strip()}")
            you = int(input("select a response option"))
            # Flan t5
            # you = int(input("Select a response option: "))
            print("You selected?", you, options[you])
            # Store the user message to context store
            add_context("They said: " + user_input + " " + " you responded: " + options[you])

def generate_core_response(user_input="", context_block="", ground_truth=""):
    with model.chat_session():
        prompt = f"<|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:\n{context_block}\n<|end|><|user|>{user_input}<|end|><|assistant|>Provide 4 short, helpful responses. One positive, one negative, one neutral and one exploratory. The responses should be related to context I have shared with you. Give them to me in 4 lines ONLY. So that it is easy to extract:\n"
        prompt = f"""
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
            """
        response = model.generate(prompt, max_tokens=500)
        # print("Assistant:", response.strip())
        options_raw = response.strip().split("\n")
        options_gpt = []
        options_t5 = []
        i = 0
        for option in options_raw:
            if option.strip() != "":
                options_gpt.append(option.strip())
                options_t5.append(paraphrase(option.strip(), 2 if i > 3 else i))
                i += 1
        for i in range(len(options_gpt)):
            # print(f"{i}. {options[i].strip()}")
            embedding_a = model_cos_sim.encode(ground_truth, convert_to_tensor=True)
            embedding_b = model_cos_sim.encode(options_t5[i], convert_to_tensor=True)
            similarity_score = util.cos_sim(embedding_a, embedding_b)
            # print(similarity_score.item())
            m_score = meteor_score([word_tokenize(ground_truth)], word_tokenize(options_t5[i]))
            with open('existing.csv', 'a', newline='') as file:
                new_row = [user_input, ground_truth, options_gpt[i], options_t5[i], similarity_score.item(), m_score]
                writer = csv.writer(file)
                writer.writerow(new_row)
        
def evaluate():
    test = None
    with open("anonymized_dialogues.json", 'r') as f:
        test = json.load(f)
    # print(test[0])
    # for i in range(0, len(test["dialogue001"])-2, 2):
    #     print(test["dialogue001"][i])
    count = 0
    for k, v in test.items():
        print("Progress:", round(count/len(test)))
        count += 1
        for i in range(0, len(v)-2, 2):
            # print(test["dialogue001"][i])
            add_context("They said: " + v[i] + " " + " you responded: " + v[i+1])
        relevant_context = retrieve_context(v[-2])
        context_block = "\n".join(relevant_context)
        # TODO: run GPT4ALL
        generate_core_response(v[-2], context_block, ground_truth=v[-1])
        delete_context()


def paraphrase(sentence, type=0):
    inputs = tokenizer(types[type] + " context: " + sentence, return_tensors="pt").to(device)
    output_ids = model_t5.generate(**inputs, max_length=256)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    # start_conversation()
    evaluate()