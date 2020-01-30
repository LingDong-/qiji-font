# import cv2
# bads = [x.split("\t")[0] for x in open("../tmp/mislabels.txt",'r').read().split("\n") if len(x)]

# for b in bads:
# 	try:
# 		im = cv2.imread(b)
# 		cv2.imwrite(b.replace("output/coarse","tmp/relabel"),im)
# 	except:
# 		print(b)


from glob import glob

olbl = [x.split("\t") for x in open("../data/labels_lh.txt",'r').read().split("\n") if len(x)]
nlbl = [x.split("\t") for x in open("../tmp/labels.txt",'r').read().split("\n") if len(x)]

clbl = olbl+nlbl

rl = [x.split("/")[-1] for x in glob("../tmp/relabel/*.png") if x.split("/")[-1][0] != "-"]
rlbl = [["-"+"-".join(x.split("-")[1:]),x.split("-")[0]] for x in rl]

rlbl = [x for x in rlbl if x[1] not in [y[1] for y in clbl]]

dlbl = clbl+rlbl
elbl = [x for x in nlbl+rlbl if x[1] not in [y[1] for y in olbl]]
# print(elbl,len(elbl))


open("../data/labels_hnz.txt",'w').write("\n".join([x[0]+"\t"+x[1] for x in elbl]))

ks = set([x[1] for x in olbl]+[x[1] for x in nlbl]+[x[1] for x in rlbl])
vs = olbl+nlbl+rlbl
flbl = []
for k in ks:
	for v in vs:
		if k == v[1]:
			break
	flbl.append(v)
# print(flbl,len(flbl))

open("../data/labels_all.txt",'w').write("\n".join([x[0]+"\t"+x[1] for x in flbl]))

# import cv2
# cv = cv2
# import numpy as np
# from glob import glob
# files = glob("./nolabel/*.png")


# new = []
# st = set()
# for f in files:
# 	ch = f.split("-")[-3].split("/")[-1]
# 	if len(ch) == 0:
# 		continue
# 	st.add(ch)
# 	pth = f.replace(ch,'').replace('nolabel','rend')
# 	new.append([pth,ch])


# done = [x.split("\t") for x in open("new-new-labels.txt",'r').read().split("\n") if len(x)]


# comb = done+new
# collect = {}
# for c in comb:
# 	if c[1] not in collect:
# 		collect[c[1]]=[]
# 	collect[c[1]].append(c[0])

# # print(len(collect.keys()))
# for c in collect:
# 	if len(collect[c]) > 1:
# 		print(c,len(collect[c]))
# # print(collect)


# mouse_x, mouse_y = 0,0
# def get_mouse(event,x,y,flags,param):
#     global mouse_x,mouse_y
#     mouse_x = x
#     mouse_y = y

# cv2.namedWindow('im')
# cv2.setMouseCallback('im',get_mouse)


# goodlabel = done
# mislabel = []

# cnt = 0
# for c in collect:
# 	cnt +=1
# 	is_done = False;
# 	for x in collect[c]:
# 		for y in mislabel+goodlabel:
# 			if x == y[0]:
# 				is_done = True
# 				break

# 	if is_done:
# 		print("done",c)
# 		continue
# 	for x in collect[c]:
# 		if cv.imread(x) is None:
# 			print("no img",x)
# 	im = np.hstack([cv.imread(i) for i in collect[c]])
# 	c0 = c
# 	c2 = c
# 	# if c in sc2tc:
# 	# 	c = sc2tc[c]
	
# 	if (len(collect[c]) == 1):
# 		goodlabel.append((collect[c][0],c))
# 		open("new-new-new-labels.txt",'w').write("\n".join(["\t".join(list(x)) for x in goodlabel]))
# 		continue

# 	mlbl= []
# 	glbl = []
# 	cv2.imshow('im',im)

# 	n = 0

# 	print(cnt,'/',len(collect.keys()),'【',c,'】')

	
# 	def calc_n():
# 		global n
# 		n = mouse_x//256
# 		if (n < 0):
# 			n = 0
# 		if (n >= len(collect[c0])):
# 			n = len(collect[c0])-1

# 	while 1:
# 		draw = im.copy()
		
# 		calc_n()
# 		# print(glbl,mlbl)
# 		for i,x in enumerate(collect[c0]):
# 			for m in mlbl:
# 				if x == m[0]:
# 					cv2.rectangle(draw,(i*256,0),(i*256+256,256),(0,0,255),30)
# 			for m in glbl:
# 				if x == m[0]:
# 					cv2.rectangle(draw,(i*256,0),(i*256+256,256),(0,255,0),20)

# 		cv2.imshow('im',draw)
# 		k = cv2.waitKey(0)
# 		if k == ord('1'):
# 			calc_n()
# 			lx = (collect[c0][n],c)
# 			glbl.append(lx)
# 			print("goodlabel",len(glbl),lx)
# 			cv2.imshow('im',draw)
# 		elif k == ord('2'):
# 			calc_n()
# 			lx = (collect[c0][n],c)
# 			mlbl.append(lx)
# 			print("mislabel",len(mlbl),lx)
# 			cv2.imshow('im',draw)
# 		elif k == ord('3'):
# 			calc_n()
# 			c,c2 = c2,c
# 			print("tradswap",c)
# 			cv2.imshow('im',draw)
# 		elif k == ord('4'):
# 			glbl = []
# 			mlbl = []
# 		elif k == ord(' '):
# 			break;
# 		cv2.imshow('im',draw)

# 	for m in mlbl:
# 		if m not in mislabel:
# 			mislabel.append(m)
# 	for m in glbl:
# 		if m not in goodlabel:
# 			goodlabel.append(m)
# 	print(goodlabel)
# 	open("new-new-new-labels.txt",'w').write("\n".join(["\t".join(list(x)) for x in goodlabel]))
# print(collect)

