# -*- coding: utf-8 -*-
import re
import json

FILE_LIST = [
    "润测/1-序章",
    "润测/2-第一章",
    "润测/3-第二章",
    "润测/4-第三章.new",
    "润测/5-第四章",
    "润测/6.星奏回忆",
    "润测/7.星奏线",
    "润测/8.星奏线TE",
    "润测/9.四条凛香",
    "润测/10.小鞠结衣",
    "润测/11.新堂彩音_回忆"
]

INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"

if __name__ == "__main__":

    dialogs = [] # list of dialogs
    texts = [] # list of texts including narration
    name_pairs = [] # list of names and ids

    with open("names.txt", "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n")
        for i, line in enumerate(content):
            name_pairs += [[name, i] for name in line.strip().split()]
    names = [name for name, _ in name_pairs]

    for filename in FILE_LIST:
        with open(filename+".txt", "r", encoding="utf-8") as f:
            data = f.read().strip().replace("\ufeff", "").split("\n") # delete UTF-8 BOM

        line_idx = 0
        line_max = len(data)
        temp = None
        dialog = [] # dialog that may includes multiple chat lines
        num_tor = 0
        max_tor = 3 # maximum non-chat lines between two chat lines in one dialog
        min_len = 2 # minimum chat lines in one dialog

        while line_idx < line_max:
            line_jpn = data[line_idx]
            line_chs = data[line_idx+1]
            # validate
            prefix_jpn, jpn = line_jpn[:12], line_jpn[12:]
            prefix_chs, chs = line_chs[1:13], line_chs[13:]

            jpn = re.sub(r"<.+?>", "", jpn)
            chs = re.sub(r"<.+?>", "", chs)
            jpn = jpn.replace(FULLSPACE, "").strip()
            chs = chs.replace(FULLSPACE, "").strip()

            assert prefix_jpn == prefix_chs, "mismatched prefix at {}".format(filename + prefix_jpn + prefix_chs)
            assert len(jpn) != 0 and len(chs) != 0, "empty string at {}".format(filename + prefix_jpn + prefix_chs)

            # save texts
            if chs not in names:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    new_jpn = jpn[1:index_jpn]
                    new_chs = chs[1:index_chs]
                else:
                    new_jpn = jpn
                    new_chs = chs
                texts.append([new_jpn, new_chs])

            # save dialogs
            if chs[0] == INDICATOR:
                index_jpn = jpn.find(ENDICATOR)
                index_chs = chs.find(ENDICATOR)
                temp = {"jpn": jpn[1:index_jpn], "chs": chs[1:index_chs]}
            elif chs in names and temp is not None:
                temp["speaker"] = chs
                dialog.append(temp) # line completed
                temp = None
                num_tor = 0
            else:
                if num_tor < max_tor:
                    num_tor += 1
                else:
                    if len(dialog) > min_len:
                        dialogs.append(dialog)
                    dialog = []
                    num_tor = 0

            line_idx += 3

    json.dump(name_pairs, open("koikake.name.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(dialogs, open("koikake.chat.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(texts, open("koikake.full.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
