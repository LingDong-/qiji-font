import cv2
cv = cv2
from glob import glob
import numpy as np
import random

def f2t(f):
    return "../data/rects/"+f.split(" ")[1].split(".")[0]+".tsv"

# files = glob("pages/李长吉歌诗.4卷.外诗集1卷.李贺撰.刘辰翁评.明末凌濛初刊闵氏朱墨套印本 11.png")

files = glob("../pages/* H*.png")


def show(x):
    cv2.imshow('',x);cv2.waitKey(0)

care = [x.split("\t")[0].split("/")[-1].split(".")[0] for x in open("../data/labels_hnz.txt",'r').read().split("\n") if len(x)]

print(len(care))
for f in files:
    print(f)
    rects = [[int(y) for y in x.split("\t")] for x in open(f2t(f),'r').read().split("\n") if len(x)]

    im = None
    for r in rects:
        if (not r[2]) or (not r[3]):
            continue

        bname = "-"+f2t(f).split("/")[-1].split(".")[0]+"-"+"_".join([str(x) for x in r])

        if (bname not in care):
            continue

        if im is None:
            im = cv2.imread(f)

        c3 = im[int(r[1]-r[3]*0.1):int(r[1]+r[3]*1.2),int(r[0]-r[2]*0.1):int(r[0]+r[2]*1.2)].astype(np.float32)/255
        c = (np.clip(c3[:,:,2]+(c3[:,:,2]-c3[:,:,0]),0,1)*255).astype(np.uint8)
        c0 = (cv2.cvtColor(c3,cv.COLOR_BGR2GRAY)*255).astype(np.uint8)

        c = cv2.GaussianBlur(c,(5,5),0)
        # th = cv2.adaptiveThreshold(c,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,15)

        ret,th = cv2.threshold(c,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        _,th = cv2.threshold(c,ret+10,255,cv2.THRESH_BINARY)
        # thd = 255-(((th.astype(np.float32)/255)*(ath.astype(np.float32)/255))*255).astype(np.uint8)
        thd = 255-th

        # a = thd
        # a = cv2.dilate(a,np.array([[0,0,0,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,0,0,0]],np.uint8),iterations = 5)
        # a = cv2.dilate(a,np.array([[0,0,1,0,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,0,1,0,0]],np.uint8),iterations = 1)
        # a = cv2.dilate(a,np.array([[0,1,0],[0,1,0],[0,1,0]],np.uint8),iterations = 1)
        # a = cv2.erode(a,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations = 5)
        # a = cv2.erode(a,np.array([[0,0,0,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,0,0,0]],np.uint8),iterations = 2)
        # thd = a


        contours,hier = cv.findContours(thd, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
        # print(hier)

        boundRect = [None]*len(contours)

        for i, _ in enumerate(contours):

            boundRect[i] = cv.boundingRect(contours[i])
        
        drawing = np.zeros((th.shape[0],th.shape[1],3), dtype=np.uint8)
        
        nhier = {}
        mask = []

        def rectok(r):
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

            cv.drawContours(drawing, [cnt], 0, color, -1)
            for x in cnt:
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
            # approx = cv2.approxPolyDP(contours[i],1.5,True)
            approx = contours[i]
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
        ss = 1.05
        if bd[2]>bd[3]:
            
            s = ss/(th.shape[1])
            px = (th.shape[1]-bd[2])/2
            py = px+(bd[2]-bd[3])/2
        else:
            
            s = ss/(th.shape[0])
            py = (th.shape[0]-bd[3])/2
            px = py+(bd[3]-bd[2])/2

        # print(s)
        # exit()  
        W = 512       

        for i in mask:
            for j in range(len(ncnt[i])):
                x = (ncnt[i][j][0]-bd[0]+px)*s*W
                y = (ncnt[i][j][1]-bd[1]+py)*s*W
                ncnt[i][j][0] = x
                ncnt[i][j][1] = y
        # exit()

        tr = np.zeros((W,W),np.float32)
        for k in nhier:

            cv.drawContours(tr, [np.array(ncnt[k])], 0, (1,1,1), -1);

            for k1 in nhier[k]:
                cv.drawContours(tr, [np.array(ncnt[k1])], 0, (0,0,0), -1);

        #######################
        su = np.sum(tr)
        sl,sr,st,sb = 0,0,0,0
        for il in range(tr.shape[1]):
            sl += np.sum(tr[:,il])
            if (sl > su*0.1):
                break
        
        for ir in range(tr.shape[1]):
            sr += np.sum(tr[:,tr.shape[1]-1-ir])
            if (sr > su*0.1):
                break
        

        for it in range(tr.shape[0]):
            st += np.sum(tr[it,:])
            if (st > su*0.1):
                break

        for ib in range(tr.shape[0]):
            sb += np.sum(tr[tr.shape[0]-1-ib,:])
            if (sb > su*0.1):
                break

        hshft = (ir-il)/2
        vshft = (ib-it)/2
        #######################

        for i in mask:
            for j in range(len(ncnt[i])):
                ncnt[i][j][0] = ncnt[i][j][0]+hshft
                ncnt[i][j][1] = ncnt[i][j][1]+vshft

        trr = np.zeros((W,W),np.float32)
        for k in nhier:
            cv.drawContours(trr, [np.array(ncnt[k])], 0, (1,1,1), -1);

            for k1 in nhier[k]:
                cv.drawContours(trr, [np.array(ncnt[k1])], 0, (0,0,0), -1);

        # cv2.imwrite("xrend/"+bname+".png",255*(1-trr))

        cp = cv2.copyMakeBorder(c0,100,100,100,100,cv2.BORDER_CONSTANT,value=255)
        # print(s)
        nbd = [int(1/1*(bd[0]-px+100)-hshft/(s*W)*ss),int(1/1*(bd[1]-py+100)-vshft/(s*W)*ss),int(1/ss*(bd[2]+px*2)),int(1/ss*(bd[3]+py*2))];
        # print(px,py,nbd)
        crp = cp[nbd[1]:nbd[1]+nbd[3],nbd[0]:nbd[0]+nbd[2]]
        crp = cv.resize(crp,(trr.shape[0],trr.shape[1]),cv2.INTER_AREA)

        trrd = cv2.dilate(trr,np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]],np.uint8),iterations = 5)
        crpd = crp

        crpd = cv2.adaptiveThreshold(crpd,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,151,15)

        # cv2.imshow('',crpd)
        fnl = ((1-trrd*(1-crpd.astype(np.float32)/255))*255).astype(np.uint8)
        # cv2.imshow('',fnl);cv2.waitKey(0)
        cv2.imwrite("../output/fine/"+bname+".bmp",fnl)
