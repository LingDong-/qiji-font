import numpy as np
import cv2; cv = cv2
import random
import math
from PIL import Image, ImageFont, ImageDraw

def make_char(ch):

	font = ImageFont.truetype("../tmp/SourceHanSerifTC-SemiBold.otf",300)
	im = Image.new("L",(512,512))
	dr = ImageDraw.Draw(im)
	dr.text((110,42),ch,200,font=font)

	im = np.array(im)
	im00 = im.copy()
	# cv.imshow('',im);cv2.waitKey(0)

	im = im.astype(np.float32)/255;

	im = cv2.resize(im,(540,660))[74:-74,14:-14]

	for i in range(512):
		r = i*0.1*(0.95+0.05*math.sin(i*0.1))*0.5
		# r = random.random()*20
		im[52:460,i]=im[int(52+r):int(460+r),i]
	# cv.imshow('',im);cv2.waitKey(0)

	im0 = im.copy()

	im -= np.random.random((512,512))*0.1
	m2 = cv2.GaussianBlur(np.random.random((64,64)),(11,11),0)
	# cv.imshow('',m2);cv2.waitKey(0)
	im +=  cv2.GaussianBlur(cv2.resize(m2*1.1,(512,512),interpolation=cv2.INTER_AREA),(11,11),0)


	im = np.clip(im,0,1)
	im0 = cv2.dilate(im0,np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8),iterations=5)
	# cv.imshow('',im);cv2.waitKey(0)

	_,im = cv2.threshold(im,0.5,1,cv2.THRESH_BINARY)
	im = cv2.erode(im,np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8))

	im*=im0

	im = cv2.GaussianBlur(im,(21,21),0)
	_,im = cv2.threshold(im,0.5,1,cv2.THRESH_BINARY)
	# im = cv2.dilate(im,np.array([[0,1,0],[0,1,0],[0,1,0]],np.uint8),iterations=1)
	# im = cv2.erode(im,np.array([[0,0,0],[1,1,1],[0,0,0]],np.uint8),iterations=2)


	m3 = cv2.GaussianBlur(cv2.resize(cv2.GaussianBlur(np.random.random((16,16)),(11,11),0),(512,512),interpolation=cv2.INTER_AREA),(51,51),0)
	m4 = cv2.GaussianBlur(cv2.resize(np.random.random((256,256)),(512,512),interpolation=cv2.INTER_AREA),(11,11),0)
	_,m5 = cv2.threshold(m3*m4,0.18,1,cv2.THRESH_BINARY)

	m5 = cv2.dilate(m5,np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8),iterations=2)
	m5 = cv2.erode(m5,np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8),iterations=2)
	m5 = cv2.erode(m5,np.array([[0,0,0],[1,1,1],[0,0,0]],np.uint8),iterations=1)
	# m5 = cv2.erode(m5,np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]],np.uint8),iterations=1)
	# cv.imshow('',m5);cv2.waitKey(0)

	im = cv.morphologyEx(im, cv.MORPH_CLOSE, np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8))

	
	

	# im+=m3
	im *= m5

	im = (np.clip(1-im,0,1)*255).astype(np.uint8)


	# cv.imshow('',255-im);cv2.waitKey(0)

	# cv.imshow('',np.hstack((255-im00,im)));cv2.waitKey(0)
	return im

CH0 = 0x4e00
CH1 = 0x9feb

# lbls = [x.split("\t") for x in open("../data/labels_all.txt",'r').read().split("\n")]

# for p,l in lbls:
# 	im0 = make_char(l)
# 	im1 = cv2.imread("../output/fine/"+p.replace(".png",".bmp"),0)

# 	# cv2.imshow('',np.hstack((im0,im1)));cv2.waitKey(0)

# for i in range(20):
# 	c = chr(random.randrange(CH0,CH1))
# 	make_char(c)



for i in range(CH0,CH1):
	c = chr(i)
	print(c)
	im = make_char(c)
	cv2.imwrite("../output/fallback/"+c+".bmp",im)


