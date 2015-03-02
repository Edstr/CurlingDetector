__author__ = 'andy.cheung'

import cv2
import numpy as np

img = cv2.imread("../images/curling1 - Copie.png",0)
#img = cv2.imread("../images/curling3.png",0)
thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)[1]

kernel = np.ones((4,4),np.uint8)

opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img',img)
#cv2.imshow('thresh1',thresh1)
#cv2.imshow('opening',opening)
#cv2.imshow('dst_rt',dilate)

var = cv2.bitwise_xor(opening,dilate)

cv2.namedWindow('contour', cv2.WINDOW_NORMAL)

#cv2.imshow('contour',var)
#cv2.waitKey(0)

# img = cv2.imread('../images/curling1.png',0)
# img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(var,cv2.COLOR_GRAY2BGR)

#circles = cv2.HoughCircles(var,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
circles = cv2.HoughCircles(var,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=16,maxRadius=50)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# img = cv2.imread('../images/curling1.png')
#
# b,g,r = cv2.split(img)
#
# kernel = np.ones((5,5),np.uint8)
# erosion = cv2.erode(img,kernel,iterations = 1)
#
# b = cv2.medianBlur(b,5)
# ret,thresh2 = cv2.threshold(b,127,255,cv2.THRESH_BINARY_INV)
# b = cv2.bitwise_not(b)
#
# cv2.imshow("origin",img)
# #cv2.imshow("r",r)
# #cv2.imshow("g",g)
# cv2.imshow("b",b)

cv2.waitKey(0)
cv2.destroyAllWindows()
