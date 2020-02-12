# -*- coding: utf-8 -*-

# generate a TTF font using fontforge

from glob import glob
import os
import sys
import json
import fontforge

version = json.loads(open("../package.json", "r").read())["version"]

font = fontforge.open("../dist/qiji.ttf")
font.familyname = "QIJIC"
font.fontname = "QIJIC"
font.fullname= "QIJIC"
font.copyright = "Copyright (c) 2020, Lingdong Huang"
font.version = version

done = [x.unicode for x in list(font.glyphs())]
for x in list(font.glyphs()):
	if x.altuni:
		done += [y[0] for y in x.altuni]
done = list(set(done))


for f in glob("../output/fallback_stage/*.svg"):
    char = f.split("/")[-1].split(".")[0]
    hx = ord(char)
    print(hx,char)
    if hx in done:
    	print("done")
    	continue
    
    glyph = font.createChar(hx)
    
    glyph.importOutlines(f)
    glyph.width=800

print(len(list(font.glyphs())))

font.generate("../dist/qiji-combo.ttf")




