import cv2
import cv2.cv as cv
import numpy as np

def splitImage():
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_red = np.array([130, 50, 50], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    img = cv2.imread("../images/curling2.png")
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    frame_threshed = cv2.inRange(hsv_img, lower_red, upper_red)
    frame_threshed += cv2.inRange(hsv_img, lower_yellow, upper_yellow)

    res = cv2.bitwise_and(img,img, mask= frame_threshed)

    thresh1 = cv2.threshold(res,127,255,cv2.THRESH_BINARY)[1]
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    dilate = cv2.morphologyEx(opening, cv2.MORPH_GRADIENT, kernel)
    dilate = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)

    var = cv2.bitwise_or(opening,dilate)

    #img2 = cv2.cvtColor(var,cv2.COLOR_RGB2GRAY)
    #img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)

    cv2.imshow('img',img)
    cv2.imshow('Stones',var)
    # cv2.imshow('Stones',img2)

    # Circle detector

    cimg = cv2.cvtColor(var,cv2.COLOR_RGB2GRAY)

    circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,20,param1=130,param2=7,minRadius=20,maxRadius=30)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(127,127,0),3)

    cimg = cv2.cvtColor(cimg,cv2.COLOR_GRAY2RGBA)
    cv2.imshow('detected circles',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    splitImage()

if __name__ == '__main__':
    main()
