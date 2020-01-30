import cv2
cv = cv2
from glob import glob
import numpy as np
import random

def f2t(f):
    return "../data/rects/"+f.split(" ")[1].split(".")[0]+".tsv"

# files = glob("pages/李长吉歌诗.4卷.外诗集1卷.李贺撰.刘辰翁评.明末凌濛初刊闵氏朱墨套印本 11.png")

files = glob("../pages/* H*.png")
files = glob("../pages/* H230.png")

done = glob("../output/coarse/*.png")

def show(x):
    cv2.imshow('',x);cv2.waitKey(0)

for f in files:
    
    print(f)
    rects = [[int(y) for y in x.split("\t")] for x in open(f2t(f),'r').read().split("\n") if len(x)]
    im = cv2.imread(f);
    for r in rects:
        if (not r[2]) or (not r[3]):
            continue
        # if not (4500<r[0]<5000 and 1500 < r[1] < 2000):
            # continue
        # print(r)

        oname = "-"+f2t(f).split("/")[-1].split(".")[0]+"-"+"_".join([str(x) for x in r])+".png"

        if oname in done:
            continue

        c3 = im[int(r[1]-r[3]*0.1):int(r[1]+r[3]*1.2),int(r[0]-r[2]*0.1):int(r[0]+r[2]*1.2)].astype(np.float32)/255
        c = (np.clip(c3[:,:,2]+(c3[:,:,2]-c3[:,:,0]),0,1)*255).astype(np.uint8)

        c = cv2.GaussianBlur(c,(3,3),0)
        # ath = cv2.adaptiveThreshold(c,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,15)

        ret,th = cv2.threshold(c,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        _,th = cv2.threshold(c,ret+10,255,cv2.THRESH_BINARY)
        # thd = 255-(((th.astype(np.float32)/255)*(ath.astype(np.float32)/255))*255).astype(np.uint8)
        thd = 255-th

        contours,hier = cv.findContours(thd, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        # print(hier)

        boundRect = [None]*len(contours)

        for i, _ in enumerate(contours):

            boundRect[i] = cv.boundingRect(contours[i])
        
        drawing = np.zeros((th.shape[0],th.shape[1],3), dtype=np.uint8)
        
        nhier = {}
        mask = []

        def rectok(r):
            # return True
            if (r[0] < 5):
                return False
            if (r[1] < 5):
                return False
            if (r[1]+r[3] > th.shape[0]-5):
                return False
            if (r[0]+r[2] > th.shape[1]-5):
                return False

            if (r[2]<20):
                if (r[0] < 20):
                    return False
                if (r[0]+r[2] > th.shape[1]-20):
                    return False

            if (r[3]<20):
                if (r[1] < 20):
                    return False
                if (r[1]+r[3] > th.shape[0]-20):
                    return False

            if (r[2] < 10 and r[3] < 10):
                return False
            return True

        for i in range(len(contours)):
            rc = boundRect[i]
            if not rectok(rc):
                continue
            is_hole = hier[0][i][3] >= 0;
            if not is_hole:
                color = (random.randrange(128,255), random.randrange(128,255), random.randrange(128,255))
            else:
                color = (0,0,0)
                # print(hier[0][i])

            cnt = contours[i]
            approx = cv2.approxPolyDP(cnt,1.5,True)

            cv.drawContours(drawing, [approx], 0, color, -1)
            for x in approx:
                cv.rectangle(drawing, (x[0,0]-1,x[0,1]-1), (x[0,0]+1,x[0,1]+1), (0,0,255), 1)

            if not is_hole:
                nhier[i] = []
                mask.append(i)
            else:
                p = hier[0][i][3]
                if rectok(boundRect[p]):
                    if not (p in nhier):
                        nhier[p] = []
                    nhier[p].append(i)
                    mask.append(i)
        
        ncnt = []
        for i in range(len(contours)):
            approx = cv2.approxPolyDP(contours[i],1.5,True)
            # approx = contours[i]
            approx = [x[0] for x in approx]
            ncnt.append(approx)
        # print(n cnt)
        pts = []
        for i in mask:
            for j in range(len(ncnt[i])):
                pts.append(ncnt[i][j])
        if (len(pts) == 0):
            continue
        bd = cv.boundingRect(np.array(pts))
  
        px,py = 0,0
        s = 1
        if bd[2]>bd[3]:
            py = (bd[2]-bd[3])/2
            s = 1/bd[2]
        else:
            px = (bd[3]-bd[2])/2
            s = 1/bd[3]

        for i in mask:
            for j in range(len(ncnt[i])):
                x = round((ncnt[i][j][0]-bd[0]+px)*s*256)
                y = round((ncnt[i][j][1]-bd[1]+py)*s*256)  
                ncnt[i][j][0] = x
                ncnt[i][j][1] = y

        ren = np.ones((256,256),np.uint8)*255


        for k in nhier:
            cv.drawContours(ren, [np.array(ncnt[k])], 0, (0,0,0), -1);

            for k1 in nhier[k]:
                cv.drawContours(ren, [np.array(ncnt[k1])], 0, (255,255,255), -1);


        for i in nhier:
            re = boundRect[i]
            cv.rectangle(drawing, (int(re[0]), int(re[1])), (int(re[0]+re[2]), int(re[1]+re[3])), (255,255,255), 1)
       
        # show(ren)
        # show(c3)
        # show(thd)
        # show(drawing)

        cv2.imwrite("../tmp/dbg/"+oname,drawing)
        cv2.imwrite("../output/coarse/"+oname,ren)
