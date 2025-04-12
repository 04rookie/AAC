from gpt4all import GPT4All
from rag_store import add_context, retrieve_context
import re
# Load local LLaMA model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

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

        # Get response
        response = model.generate(prompt, max_tokens=500)
        # print("Assistant:", response.strip())
        options = response.strip().split("\n")
        # print(options)
        for i in range(2, 6):
            print(f"{i}. {options[i].strip()}")
        you = int(input("select a response option"))
        # Flan t5
        # you = int(input("Select a response option: "))
        print("You selected?", you, options[you])
        # Store the user message to context store
        add_context("They said: " + user_input + " " + " you responded: " + options[you])
        
def start_conversation():