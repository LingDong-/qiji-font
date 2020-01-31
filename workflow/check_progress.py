from glob import glob
import json

# odd = {x.split("\t")[0]:x.split("\t")[1] for x in open("../data/variant_map.txt",'r').read().split("\n")}
# def uni(s):
# 	t = ""
# 	for x in s:
# 		if x in odd:
# 			t += odd[x]
# 		else:
# 			t += x
# 	return t

# ocr_ret = [y.split("\t") for y in ("\n".join([open(x,'r').read() for x in glob("../tmp/ocr_ret*.txt")])).split("\n") if len(y)]
# hnz = list(set(open('../data/labels_hnz_raw.txt','r').read()))


# tc2sc = json.loads(open("../data/TC2SC.json",'r').read())
# sc2tc = {}
# for k in tc2sc:
	# sc2tc[tc2sc[k]]=k

# new = list(set([(sc2tc[x[1][0]] if x[1][0] in sc2tc else x[1][0]) for x in ocr_ret if len(x[1])]))

old = [x.split("\t")[1] for x in open("../data/labels_all.txt",'r').read().split("\n") if len(x)]

# add = [x for x in new if x not in old]

# addhnz = [x for x in hnz if x not in old]

# print(add,len(add))

# print(addhnz,len(addhnz))

# unionhnz = addhnz+old


corp = "".join([open(x,'r').read() for x in glob("../../wenyan-book/*.md")])
scorp = "".join(sorted(list(set([x for x in list(corp) if 0x4e00 < ord(x) < 0x9fff]))))

chuci = list(set(open("../../../Downloads/chuci.txt",'r').read()))

common = set(open("../data/common4808.txt",'r').read())

lack = [x for x in scorp if x not in old and x not in chuci]
print(lack,len(lack))

print(len(old))

lackc = [x for x in scorp if x not in old]
print("".join(lackc),len(lackc))