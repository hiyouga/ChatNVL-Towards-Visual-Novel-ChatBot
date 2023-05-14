# -*- coding: utf-8 -*-
import re
import json
import os

'''
此脚本的状态机对应姓名在前、对话在后的对话文件格式。
使用前将对话中所有会出现的人物姓名记录到names.txt文件中，同一个人物的不同称呼放在同一行，中间用空格分隔，names.txt与此脚本置于同一目录下。
最后将CUR_PATH设置为对话文件夹目录后运行此脚本即可生成数据集，输出为add.chat，add.full，add.name共3个json文件。
'''


IDLE = 100 # idle
WAIT = 200 # wait speaker
DONE = 300 # accept
TOLER = 400 # tolerance
INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"
CUR_PATH = "Temp" # 此处变量设置为对话文件夹相对目录


# 递归读取对话文件目录
def list_dir(file_dir):
    files = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):
            files.append(path)
        if os.path.isdir(path):
            files += list_dir(path)
    return files


if __name__ == "__main__":

    file_list = list_dir(CUR_PATH)
    # print(file_list)

    convs_list = [] # list of conversations
    multi_list = [] # list of parallel sentence
    name_list = []

    # 从所在目录的names.txt读取所有人物姓名
    with open(".\\names.txt", "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n")
        for i, line in enumerate(content):
            name_list += [[name, i] for name in line.strip().split()]
    names = [name for name, _ in name_list]

    for filename in file_list:
        with open(filename, "r", encoding="utf-8") as f:
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
            jpn = jpn.replace(FULLSPACE, "").replace("\\n", "").replace("[・]", "").strip()
            chs = chs.replace(FULLSPACE, "").replace("\\n", "").replace("[・]", "").strip()
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
                if chs in names:
                    temp = {"speaker": chs}
                    state = WAIT
            elif state == WAIT:
                if chs[0] == INDICATOR:
                    index_jpn = jpn.find(ENDICATOR)
                    index_chs = chs.find(ENDICATOR)
                    temp["jpn"] = jpn[1:index_jpn]
                    temp["chs"] = chs[1:index_chs]
                    convs.append(temp)  # complete one sentence
                    temp = None
                    state = DONE
                elif chs in names:
                    state = IDLE
            elif state == DONE:
                if chs in names:
                    temp = {"speaker": chs}
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
    json.dump(name_list, open("sanoba.name.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(convs_list, open("sanoba.chat.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    json.dump(multi_list, open("sanoba.full.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
