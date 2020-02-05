import os
from glob import glob

fs = glob("../output/fallback/*.bmp")
for f in fs:
	print(f)
	os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg "+f)

import stage_svg

print("done")