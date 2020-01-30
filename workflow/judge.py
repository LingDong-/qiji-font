import numpy as np
import cv2
cv = cv2
import json


# known_problem = ["/Users/admin/proj/qiji-font/coarse/"+x for x in open("../data/ocr_crashers.txt",'r').read().split("\n")]

goodone = [x.split("\t") for x in open("../tmp/labels.txt",'r').read().split("\n")]
misdone = [x.split("\t") for x in open("../tmp/mislabels.txt",'r').read().split("\n")]

mislabel = misdone
goodlabel = goodone
nolabel = []#known_problem

tc2sc = json.loads(open("../data/TC2SC.json",'r').read())
sc2tc = {}
for k in tc2sc:
	# if tc2sc[k] not in sc2tc:
	# 	sc2tc[tc2sc[k]] = []
	# sc2tc[tc2sc[k]].append(k)
	sc2tc[tc2sc[k]]=k

files = [x.replace("\t\t","\t").split("\t") for x in open("../data/labels_hnz_raw.txt",'r').read().split("\n") if len(x)]
files = [["../output/coarse/"+x[0],x[1]] for x in files]

done = [x.split("\t")[1] for x in open("../data/labels_lh.txt",'r').read().split("\n") if len(x)]

for f in files:
	if len(f) != 2:
		print(f)


collect = {}
for f,xs in files:
	# xs = [x for x in list(xs) if 0x4e00 < ord(x) < 0x9fff]
	if (len(xs) == 0):
		nolabel.append(f)
	for x in xs:
		if x not in done:
			if x not in collect:
				collect[x] = []
			collect[x].append(f)

print(collect.keys(),len(collect.keys()))

open("../tmp/nolabels.txt",'w').write("\n".join(nolabel))

mouse_x, mouse_y = 0,0
def get_mouse(event,x,y,flags,param):
    global mouse_x,mouse_y
    mouse_x = x
    mouse_y = y

cv2.namedWindow('im')
cv2.setMouseCallback('im',get_mouse)


cnt = 0
for c in collect:
	cnt +=1
	is_done = False;
	for x in collect[c]:
		for y in mislabel+goodlabel:
			if x == y[0]:
				is_done = True
				break

	if is_done:
		print("done",c)
		continue
	imgs = []
	for x in collect[c]:
		if cv.imread(x) is None:
			print("no img",c,x)
		else:
			imgs.append(x)
	if not len(imgs):
		continue
	im = np.hstack([cv.imread(i) for i in imgs[0:50]])
	c0 = c
	c2 = c
	if c in sc2tc:
		c = sc2tc[c]
	
	mlbl= []
	glbl = []
	cv2.imshow('im',im)

	n = 0

	print(cnt,'/',len(collect.keys()),'【',c,'】')

	
	def calc_n():
		global n
		n = mouse_x//256
		if (n < 0):
			n = 0
		if (n >= len(collect[c0])):
			n = len(collect[c0])-1

	while 1:
		draw = im.copy()
		
		calc_n()
		# print(glbl,mlbl)
		for i,x in enumerate(collect[c0]):
			for m in mlbl:
				if x == m[0]:
					cv2.rectangle(draw,(i*256,0),(i*256+256,256),(0,0,255),30)
			for m in glbl:
				if x == m[0]:
					cv2.rectangle(draw,(i*256,0),(i*256+256,256),(0,255,0),20)

		cv2.imshow('im',draw)
		k = cv2.waitKey(0)
		if k == ord('1'):
			calc_n()
			lx = (collect[c0][n],c)
			glbl.append(lx)
			print("goodlabel",len(glbl),lx)
			cv2.imshow('im',draw)
		elif k == ord('2'):
			calc_n()
			lx = (collect[c0][n],c)
			mlbl.append(lx)
			print("mislabel",len(mlbl),lx)
			cv2.imshow('im',draw)
		elif k == ord('3'):
			calc_n()
			c,c2 = c2,c
			print("tradswap",c)
			cv2.imshow('im',draw)
		elif k == ord('4'):
			glbl = []
			mlbl = []
		elif k == ord(' '):
			break;
		cv2.imshow('im',draw)

	for m in mlbl:
		if m not in mislabel:
			mislabel.append(m)
	for m in glbl:
		if m not in goodlabel:
			goodlabel.append(m)

	open("../tmp/labels.txt",'w').write("\n".join(["\t".join(list(x)) for x in goodlabel]))
	open("../tmp/mislabels.txt",'w').write("\n".join(["\t".join(list(x)) for x in mislabel]))
print(collect)