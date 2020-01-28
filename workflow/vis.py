# -*- coding: utf-8 -*-
import cv2
cv = cv2
import numpy as np

labels = [x.split("\t") for x in open("../data/labels.txt",'r').read().split("\n")]
labels.sort(key=lambda x:x[1])

mapper = {x[1]:x[0] for x in labels}

# im = np.vstack([np.hstack([cv2.resize(cv.imread(x[0].replace('rend','xrend')),(64,64),cv2.INTER_AREA) for x in labels[i:i+50]]) for i in range(0,2500,50)])
# cv2.imshow('',im)
# cv2.waitKey(0)

txt = "秋風吹地百草乾華容碧影生晚寒我當二十不得意一心愁謝如枯蘭衣如飛鶉馬如狗臨歧擊劍生銅吼旗亭下馬解秋衣請貰宜陽一壺酒壺中喚天雲不開白晝萬里閑淒迷主人勸我養心骨莫受俗物相填豗"
txt += "越羅衫袂迎春風玉刻麒麟腰帶紅樓頭曲宴仙人語帳底吹笙香霧濃人間酒暖春茫茫花枝入簾白日長飛窗復道傳籌飲十夜銅盤膩燭黃禿衿小袖調鸚鵡紫繡麻鞋踏哮虎斫桂燒金待曉筵白鹿青蘇夜半煮桐英永巷騎新馬內屋深屏生色畫開門爛用水衡錢卷起黃河向身瀉皇天厄運猶曾裂秦宮一生花底活鸞篦奪得不還人醉睡氍毹滿堂月"
txt += "北虜膠堪折秋沙亂曉鼙髯鬍頻犯塞驕氣似橫霓灞水樓船渡營門細柳開將軍馳白馬豪彥騁雄材箭射欃槍落旗懸日月低榆稀山易見甲重馬頻嘶天遠星光沒沙平草葉齊風吹雲路火雪汙玉關泥屢斷呼韓頸曾然董卓臍太常猶舊寵光祿是新隮寳玦麒麟起銀壺狒狖啼桃花連馬發綵絮撲鞍來呵臂懸金斗當脣注玉罍清蘇和碎蟻紫膩卷浮杯虎鞹先蒙馬魚腸且斷犀䟃𧽼西旅狗蹙額北方奚守帳然香暮看鷹永夜棲黃龍就別鏡青塚念陽臺周處長橋役侯調短弄哀錢塘階鳳羽正室擘鸞釵內子攀琪樹羌兒奏落梅今朝擎劍去何日刺蛟廻"

for www in range(1):

	w = 128
	ww = 100
	W = ww*20

	c = 0
	r = 0
	im = np.zeros((W,W*2),np.float32)
	for p in txt:
		if p not in mapper:
			print(p)
			continue
		# _,iid,bstr = mapper[p].split("/")[-1].split(".")[0].split("-")
		# x,y,_w,_h=[int(a) for a in bstr.split("_")]
		# a = cv2.imread("pages/李长吉歌诗.4卷.外诗集1卷.李贺撰.刘辰翁评.明末凌濛初刊闵氏朱墨套印本 "+iid+".png",0)[y:y+_h,x:x+_w]


		a = 1-cv2.imread("../output/fine/"+mapper[p].replace(".png",".bmp"),0).astype(np.float32)/255

		# a = cv2.dilate(a,np.array([[0,0,0,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,0,0,0]],np.uint8),iterations = 5)
		# a = cv2.dilate(a,np.array([[0,0,1,0,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,0,1,0,0]],np.uint8),iterations = 1)
		# a = cv2.dilate(a,np.array([[0,1,0],[0,1,0],[0,1,0]],np.uint8),iterations = 1)
		# a = cv2.erode(a,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations = 5)
		# a = cv2.erode(a,np.array([[0,0,0,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,0,0,0]],np.uint8),iterations = 2)

		a = cv2.resize(a,(w,w),interpolation = cv2.INTER_AREA)

		# cv2.imshow('',a);
		# cv2.waitKey(0)

		# print(p,a.shape)
		try:
			im[r*ww:r*ww+w,int(im.shape[1]-c*w-w):int(im.shape[1]-c*w)]+=a
		except:
			pass
		# cv2.imshow('',im)
		# cv2.waitKey(0)
		r += 1
		if (r+1)*ww >= W:
			r = 0
			c += 1.3
			try:
				pass
				# im[:,im.shape[1]-int(c*w)+10:im.shape[1]-int(c*w)+12]=1
			except:
				pass
			if c*w >= im.shape[1]:
				break

	im = (255*im).astype(np.uint8)

	# im = cv2.dilate(im,np.array([[0,0,0,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,0,0,0]],np.uint8),iterations = 1)
	# im = cv2.dilate(im,np.array([[0,0,1,0,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,0,1,0,0]],np.uint8),iterations = 1)
	# im = cv2.dilate(im,np.array([[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]],np.uint8),iterations = 1)


	cv2.imshow('',255-im)
	cv2.waitKey(0)

	cv2.imwrite("tmp/vis.png",255-im)


#-72-5166_952_222_207