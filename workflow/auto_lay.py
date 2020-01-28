import cv2
cv = cv2
import numpy as np
from glob import glob
files = glob("../pages/淮南鸿烈解.二十一卷.汉刘安撰.明茅坤.茅一桂辑评.明刊朱墨套印本 H*.png")
# files = glob("../pages/淮南鸿烈解.二十一卷.汉刘安撰.明茅坤.茅一桂辑评.明刊朱墨套印本 H10.png")
for f in files:
    print(f)
    im = cv2.imread(f)
    im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)
    im = im[50:-50,50:-50]

    c3 = im.astype(np.float32)/255
    gray = (np.clip(c3[:,:,2]+(c3[:,:,2]-c3[:,:,0]),0,1)*255).astype(np.uint8)

    _,th = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    _,th2 = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)

    th[:,10:150]=th2[:,10:150]
    th[:,-150:-10]=th2[:,-150:-10]

    th[600:-300,150:1200]=255

    th[600:-300,-1200:-150]=255

    # edges = cv2.Canny(gray,50,150,apertureSize = 3)


    minLineLength = 300
    maxLineGap = 10
    lines = cv2.HoughLinesP(255-th,rho=1,theta=np.pi/180,threshold=10,lines=10,minLineLength=minLineLength,maxLineGap=maxLineGap)
    if lines is not None:
        print(lines.shape)
        for xxx in lines:
            x1,y1,x2,y2 = xxx[0]
            cv2.line(im,(x1,y1),(x2,y2),(0,0,255),5)

    cv2.imshow('',th);cv2.waitKey(0)
    cv2.imshow('',im);cv2.waitKey(0)