import cv2
import numpy as np
import math
import operator

# centre de la maison
centerX = 0
centerY = 0

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
    mask = cv2.inRange(cv2.medianBlur(img,5), lower_blue, upper_blue)    # Threshold the HSV image to get only blue colors

    center = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,40,param1=150,param2=15,minRadius=110,maxRadius=120) # maison
    center = np.uint16(np.around(center))
    for i in center[0,:]:
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,255),3)

# get centers of red stones
    cimg_red = cv2.cvtColor(red_stones,cv2.COLOR_RGB2GRAY)
    circles_red = cv2.HoughCircles(cimg_red,cv2.HOUGH_GRADIENT,1,20,param1=150,param2=7,minRadius=20,maxRadius=25) # Red stones
    circles_red = np.uint16(np.around(circles_red))

    for i in circles_red[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,0),3)

    # Draw lines between the center and the red stones
    for i in range(len(circles_red[0])):
        cv2.line(img,(center[0][0][0],center[0][0][1]),(circles_red[0][i][0],circles_red[0][i][1]),(0,0,255),1)
        # cv2.putText(img,str(i+1), (circles_red[0][i][0]+25,circles_red[0][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)

# get centers of yellow stones
    cimg_yellow = cv2.cvtColor(yellow_stones,cv2.COLOR_RGB2GRAY)
    circles_yellow = cv2.HoughCircles(cimg_yellow,cv2.HOUGH_GRADIENT,1,20,param1=150,param2=7,minRadius=20,maxRadius=25) # Yellow Stones
    circles_yellow = np.uint16(np.around(circles_yellow))

    for i in circles_yellow[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,0),3)

    # Draw lines between the center and the yellow stones
    for i in range(len(circles_yellow[0])):
        cv2.line(img,(center[0][0][0],center[0][0][1]),(circles_yellow[0][i][0],circles_yellow[0][i][1]),(0,255,255),1)
        # cv2.putText(img,str(i+1), (circles_yellow[0][i][0]+25,circles_yellow[0][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255),2)


    centerX = center[0,0,0]
    centerY = center[0,0,1]

    print(centerX,centerY)

    # sorted list of stones
    circles_red = sortStone(circles_red)
    circles_yellow = sortStone(circles_yellow)

    circles_all = {}
    circles_all.update(circles_red)
    circles_all.update(circles_yellow)

    print("DEBUG Dico circles_red " , circles_red)
    print("DEBUG Dico circles_yellow " , circles_yellow)
    print("DEBUG Dico circles_all " , circles_all)

    # tmp = {}
    #
    #
    # for i in range(len((circles_red[0,:]))):
    #     # get stone cardinal point
    #     Xstone = circles_red[0,i,0]
    #     Ystone = circles_red[0,i,1]
    #
    #     distance = math.sqrt(math.pow(centerX-Xstone,2)+math.pow(centerY - Ystone,2))
    #     print(i," = [",Xstone,Ystone,"] : ",distance)
    #
    #     tmp[Xstone,Ystone] = distance
    #
    #
    # redStoneDico = sorted(tmp.items(), key=lambda x:x[1])
    #
    # print("DEBUG Dico Stone " , redStoneDico)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def sortStone(circleColorDico):

    tmp = {}

    for i in range(len((circleColorDico[0,:]))):
        # get stone cardinal point
        Xstone = circleColorDico[0,i,0]
        Ystone = circleColorDico[0,i,1]

        distance = math.sqrt(math.pow(centerX-Xstone,2)+math.pow(centerY - Ystone,2))
        print(i," = [",Xstone,Ystone,"] : ",distance)

        tmp[Xstone,Ystone] = distance


    circleColorDico = sorted(tmp.items(), key=lambda x:x[1])

    return circleColorDico

def main():
    splitImage()

if __name__ == '__main__':
    main()
