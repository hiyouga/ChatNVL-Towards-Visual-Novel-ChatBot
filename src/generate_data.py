import re
import json
import hashlib
from itertools import chain


def check_sentence(sentence, stopwords):
    if len(sentence) < 6:
        return False
    stop_cnt = 0
    for ch in sentence:
        if ch in stopwords:
            stop_cnt += 1
    if stop_cnt > len(sentence) * 0.5:
        return False
    return True


if __name__ == "__main__":

    file_name = "sanoba"
    person_name = "宁宁"
    person_id = "nene"
    max_length = 384
    window_size = 128

    with open("stopwords.txt", "r", encoding="utf-8", newline="\n") as f:
        stopwords = f.read().strip().split("\n")
    with open(file_name+"/"+file_name+".chat.json", "r", encoding="utf-8", newline="\n") as f:
        dialogs = json.load(f)

    dataset = []
    personset = []
    for dialog in dialogs:
        # delete and merge
        texts_with_speaker = []
        last_speaker = None
        for sentence in dialog:
            chn_text = sentence["chs"]
            chn_text = re.sub(r"…+", "…", chn_text)
            chn_text = re.sub(r"—+", "", chn_text)
            if check_sentence(chn_text, stopwords):
                if sentence["speaker"] != last_speaker:
                    texts_with_speaker.append([sentence["speaker"], chn_text]) # 0: speaker, 1: content
                    last_speaker = sentence["speaker"]
                else:
                    if texts_with_speaker[-1][1][-1] not in ["。", "，", "？", "！", "）", "…"]:
                        texts_with_speaker[-1][1] += "。" + chn_text
                    else:
                        texts_with_speaker[-1][1] += chn_text

        if len(texts_with_speaker) < 2:
            continue

        # group text with window size
        grouped_texts = []
        current_group = []
        current_length = 0
        for speaker, text in texts_with_speaker:
            current_group.append((speaker, text))
            current_length += len(text)
            if current_length >= window_size:
                grouped_texts.append(current_group)
                current_group = []
                current_length = 0
        if current_length != 0:
            grouped_texts.append(current_group)

        # split text with max length
        group_size = max_length // window_size
        for i in range(0, len(grouped_texts), group_size - 1):
            current_texts = list(chain(*grouped_texts[i : i + group_size]))
            for j in range(2):
                name_pairs = [(current_texts[2*k+j][0], current_texts[2*k+j+1][0]) for k in range((len(current_texts) - j) // 2)]
                text_pairs = [(current_texts[2*k+j][1], current_texts[2*k+j+1][1]) for k in range((len(current_texts) - j) // 2)]
                person_pairs = [text_pairs[i] for i in range(len(text_pairs)) if name_pairs[i][1] == person_name]
                if len(text_pairs) > 0:
                    dataset.append({
                        "instruction": text_pairs[-1][0],
                        "input": "",
                        "output": text_pairs[-1][1],
                        "history": text_pairs[:-1]
                    })
                if len(person_pairs) > 0:
                    personset.append({
                        "instruction": person_pairs[-1][0],
                        "input": "",
                        "output": person_pairs[-1][1],
                        "history": person_pairs[:-1]
                    })

    json.dump(dataset, open("generated/"+file_name+".all.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    with open("generated/"+file_name+".all.json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())

    json.dump(personset, open("generated/"+file_name+"."+person_id+".json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    with open("generated/"+file_name+"."+person_id+".json", "rb") as f:
        print(hashlib.sha1(f.read()).hexdigest())
