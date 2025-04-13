import csv
import json
from collections import defaultdict

def prepare_data(input_csv, output_json):
    conversations = defaultdict(list)

    with open(input_csv, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            conv_id = row["conv_id"]
            conversations[conv_id].append(row)

    data = []
    for conv_id, utterances in conversations.items():
        context = utterances[0]["prompt"]
        num_turns = len(utterances)
        
        # Sort by utterance_idx to maintain order
        utterances = sorted(utterances, key=lambda x: int(x["utterance_idx"]))
        for i in range(num_turns-1):
            input =  f"""
            <|system|>You are an AI assistant that provides short, conversational response options for AAC users. Use the following conversation context:
            {context}
            <|end|><|user|>{utterances[i]["utterance"]}<|end|><|assistant|>
            Provide a short, helpful response in plain text. Write the response as exactly single sentence on a new line, without bullet points or numbering. The response should relate to the context I have shared with you. Do not add any extra text or formatting.
            <|end|>
            """.strip()
            ground_truth = utterances[i+1]["utterance"]
            
            context + f"""\n
            Turn {i+1}: {utterances[i]["utterance"]}
            """            
        
            data.append({
            "input": input,
            "output": ground_truth
            })


    with open(output_json, "w") as out_file:
        json.dump(data, out_file, indent=4)

    print(f"Prepared {len(data)} conversation blocks.")

if __name__ == "__main__":
    prepare_data("emotional_data.csv", "emotional_finetune.json")
