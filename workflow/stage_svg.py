from glob import glob
import re

for f in glob("../output/fine/*.svg"):
	s = open(f,'r').read()
# 	s = s.replace('width="512.000000pt" height="512.000000pt" viewBox="0 0 512.000000 512.000000"\
# \n preserveAspectRatio="xMidYMid meet"',
# 		'width="100" height="100" viewBox="-256 -256 1024 1024"')

	s = s.replace('width="512.000000pt" height="512.000000pt" viewBox',
		'width="100" height="100" viewBox')
	# s = re.sub(r"(\d+?)([ \nz])",r"0.\1\2",s)
	open(f.replace("fine","stage"),'w').write(s)


print("staged")