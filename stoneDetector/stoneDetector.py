__author__ = 'andy.cheung'

import cv2
import numpy as np


def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(img,(3,3),0)
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges) # just add some colours to edges from original image.
    cv2.imshow('canny demo',dst)

lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3


img = cv2.imread('../images/curling1 - Copie.png')
blue,green,red = cv2.split(img)

img = cv2.imread('../images/curling1 - Copie.png',0)
img = cv2.medianBlur(img,5)

cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(cimg, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(img,img, mask= mask)

#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=16,maxRadius=50)


circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


cv2.imshow('detected circles',cimg)

cv2.imshow('frame',img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

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
