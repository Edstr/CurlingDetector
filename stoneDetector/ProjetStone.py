import cv2
import numpy as np
import math

TEAM1 = "Red"
TEAM2 = "Yellow"
path_image = ""

def splitImage():
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_red = np.array([130, 50, 50], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    global path_image
    #house = cv2.imread("../images/emptyHouse.png")
    #img = cv2.imread("../images/curling2.png")
    img = cv2.imread(path_image)

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
        # text
        #cv2.putText(img,str((circles_red[0][i][0],circles_red[0][i][1])), (circles_red[0][i][0]+25,circles_red[0][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),1)

# get centers of yellow stones
    cimg_yellow = cv2.cvtColor(yellow_stones,cv2.COLOR_RGB2GRAY)
    circles_yellow = cv2.HoughCircles(cimg_yellow,cv2.HOUGH_GRADIENT,1,20,param1=150,param2=7,minRadius=20,maxRadius=25) # Yellow Stones
    circles_yellow = np.uint16(np.around(circles_yellow))

    for i in circles_yellow[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(255,0,255),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),1,(0,0,0),3)

    #Draw lines between the center and the yellow stones
    for i in range(len(circles_yellow[0])):
        cv2.line(img,(center[0][0][0],center[0][0][1]),(circles_yellow[0][i][0],circles_yellow[0][i][1]),(0,255,255),1)
        # text
        #cv2.putText(img,str((circles_yellow[0][i][0],circles_yellow[0][i][1])), (circles_yellow[0][i][0]+25,circles_yellow[0][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0),1)

    centerX = center[0,0,0]
    centerY = center[0,0,1]

    print(centerX,centerY)
    print(circles_red)


    # sorted list of stones
    circles_red = sortStone(circles_red,centerX,centerY)
    circles_yellow = sortStone(circles_yellow,centerX,centerY)

    tmp = {}
    tmp.update(circles_red)
    tmp.update(circles_yellow)

    circles_all = sorted(tmp.items(), key=lambda x:x[1])

    print("DEBUG Dico circles_red " , circles_red)
    print("DEBUG Dico circles_yellow " , circles_yellow)
    print("DEBUG Dico circles_all " , circles_all)

    point = 0
    z = 1
    last = None
    isStop = True

    global TEAM1
    global TEAM2

    for i in circles_all:
        if i in circles_red:
            if((last == None or last == TEAM1) and isStop == True):
                last = TEAM1
                point += 1
            else:
                isStop = False

            cv2.putText(img,str(int(z)), (int(i[0][0])+25,int(i[0][1])), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)

        else:
            if((last == None or last == TEAM2) and isStop == True):
                last = TEAM2
                point += 1
            else:
                isStop = False

            cv2.putText(img,str(int(z)), (int(i[0][0])+25,int(i[0][1])), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255),2)
        z+=1

    txt = '%s is the winner with %s point(s)'%(last,point)

    cv2.putText(img,str(txt), (0+25,0+25), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0),2)

    cv2.imshow('Detected stones',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#
def sortStone(circleColorDico,centerX,centerY):


    tmp = {}

    for i in range(len((circleColorDico[0,:]))):
        # get stone cardinal point
        Xstone = float(circleColorDico[0,i,0])
        Ystone = float(circleColorDico[0,i,1])

        #print( (Xstone-centerX)*(Xstone-centerX))
        # x = (0 - Xstone - centerX ) * (0 - Xstone - centerX)
        # y = (0 - Ystone - centerY ) * (0 - Ystone - centerY)

        x = (Xstone - centerX ) * (Xstone - centerX)
        y = (Ystone - centerY ) * (Ystone - centerY)

        distance = math.sqrt(float(x)+float(y))
        print(i," = [",Xstone,Ystone,"] : ",distance)

        tmp[Xstone,Ystone] = distance

    circleColorDico = sorted(tmp.items(), key=lambda x:x[1])

    return circleColorDico

def main():
    splitImage()

if __name__ == '__main__':
    import sys

    global path_image
    path_image = str(sys.argv[1])

    main()


