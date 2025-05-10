from flask import Flask, request, jsonify
from gpt4all import GPT4All
from rag_store import add_context, retrieve_context
# from rag_store import add_context, retrieve_context, delete_context
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import torch
from flask_cors import CORS
# Init
app = Flask(__name__)
CORS(app)
# CORS(app, origins=["http://localhost:3001"])
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
model_cos_sim = SentenceTransformer("all-MiniLM-L6-v2")
nltk.download("punkt_tab")
nltk.download("wordnet")

model_path = "./empathetic_flan_t5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model_t5 = AutoModelForSeq2SeqLM.from_pretrained(model_path)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model_t5 = model_t5.to(device)

types = ["positive", "negative", "neutral", "exploratory"]
def paraphrase(sentence, type=0):
    inputs = tokenizer(types[type] + " context: " + sentence, return_tensors="pt").to(device)
    output_ids = model_t5.generate(**inputs, max_length=256)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Store latest context
latest_conversation = {}
chat_session = model.chat_session() 
chat_session.__enter__()

    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # print(data["prompt"])
    user_input = data["prompt"].strip()
    if not user_input:
        return jsonify({'error': 'Missing user_input'}), 400

    relevant_context = retrieve_context(user_input)
    context_block = "\n".join(relevant_context)
    # print(data)
    user_type = data["type"]
    toggle = data["toggle"]
    print("toggle", toggle)
    if user_type == "you" and toggle == False:
        prompt = prompt = f"""
        <|system|>You are an AI assistant that auto-completion, conversational response options for AAC users. Use the following conversation context:
        {context_block}
        <|end|><|user|>{user_input}<|end|><|assistant|>
        Make sure to use the keywords provided in user input.
        Provide 4 short, helpful responses in plain text. Each response should be:
        1. One positive sentence.
        2. One negative sentence.
        3. One neutral sentence.
        4. One exploratory sentence.

        Write them as exactly 4 sentences, each on a new line, without bullet points or numbering. The responses should relate to the context I have shared with you. Do not add any extra text or formatting.
        <|end|>
        """
    else:
        prompt = f"""
        <|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:
        {context_block}
        <|end|><|user|>{user_input}<|end|><|assistant|>
        Provide 4 short, helpful responses in plain text. Each response should be:
        1. One positive sentence.
        2. One negative sentence.
        3. One neutral sentence.
        4. One exploratory sentence.

        Write them as exactly 4 sentences, each on a new line, without bullet points or numbering. The responses should relate to the context I have shared with you. Do not add any extra text or formatting.
        <|end|>
        """

    response = model.generate(prompt, max_tokens=500)

    options = [line.strip() for line in response.strip().split("\n") if line.strip()]
    options = [paraphrase(option) for option in options]
    # Save temporarily for second API
    if (user_type != "you"): 
        latest_conversation['user_input'] = user_input
    latest_conversation['options'] = options
    print({
        'context': context_block,
        'options': options
    })
    return jsonify({
        'context': context_block,
        'options': options
    })

@app.route('/respond', methods=['POST'])
def respond():
    data = request.json
    print(data["index"])
    if 'index' not in data:
        return jsonify({'error': 'Missing index'}), 400
    index = data["index"]

    if 'user_input' not in latest_conversation or 'options' not in latest_conversation:
        return jsonify({'error': 'No active conversation'}), 400

    try:
        user_input = latest_conversation['user_input']
        options = latest_conversation['options']
        selected_response = options[int(index)]
    except (IndexError, ValueError):
        return jsonify({'error': 'Invalid selected index'}), 400
    print(f"Selected response: {selected_response}")
    add_context(f"They said: {user_input} you responded: {selected_response}")
    return jsonify({'message': 'Response saved', 'response': selected_response})

if __name__ == '__main__':
    try:
        app.run(port=5000, debug=True)
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        chat_session.__exit__(None, None, None)
        print("Chat session closed.")