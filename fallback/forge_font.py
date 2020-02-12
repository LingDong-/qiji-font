# -*- coding: utf-8 -*-

# generate a TTF font using fontforge

from glob import glob
import os
import sys
import json
import fontforge

version = json.loads(open("../package.json", "r").read())["version"]

font = fontforge.font()
font.familyname = "QIJIFALLBACK"
font.fontname = "QIJIFALLBACK"
font.fullname= "QIJIFALLBACK"
font.copyright = "Copyright (c) 2020, Lingdong Huang"
font.version = version

for f in glob("../output/fallback_stage/*.svg"):
    char = f.split("/")[-1].split(".")[0]
    hx = ord(char)
    print(hx,char)
    glyph = font.createChar(hx)
    glyph.importOutlines(f)
    glyph.width=800
    glyph.simplify()

print(len(list(font.glyphs())))

font.generate("../dist/qiji-fallback.ttf")




