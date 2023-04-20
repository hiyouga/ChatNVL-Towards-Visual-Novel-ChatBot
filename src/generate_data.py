import re
import json
import random
import hashlib


def check_sent(sent, stopwords):
    if len(sent) < 6:
        return False
    stop_cnt = 0
    for ch in sent:
        if ch in stopwords:
            stop_cnt += 1
    if stop_cnt > len(sent) * 0.5:
        return False
    return True


# def replace_name(sent, names, mapping, past_speaker, next_speaker):
#     for name in names:
#         if name not in sent[1]:
#             continue
#         if mapping[name] == mapping[sent[0]]:
#             sent[1] = sent[1].replace(name, "我")
#         elif past_speaker is not None and mapping[name] == mapping[past_speaker]:
#             sent[1] = sent[1].replace(name, "你")
#         elif next_speaker is not None and mapping[name] == mapping[next_speaker]:
#             sent[1] = sent[1].replace(name, "你")
#         else:
#             sent[1] = sent[1].replace(name, "她")
#     sent[1] = re.sub(r"我+", "我", sent[1])
#     sent[1] = re.sub(r"你+", "你", sent[1])
#     sent[1] = re.sub(r"她+", "她", sent[1])
#     return sent[1]


if __name__ == "__main__":

    file_name = "koikake"
    with open("stopwords.txt", "r", encoding="utf-8", newline="\n") as f:
        stopwords = f.read().strip().split("\n")
    with open(file_name+"/"+file_name+".name.json", "r", encoding="utf-8", newline="\n") as f:
        name_list = json.load(f)
    with open(file_name+"/"+file_name+".chat.json", "r", encoding="utf-8", newline="\n") as f:
        chats = json.load(f)
    names = [name for name, _ in name_list] # order is important!
    mapping = {name: name_id for name, name_id in name_list}
    dataset = []
    yuiset = []
    for conv in chats:
        # delete and merge
        sents = []
        last_speaker = None
        for sent in conv:
            sent["chs"] = sent["chs"].replace("…", "")
            if check_sent(sent["chs"], stopwords):
                if sent["speaker"] != last_speaker:
                    sents.append([sent["speaker"], sent["chs"]]) # 0: speaker, 1: content
                    last_speaker = sent["speaker"]
                else:
                    if sents[-1][1][-1] not in ["。", "，", "？", "！", "）"]:
                        sents[-1][1] += "。" + sent["chs"]
        # generate data
        if len(sents) < 2:
            continue
        hist = []
        total_len = 0
        idx = 0
        while idx < len(sents):
            sent = sents[idx]
            past_speaker = sents[idx-1][0] if idx > 0 else None
            next_speaker = sents[idx+1][0] if idx < len(sents) - 1 else None
            # text = replace_name(sent, names, mapping, past_speaker, next_speaker)
            text = sent[1]
            if len(hist) > 0:
                if len(hist) % 2 == 1:
                    sent_pairs = [(hist[2*i], hist[2*i+1]) for i in range(len(hist) // 2)]
                else:
                    sent_pairs = [(hist[2*i+1], hist[2*i+2]) for i in range((len(hist)-1) // 2)]
                dataset.append({
                    "instruction": hist[-1],
                    "input": "",
                    "output": text,
                    "history": sent_pairs
                })
                if sent[0] == "结衣":
                    yuiset.append({
                        "instruction": hist[-1],
                        "input": "",
                        "output": text,
                        "history": sent_pairs
                    })
            hist.append(text)
            total_len += len(text)
            while total_len > 1024:
                dummy = hist.pop(0)
                total_len -= len(dummy)
            idx += 1
    json.dump(dataset, open(file_name+"/"+file_name+".all.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    random.shuffle(dataset)
    json.dump(dataset[:100], open(file_name+"/"+file_name+".all.test.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    json.dump(dataset[100:], open(file_name+"/"+file_name+".all.train.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    with open(file_name+"/"+file_name+".all.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
    with open(file_name+"/"+file_name+".all.train.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
    with open(file_name+"/"+file_name+".all.test.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())

    json.dump(yuiset, open(file_name+"/"+file_name+".yui.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    random.shuffle(yuiset)
    json.dump(yuiset[:100], open(file_name+"/"+file_name+".yui.test.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    json.dump(yuiset[100:], open(file_name+"/"+file_name+".yui.train.json", "w", encoding="utf-8", newline="\n"), indent=4, ensure_ascii=False)
    with open(file_name+"/"+file_name+".yui.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
    with open(file_name+"/"+file_name+".yui.train.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
    with open(file_name+"/"+file_name+".yui.test.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
