from glob import glob
import cv2
import numpy as np
cv = cv2

pages = glob("../pages/*.png")
for p in pages:
	print(p)
	im = cv.imread(p,0).astype(np.float32)/255
	m = np.min(im)+0.1
	M = np.max(im)-0.1
	nml = (im-m)/(M-m)
	nml = np.clip(nml,0,1)
	cv2.imwrite("../tmp/compact_pages/"+p.split("/")[-1],cv2.resize((nml*255).astype(np.uint8),(0,0),fx=0.1,fy=0.1,interpolation=cv2.INTER_AREA))