import cv2
cv = cv2
from glob import glob
import numpy as np
import random

# PAGE_COLS = 8
# PAGE_ROWS = 19
PAGE_COLS = 9
PAGE_ROWS = 20

def f2t(f):
    return "../data/rects/"+f.split(" ")[1].split(".")[0]+".tsv"

# files = glob("../pages/李长吉歌诗.4卷.外诗集1卷.李贺撰.刘辰翁评.明末凌濛初刊闵氏朱墨套印本 11.png")

files = glob("../pages/*.png")
done = glob("../data/rects/*.tsv")
print(files)
print(done)
files = [f for f in files if f2t(f) not in done]
print(len(files))

def generate_grid(x0,y0,x1,y1,x2,y2,x3,y3):
    cols = PAGE_COLS
    rows = PAGE_ROWS

    w = (x1-x0)/cols
    h = (y2-y0)/rows

    R = []
    
    for i in range(rows):
        s = i/rows
        for j in range(cols):
            t = 0.01+(j/cols)*0.98
            # t=(j/cols)
            xtop = x0*(1-t)+x1*t
            ytop = y0*(1-t)+y1*t

            xbot = x3*(1-t)+x2*t
            ybot = y3*(1-t)+y2*t

            x = xtop*(1-s)+xbot*s
            y = ytop*(1-s)+ybot*s

            R.append([x+w*0.1,y,w*0.8,h])
    return R

mouse_x, mouse_y = 0,0
def get_mouse(event,x,y,flags,param):
    global mouse_x,mouse_y
    mouse_x = x
    mouse_y = y

cv2.namedWindow('im')
cv2.setMouseCallback('im',get_mouse)

print(len(files))
files.sort(key= lambda x: int(x.split(" ")[1].split(".")[0][1:]))
for f in files:
    print(files.index(f),'/',len(files),f)
    im = cv2.imread(f);
    im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)

    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    x3 = 0
    y3 = 0

    x4 = 0
    y4 = 0
    x5 = 0
    y5 = 0
    x6 = 0
    y6 = 0
    x7 = 0
    y7 = 0

    R1,R2 = [],[]

    cv2.imshow("im",im)

    while 1:
        drawing = np.copy(im)
        

        k = cv2.waitKey(0)

        if k == ord('1'):
            x0 = mouse_x
            y0 = mouse_y

        elif k == ord('2'):
            x1 = mouse_x
            y1 = mouse_y

        elif k == ord('3'):
            x2 = mouse_x
            y2 = mouse_y

        elif k == ord('4'):
            x3 = mouse_x
            y3 = mouse_y

        elif k == ord('5'):
            x4 = mouse_x
            y4 = mouse_y

        elif k == ord('6'):
            x5 = mouse_x
            y5 = mouse_y

        elif k == ord('7'):
            x6 = mouse_x
            y6 = mouse_y

        elif k == ord('8'):
            x7 = mouse_x
            y7 = mouse_y

        elif k == ord(' '):
            break

        elif k == ord('t'):
            x0 = 0
            y0 = 0
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 0
            x3 = 0
            y3 = 0
            o0 = 0
            o1 = 0
            m0 = 0
            m1 = 0

        print(x0,y0,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7)

        # R = generate_grid(251,1001,2635,3812)
        R1 = generate_grid(x0,y0,x1,y1,x2,y2,x3,y3)
        R2 = generate_grid(x4,y4,x5,y5,x6,y6,x7,y7)

        for r in R1:
            cv.rectangle(drawing, (int(r[0]),int(r[1])), (int(r[0]+r[2]),int(r[1]+r[3])), (0,255,255), 4)

        for r in R2:
            cv.rectangle(drawing, (int(r[0]),int(r[1])), (int(r[0]+r[2]),int(r[1]+r[3])), (255,255,0), 4)

        cv.circle(drawing, (int(x0),int(y0)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x1),int(y1)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x2),int(y2)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x3),int(y3)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x4),int(y4)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x5),int(y5)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x6),int(y6)), 20, (0,0,255), 5)
        cv.circle(drawing, (int(x7),int(y7)), 20, (0,0,255), 5)

        cv2.imshow("im",drawing)

    R = []
    if x0 != 0:
        R += R1
    if x2 != 0:
        R += R2

    open(f2t(f),'w').write("\n".join(["\t".join([str(int(y*2)) for y in x]) for x in (R1+R2)]))

