# -*- coding: utf-8 -*-
import os
import re
import json


INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"
CUR_PATH = "Temp"


def collect_files(path): # read files recursively
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        files = []
        for child in os.listdir(path):
            files += collect_files(os.path.join(path, child))
        return files


if __name__ == "__main__":

    file_list = collect_files(CUR_PATH)

    dialogs = [] # list of dialogs
    texts = [] # list of texts including narration
    name_pairs = [] # list of names and ids

    with open("names.txt", "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n")
        for i, line in enumerate(content):
            name_pairs += [[name, i] for name in line.strip().split()]
    names = [name for name, _ in name_pairs]

    for filename in file_list:
        with open(filename, "r", encoding="utf-8") as f:
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
            jpn = jpn.replace(FULLSPACE, "").replace("\\n", "").replace("[・]", "").replace("●", "").replace("%138;", "").strip()
            chs = chs.replace(FULLSPACE, "").replace("\\n", "").replace("[・]", "").replace("●", "").replace("%138;", "").strip()

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
            if chs in names:
                temp = chs # caching name
            elif chs[0] == INDICATOR and temp is not None:
                index_jpn = jpn.find(ENDICATOR)
                index_chs = chs.find(ENDICATOR)
                dialog.append({
                    "jpn": jpn[1:index_jpn],
                    "chs": chs[1:index_chs],
                    "speaker": temp
                }) # line completed
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

    json.dump(name_pairs, open("sanoba.name.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(dialogs, open("sanoba.chat.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(texts, open("sanoba.full.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
