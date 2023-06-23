# -*- coding: utf-8 -*-
import os
import re
import json


INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"
CUR_PATH = "cn"


def collect_files(path): # read files
    return os.listdir(path)

def strip_text(text: str) -> str:
    start, end = text.find(INDICATOR), text.find(ENDICATOR)
    return text[start+1:end]

if __name__ == "__main__":

    file_list = collect_files(CUR_PATH)

    dialogs = [] # list of dialogs
    texts = [] # list of texts including narration

    for filename in file_list:

        with open(os.path.join("jp", filename), "r", encoding="utf-8") as f:
            jp_data = json.load(f)

        with open(os.path.join("cn", filename), "r", encoding="utf-8") as f:
            cn_data = json.load(f)

        assert len(jp_data) == len(cn_data)

        dialog = [] # dialog that may includes multiple chat lines
        num_tor = 0
        max_tor = 3 # maximum non-chat lines between two chat lines in one dialog
        min_len = 2 # minimum chat lines in one dialog

        for i in range(len(cn_data)):
            jpn = jp_data[i]["message"].replace(FULLSPACE, "")
            chs = cn_data[i]["message"].replace(FULLSPACE, "")

            # save texts
            jp_text = strip_text(jpn) if "name" in jp_data[i] else jpn
            cn_text = strip_text(chs) if "name" in jp_data[i] else chs
            texts.append([jp_text, cn_text])

            # save dialogs
            if "name" in cn_data[i]:
                dialog.append({
                    "jpn": strip_text(jpn),
                    "chs": strip_text(chs),
                    "speaker": cn_data[i]["name"]
                })
                num_tor = 0
            else:
                if num_tor < max_tor:
                    num_tor += 1
                else:
                    if len(dialog) > min_len:
                        dialogs.append(dialog)
                    dialog = []
                    num_tor = 0

    json.dump(dialogs, open("senren.chat.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(texts, open("senren.full.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
