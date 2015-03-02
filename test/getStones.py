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

    thresh1 = cv2.threshold(res,127,255,cv2.THRESH_TOZERO)[1]
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_CROSS, kernel)
    dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)
    var = cv2.bitwise_or(opening,dilate)

    img2 = cv2.cvtColor(var,cv2.COLOR_HSV2RGB_FULL)
    img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)

    cv2.imshow('img',img)
    cv2.imshow('Stones',img2)

    # Circle detector

    img3 = cv2.medianBlur(img2,5)
    cimg = cv2.cvtColor(img3,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img3,cv.CV_HOUGH_GRADIENT,1,20,param1=200,param2=30,minRadius=5,maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',cimg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    splitImage()

if __name__ == '__main__':
    main()
