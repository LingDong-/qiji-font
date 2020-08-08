from glob import glob
import re
import json

tweak = json.loads(open("../data/svg_tweak.json",'r').read())

n = 0
t = 0
for f in glob("../output/fine/*.svg"):
	bname = f.split("/")[-1]
	try:
		t += tweak[bname]['scale']
	except:
		t += 1
	n+=1

avgsc = int((1/(t/n))*10000)/10000


for f in glob("../output/fine/*.svg"):
	bname = f.split("/")[-1]
	try:
		t = tweak[bname]
	except:
		t = {'x':0,'y':0,'scale':1,'rotate':0}
	gstr = f'<g transform="translate(256,256) translate({t["x"]},{t["y"]}) scale({t["scale"]*avgsc}) rotate({t["rotate"]}) translate(-256,-256)">'

	s = open(f,'r').read()
# 	s = s.replace('width="512.000000pt" height="512.000000pt" viewBox="0 0 512.000000 512.000000"\
# \n preserveAspectRatio="xMidYMid meet"',
# 		'width="100" height="100" viewBox="-256 -256 1024 1024"')

	s = s.replace('width="512.000000pt" height="512.000000pt" viewBox',
		'width="100" height="100" viewBox').replace("</metadata>",
		"(modified)</metadata>"+gstr).replace("</svg>","</g></svg>")

	# s = re.sub(r"(\d+?)([ \nz])",r"0.\1\2",s)
	open(f.replace("fine","stage"),'w').write(s)


print("staged")