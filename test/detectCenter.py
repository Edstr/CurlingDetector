__author__ = 'andy.cheung'

import cv2
import numpy as np


# def splitImage():
#
#     img = cv2.imread("../images/emptyHouse.png",0)
#     thresh1 = cv2.threshold(img,160,255,cv2.THRESH_BINARY)[1]
#
#     kernel = np.ones((7,7),np.uint8)
#
#     opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#
#     dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)
#
#     cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#     cv2.imshow('img',img)
#     #cv2.imshow('thresh1',thresh1)
#     #cv2.imshow('opening',opening)
#     #cv2.imshow('dst_rt',dilate)
#     cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
#     cv2.imshow('contour',cv2.bitwise_xor(opening,dilate))
#
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


lower_blue = np.array([110, 50, 50], dtype=np.uint8)
upper_blue = np.array([130,255,255], dtype=np.uint8)

# img = cv2.imread('../images/emptyHouse.png')
# blue,green,red = cv2.split(img)

img = cv2.imread('../images/emptyHouse.png',0)
thresh1 = cv2.threshold(img,160,255,cv2.THRESH_BINARY)[1]
# img = cv2.medianBlur(img,5)


kernel = np.ones((7,7),np.uint8)

opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)

#cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#cv2.imshow('img',img)
#cv2.imshow('thresh1',thresh1)
#cv2.imshow('opening',opening)
#cv2.imshow('dst_rt',dilate)
cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
cv2.imshow('contour',cv2.bitwise_xor(opening,dilate))

cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
# mask = cv2.inRange(cimg, lower_blue, upper_blue)
mask = cv2.bitwise_xor(opening,dilate)

cp = mask.copy()
cv2.imshow('mask',mask)

gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

# Bitwise-AND mask and original image
# res = cv2.bitwise_and(img,img, mask= mask)

# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=16,maxRadius=50)
#circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=25,maxRadius=80)


circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    # # draw the outer circle
    # cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # # draw the center of the circle
    # cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)

print(circles)

#cv2.imshow('detected circles',cimg)
cv2.imshow('contour',mask)
# cv2.imshow('frame',img)
# cv2.imshow('mask',mask)
# cv2.imshow('res',res)

#cv2.namedWindow('canny demo')
#cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
#CannyThreshold(0) # initialization

laplacian = cv2.Laplacian(cimg,cv2.CV_64F)
sobelx = cv2.Sobel(cimg,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(cimg,cv2.CV_64F,0,1,ksize=5)


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

print("Il y a %s cercles" %(len(circles)))

cv2.waitKey(0)
cv2.destroyAllWindows()
