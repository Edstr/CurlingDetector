__author__ = 'andy.cheung'

import cv2
import numpy as np


#img = cv2.imread("../images/emptyHouse.png",0)
img = cv2.imread("../images/curling2.png",0)

#cv2.imshow('origine',img)

thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)[1]
kernel = np.ones((4,4),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)

#cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#cv2.imshow('img',img)

var = cv2.bitwise_xor(opening,dilate)
#cv2.namedWindow('contour', cv2.WINDOW_NORMAL)

cimg = cv2.cvtColor(var,cv2.COLOR_GRAY2BGR)

#circles = cv2.HoughCircles(var,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=16,maxRadius=50)
# circles = cv2.HoughCircles(var,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=16,maxRadius=50)
center = cv2.HoughCircles(var, cv2.HOUGH_GRADIENT,1,20,param1=40,param2=30,minRadius=60,maxRadius=250)

print("center")
print(center)

#circles = np.uint16(np.around(circles))
center = np.uint16(np.around(center))

# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

for i in center[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


cv2.imshow('detected circles',cimg)

cv2.waitKey(0)
cv2.destroyAllWindows()