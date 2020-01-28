# -*- coding: utf-8 -*-

# generate a TTF font using fontforge

from glob import glob
import os
import sys

import fontforge

odd = [x.split("\t") for x in open("../data/variant_map.txt",'r').read().split("\n") if len(x)]

font = fontforge.font()
font.familyname = "QIJI"

care = {x.split("\t")[0].split("/")[-1].split(".")[0]:x.split("\t")[1] for x in open("../data/labels.txt",'r').read().split("\n") if len(x)}

for f in glob("../output/stage/*.svg"):
    char = care[f.split("/")[-1].split(".")[0]]

    other = None
    for o in odd:
        if o[0] == char:
            other = o[1]
        elif o[1] == char:
            other = o[0]
    print(char,other)
    hx = ord(char)
    # print(hx)
    glyph = font.createChar(hx)
    glyph.importOutlines(f)
    glyph.width=800

    if other:
        hx = ord(other)
        glyph = font.createChar(hx)
        glyph.importOutlines(f)
        glyph.width=800

font.generate("../qiji.ttf")