import cv2
import cv2.cv as cv
import numpy as np

def splitImage():
    # colors range
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_green = np.array([50, 50, 50], dtype=np.uint8)
    upper_green = np.array([110,255,255], dtype=np.uint8)
    lower_red = np.array([130, 50, 50], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    img = cv2.imread("../images/emptyHouse2.png")

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    frame_threshed_red = cv2.inRange(hsv_img, lower_red, upper_red)
    frame_threshed_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

    kernel = np.ones((3,3),np.uint8)

    # get red stones
    res_red = cv2.bitwise_and(img,img, mask= frame_threshed_red)
    thresh_red = cv2.threshold(res_red,127,255,cv2.THRESH_BINARY)[1]
    opening = cv2.morphologyEx(thresh_red, cv2.MORPH_OPEN, kernel)
    dilate = cv2.morphologyEx(opening, cv2.MORPH_GRADIENT, kernel)
    dilate = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    red_stones = cv2.bitwise_or(opening,dilate)

    # get yellow stones
    res_yellow= cv2.bitwise_and(img,img, mask= frame_threshed_yellow)
    thresh_yellow = cv2.threshold(res_yellow,127,255,cv2.THRESH_BINARY)[1]
    opening = cv2.morphologyEx(thresh_yellow, cv2.MORPH_OPEN, kernel)
    dilate = cv2.morphologyEx(opening, cv2.MORPH_GRADIENT, kernel)
    dilate = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    yellow_stones = cv2.bitwise_or(opening,dilate)

# get center of the house
    mask = cv2.inRange(cv2.medianBlur(img,5), lower_green, upper_green)    # Threshold the HSV image to get only green colors
    cv2.imshow('mask',mask)
    center = cv2.HoughCircles(mask,cv.CV_HOUGH_GRADIENT,1,1,param1=10,param2=1,minRadius=0,maxRadius=500) # maison
    # center = np.uint16(np.around(center))
    # for i in center[0,:]:
    #     cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
    #     # draw the center of the circle
    #     cv2.circle(img,(i[0],i[1]),1,(0,0,255),3)
    #
    #
    # cv2.imshow('Detected stones',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    splitImage()

if __name__ == '__main__':
    main()
