import cv2
import numpy as np

def splitImage():
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)

    img = cv2.imread("../images/emptyHouse2.png",0)
    thresh1 = cv2.threshold(img,160,255,cv2.THRESH_BINARY)[1]

    kernel = np.ones((7,7),np.uint8)
    
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

    dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img',img)
    #cv2.imshow('thresh1',thresh1)
    #cv2.imshow('opening',opening)
    #cv2.imshow('dst_rt',dilate)
    cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
    cv2.imshow('contour',cv2.bitwise_xor(opening,dilate))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    splitImage()

if __name__ == '__main__':
    main()
