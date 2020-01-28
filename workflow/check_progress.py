from glob import glob
import json

ocr_ret = [y.split("\t") for y in ("\n".join([open(x,'r').read() for x in glob("../tmp/ocr_ret*.txt")])).split("\n") if len(y)]

tc2sc = json.loads(open("../data/TC2SC.json",'r').read())
sc2tc = {}
for k in tc2sc:
	sc2tc[tc2sc[k]]=k

new = list(set([(sc2tc[x[1][0]] if x[1][0] in sc2tc else x[1][0]) for x in ocr_ret if len(x[1])]))

old = [x.split("\t")[1] for x in open("../data/labels.txt",'r').read().split("\n") if len(x)]

add = [x for x in new if x not in old]

print(add,len(add))