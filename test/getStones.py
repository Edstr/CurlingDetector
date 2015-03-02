import cv2
import numpy as np

def splitImage():
    lower_blue = np.array([110, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_red = np.array([130, 50, 50], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    img = cv2.imread("../images/curling1.png")

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(hsv_img, lower_red, upper_red)
    frame_threshed += cv2.inRange(hsv_img, lower_yellow, upper_yellow)

    res = cv2.bitwise_and(img,img, mask= frame_threshed)

    cv2.imshow('img',img)
    cv2.imshow('Stones',res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    splitImage()

if __name__ == '__main__':
    main()
