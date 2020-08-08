import os


# lbls = {x.split("\t")[1]:x.split("\t")[0] for x in open("../data/labels_all.txt").read().split("\n") if len(x)}
# care = [x.split("\t") for x in open("../data/bigger.txt").read().split("\n")]

# for m in care:
# 	cmd = "/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/"+lbls[m[0]][:-4]+".bmp"
# 	print(cmd)
# 	os.system(cmd)


# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-1*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-2*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-3*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-4*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-5*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-6*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-7*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-8*.bmp")
# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-9*.bmp")
os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-H*.bmp")

# os.system("/Users/admin/Downloads/potrace-1.16.mac-x86_64/potrace --svg ../output/fine/-H13-255_3941_238_197.bmp")


import stage_svg

print("done")