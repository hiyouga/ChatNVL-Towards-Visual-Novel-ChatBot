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

IDLE = 100 # idle
WAIT = 200 # wait speaker
DONE = 300 # accept
TOLER = 400 # tolerance
INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"

if __name__ == "__main__":

    convs_list = [] # list of conversations
    multi_list = [] # list of parallel sentence
    name_list = []
    with open("names.txt", "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n")
        for i, line in enumerate(content):
            name_list += [[name, i] for name in line.strip().split()]
    names = [name for name, _ in name_list]
    for filename in FILE_LIST:
        with open(filename+".txt", "r", encoding="utf-8") as f:
            data = f.read().strip().replace("\ufeff", "").split("\n") # delete UTF-8 BOM
        line_idx = 0
        line_max = len(data)
        state = IDLE
        temp = None
        convs = [] # conversation
        tor_num = 0
        tor_max = 3 # max non-chat lines between two chat lines in one conversation
        convs_min = 2 # min chat lines in one conversation
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
            if prefix_jpn != prefix_chs:
                print("mismatched prefix at {}".format(prefix_jpn + prefix_chs))
                assert False
            if len(jpn) == 0 or len(chs) == 0:
                print(filename, prefix_jpn)
                assert False
            # save the full chat
            if chs not in names:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    new_jpn = jpn[1:index_jpn]
                    new_chs = chs[1:index_chs]
                else:
                    new_jpn = jpn
                    new_chs = chs
                multi_list.append([new_jpn, new_chs])
            # finite-state machine
            if state == IDLE:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    temp = {"jpn": jpn[1:index_jpn], "chs": chs[1:index_chs]}
                    state = WAIT
            elif state == WAIT:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    temp = {"jpn": jpn[1:index_jpn], "chs": chs[1:index_chs]}
                elif chs in names:
                    temp["speaker"] = chs
                    convs.append(temp) # complete one sentence
                    temp = None
                    state = DONE
                else:
                    state = IDLE
            elif state == DONE:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    temp = {"jpn": jpn[1:index_jpn], "chs": chs[1:index_chs]}
                    state = WAIT
                else:
                    if tor_num < tor_max:
                        tor_num += 1
                    else:
                        tor_num = 0
                        if len(convs) >= convs_min:
                            convs_list.append(convs)
                        convs = []
                        state = IDLE
            line_idx += 3
    json.dump(name_list, open("koikake.name.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(convs_list, open("koikake.chat.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(multi_list, open("koikake.full.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
