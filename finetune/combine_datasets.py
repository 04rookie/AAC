import json

def combine_datasets(file1, file2, output_file):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    combined_data = data1 + data2

    with open(output_file, "w") as out_file:
        json.dump(combined_data, out_file, indent=4)

    print(f"Combined {len(data1)} + {len(data2)} = {len(combined_data)} entries into {output_file}")

if __name__ == "__main__":
    combine_datasets("empathetic_finetune_dataset.json", "aac_aware_finetune_dataset.json", "finetune_dataset.json")
