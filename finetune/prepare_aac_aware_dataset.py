import json

def prepare_aac_aware_data(input_json, output_json):
    with open(input_json, "r") as file:
        dialogues = json.load(file)

    data = []

    for dialogue_id, utterances in dialogues.items():
        context = utterances[0]  # use the first utterance as prompt/context

        for i in range(len(utterances) - 1):
            user_utterance = utterances[i]
            assistant_response = utterances[i + 1]
            if i == 0:
                context = "I am an AAC user"
            # construct the prompt as in your previous script
            input_text = f"""
            <|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:
            {context}
            <|end|><|user|>{user_utterance}<|end|><|assistant|>
            Provide a short, helpful response in plain text. Write the response as exactly single sentence on a new line, without bullet points or numbering. The response should relate to the context I have shared with you. Do not add any extra text or formatting.
            <|end|>
            """.strip()

            data.append({
                "input": input_text,
                "output": assistant_response
            })

            # update context by appending the current utterance
            context += f"\nTurn {i+1}: {user_utterance}"

    with open(output_json, "w") as out_file:
        json.dump(data, out_file, indent=4)

    print(f"Prepared {len(data)} training samples.")

if __name__ == "__main__":
    prepare_aac_aware_data("../anonymized_dialogues.json", "aac_aware_finetune_dataset.json")
