# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import json


import fontforge

font = fontforge.open("../dist/qiji.ttf")
font.generate("../dist/qiji.woff2")
print("√")

font = fontforge.open("../dist/qiji-fallback.ttf")
font.generate("../dist/qiji-fallback.woff2")
print("√")

font = fontforge.open("../dist/qiji-combo.ttf")
font.generate("../dist/qiji-combo.woff2")
print("√")