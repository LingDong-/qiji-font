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

def generate_grid(x,y,w,h,o,m):
    cols = PAGE_COLS
    rows = PAGE_ROWS
    u = w/cols
    v = h/rows
    px = 0.02 * w
    py = 0 * h
    R = []
    oo = 0
    
    for i in range(rows):
        mm = 0
        for j in range(cols):
            rx = x + u * j + px + oo
            ry = y + v * i + py + mm
            rw = u - 2 * px
            rh = v - 2 * py
            R.append([rx,ry,rw,rh])
            mm += m
        oo += o
        
    return R

mouse_x, mouse_y = 0,0
def get_mouse(event,x,y,flags,param):
    global mouse_x,mouse_y
    mouse_x = x
    mouse_y = y

cv2.namedWindow('im')
cv2.setMouseCallback('im',get_mouse)

print(len(files))
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
    o0 = 0
    o1 = 0
    m0 = 0
    m1 = 0
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

        elif k == ord('q'):
            o0 -=0.2
        elif k == ord('w'):
            o0 +=0.2
        elif k == ord('e'):
            o1 -=0.2
        elif k == ord('r'):
            o1 +=0.2

        elif k == ord('a'):
            m0 -=0.2
        elif k == ord('s'):
            m0 +=0.2
        elif k == ord('d'):
            m1 -=0.2
        elif k == ord('f'):
            m1 +=0.2


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

        print(x0,y0,x1,y1,x2,y2,x3,y3 )

        # R = generate_grid(251,1001,2635,3812)
        R1 = generate_grid(x0,y0,x1-x0,y1-y0,o0,m0)
        R2 = generate_grid(x2,y2,x3-x2,y3-y2,o1,m1)

        for r in R1:
            cv.rectangle(drawing, (int(r[0]),int(r[1])), (int(r[0]+r[2]),int(r[1]+r[3])), (0,255,255), 4)

        for r in R2:
            cv.rectangle(drawing, (int(r[0]),int(r[1])), (int(r[0]+r[2]),int(r[1]+r[3])), (255,255,0), 4)

        cv.rectangle(drawing, (int(x0),int(y0)), (int(x1),int(y1)), (0,0,255), 2)
        cv.rectangle(drawing, (int(x2),int(y2)), (int(x3),int(y3)), (0,0,255), 2)

        cv2.imshow("im",drawing)

    R = []
    if x0 != 0:
        R += R1
    if x2 != 0:
        R += R2

    open(f2t(f),'w').write("\n".join(["\t".join([str(int(y*2)) for y in x]) for x in (R1+R2)]))

