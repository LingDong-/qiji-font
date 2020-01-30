# -*- coding: utf-8 -*-

# generate a TTF font using fontforge

from glob import glob
import os
import sys
import json


import fontforge

odd = [x.split("\t") for x in open("../data/variant_map.txt",'r').read().split("\n") if len(x)]
simp = json.loads(open("../data/TC2SC.json",'r').read())
simp = [[x,simp[x]] for x in simp]


font = fontforge.font()
font.familyname = "QIJI"



care = {x.split("\t")[0].split("/")[-1].split(".")[0]:x.split("\t")[1] for x in open("../data/labels_all.txt",'r').read().split("\n") if len(x)}

print(care)
for f in glob("../output/stage/*.svg"):
    if f.split("/")[-1].split(".")[0] not in care:
        continue
    char = care[f.split("/")[-1].split(".")[0]]

    other = set()
    for o in odd:
        if o[0] == char:
            other.add(o[1])
        elif o[1] == char:
            other.add(o[0])

    for o in simp:
        if o[0] == char:
            other.add(o[1])
        elif o[1] == char:
            other.add(o[0])
            
    print(char,list(other))
    hx = ord(char)
    print(hx,char)
    glyph = font.createChar(hx)
    glyph.importOutlines(f) 
    glyph.width=800

    for o in other:
        if o not in list(care.values()):
            hx = ord(o)
            glyph = font.createChar(hx)
            glyph.importOutlines(f)
            glyph.width=800
            print(o,"copied")
        else:
            print(o,"has own glyph")


print(len(list(font.glyphs())))

font.generate("../qiji.ttf")