import json
# from rag_store import add_context

def load_dialogues_to_memory(json_file="aac_dialogues_memory.json"):
    with open(json_file, 'r') as f:
        dialogues = json.load(f)

    for key, utterances in dialogues.items():
        for i in range(0, len(utterances) - 1, 2):
            user_turn = utterances[i].strip()
            assistant_turn = utterances[i + 1].strip()
            memory_entry = f"They said: {user_turn} you responded: {assistant_turn}"
            # add_context(memory_entry)
            print(memory_entry)

    print("All dialogues have been loaded into memory.")

if __name__ == "__main__":
    load_dialogues_to_memory()
