import uuid
import json
import os
import time
import cv2
cv = cv2
import numpy as np
import sys

import os
from glob import glob

bpath="/Users/admin/proj/qiji-font/output/coarse/"
known_problem = [bpath+x for x in open("../data/ocr_crashers.txt",'r').read().split("\n")]
files = glob(bpath+"-H*.png")
# files=known_problem
# known_problem=[]

donfs = "\n".join([open(x,'r').read() for x in glob("../tmp/ocr_ret*.txt")])
done = [x.split("\t")[0] for x in donfs.split("\n") if len(x)]


os.chdir('/Users/admin/Downloads/darknet-ocr-master')

import sys
sys.path.append('/Users/admin/Downloads/darknet-ocr-master')
from dnn.main import text_ocr


for f in files:
    if f in done or f in known_problem:
        print(f,"done", file=sys.stderr)
        continue

    try:
        print(f+"\t",end="")
        sys.stdout.flush()
        # print(f, file=sys.stderr)
        image = cv2.imread(f)
        image =  cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        p = 100
        image = 255-cv2.copyMakeBorder( 255-image, p,p,p,p, cv.BORDER_CONSTANT, (0,0,0) );
        # cv2.imshow('',image);cv.waitKey(0)
        # print(image,scale,maxScale,TEXT_LINE_SCORE)
        data = text_ocr(image,200,300,0.0)

        o = ''.join([x['text'] for x in data])

        print(o)
        print(f+"\t"+o,file=sys.stderr)
        sys.stdout.flush()

    except:
        print(f,"fail", file=sys.stderr)
