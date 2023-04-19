# -*- coding: utf-8 -*-


INDICATOR = "「"
ENDICATOR = "」"
FULLSPACE = "　"
REPLACES = [
    ("依頼人", "委托人"),
    ("ゆい", "结衣"),
    ("恵子", "惠子"),
    ("愛美", "爱美"),
    ("男子生徒", "男学生"),
    ("女子生徒", "女学生")
]


if __name__ == "__main__":

    filename = "润测/4-第三章"
    with open(filename+".txt", "r", encoding="utf-8") as f:
        data = f.read().strip().replace("\ufeff", "").split("\n") # throw UTF-8 BOM
    line_idx = 0
    line_max = len(data)
    content = []
    while line_idx < line_max:
        line_jpn = data[line_idx]
        line_chs = data[line_idx+1]
        # validate
        prefix_jpn, jpn = line_jpn[:12], line_jpn[12:]
        prefix_chs, chs = line_chs[1:13], line_chs[13:]
        jpn = jpn.replace(FULLSPACE, "").replace("<s36>", "").replace("</s>", "")
        chs = chs.replace(FULLSPACE, "").replace("<s36>", "").replace("</s>", "")
        chs = chs.replace(INDICATOR, "").replace(ENDICATOR, "")
        jpn = jpn.strip()
        chs = chs.strip()
        if prefix_jpn != prefix_chs:
            print("mismatched prefix at {}".format(prefix_jpn + prefix_chs))
            assert False
        if jpn[0] == INDICATOR:
            chs = INDICATOR + chs + ENDICATOR
        if len(chs) == 0:
            chs = jpn
            for source, target in REPLACES:
                chs = chs.replace(source, target)
        content += [prefix_jpn+jpn, ";"+prefix_chs+chs, ""]
        line_idx += 3
    with open(filename+".new.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
