from glob import glob
import re
import json


for f in glob("../output/fallback/*.svg"):
	s = open(f,'r').read()

	s = s.replace('width="512.000000pt" height="512.000000pt" viewBox',
		'width="100" height="100" viewBox')

	open(f.replace("fallback","fallback_stage"),'w').write(s)

print("staged")