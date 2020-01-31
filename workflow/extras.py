import cv2
cv = cv2

im = cv2.imread("../singles/Snip20200131_9.png",0)
im = cv2.resize(im,(512,512))
im = cv2.GaussianBlur(im,(5,5),0)
im = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,151,5)

cv2.imshow('',im);cv2.waitKey(0)

cv2.imwrite("../output/singles/、.bmp",im)