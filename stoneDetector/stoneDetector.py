__author__ = 'andy.cheung'

import cv2
import cv2.cv as cv
import numpy as np

img = cv2.imread('../images/curling2.png',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20,param1=200,param2=30,minRadius=40,maxRadius=101)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()

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

