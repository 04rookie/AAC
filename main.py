from gpt4all import GPT4All
from rag import add_context, retrieve_context, delete_context
import re
import json
import csv
import nltk
from nltk.translate.meteor_score import meteor_score
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import word_tokenize

# Load local LLaMA model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
model_cos_sim = SentenceTransformer("all-MiniLM-L6-v2")
nltk.download('wordnet')
nltk.download('punkt_tab')

def start_conversation():
    # Start interactive chat
    # GPT 4 all keeps track of the current conversation, so we don't need to add the current conversation into the prompt
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
            add_context(f"Person: {user_input}\nAAC: {options[you]}")

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
        options = []
        for option in options_raw:
            if option.strip() != "":
                options.append(option.strip())
        for i in range(len(options)):
            # print(f"{i}. {options[i].strip()}")
            embedding_a = model_cos_sim.encode(ground_truth, convert_to_tensor=True)
            embedding_b = model_cos_sim.encode(options[i], convert_to_tensor=True)
            similarity_score = util.cos_sim(embedding_a, embedding_b)
            # print(similarity_score.item())
            m_score = meteor_score([word_tokenize(ground_truth)], word_tokenize(options[i]))
            with open('existing.csv', 'a', newline='') as file:
                new_row = [user_input, options[i], ground_truth, similarity_score.item(), m_score]
                writer = csv.writer(file)
                writer.writerow(new_row)
        
def evaluate_model():
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
            add_context(f"Person: {v[i]}\nAAC: {v[i+1]}")
        relevant_context = retrieve_context(v[-2])
        context_block = "\n".join(relevant_context)
        # TODO: run GPT4ALL
        generate_core_response(v[-2], context_block, ground_truth=v[-1])
        delete_context()
        
        
if __name__ == "__main__":
    start_conversation()
    # evaluate_model()