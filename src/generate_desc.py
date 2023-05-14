import json
import hashlib


if __name__ == "__main__":

    file_name = "koikake"
    dataset = []
    with open(file_name + "/generated_descriptions.txt", "r", encoding="utf-8") as f:
        desc = f.read().strip().split("\n")
    for i in range(len(desc) // 2):
        dataset.append({
            "instruction": desc[2*i],
            "input": "",
            "output": desc[2*i+1]
        })
    json.dump(dataset, open("generated/"+file_name+".yui.desc.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    with open("generated/"+file_name+".yui.desc.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
