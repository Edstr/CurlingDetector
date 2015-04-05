import cv2
import numpy as np
import math
import operator



def splitImage():
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_red = np.array([130, 50, 50], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    house = cv2.imread("../images/emptyHouse2.png")
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

    # Circle detector
    cimg = cv2.cvtColor(var,cv2.COLOR_RGB2GRAY)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(cv2.medianBlur(img,5), lower_blue, upper_blue)


    center = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,40,param1=150,param2=15,minRadius=110,maxRadius=120) # maison
    center = np.uint16(np.around(center))
    for i in center[0,:]:
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,255),3)

    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,param1=150,param2=7,minRadius=20,maxRadius=25) # Pierres
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,0),3)

    cv2.line(img, (center[0][0][0],center[0][0][1]),(circles[0][1][0],circles[0][1][1]),(0,0,255),2,2)
    cv2.imshow('Detected stones',img)

    centerX = center[0,0,0]
    centerY = center[0,0,1]

    print(centerX,centerY)

    #
    meinenBeauStones = {}

    for i in range(len((circles[0,:]))):

        Xstone = circles[0,i,0]
        Ystone = circles[0,i,1]

        distance = math.sqrt(math.pow(centerX-Xstone,2)+math.pow(centerY - Ystone,2))

        print(i," = [",Xstone,Ystone,"] : ",distance)

        meinenBeauStones[Xstone,Ystone] = distance

    sortedStones = sorted(meinenBeauStones.items(), key=lambda x:x[1])

    print("DEBUG Dico Stone " , sortedStones)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    splitImage()

if __name__ == '__main__':
    main()
