import numpy as np
import cv2
import pickle

def nothing(*_):
    pass

data = None
with open("david.pdf", "rb") as handle:
      data = pickle.load(handle)
image = data['arr']

# im2,contours,hierarchy = cv.findContours(thresh, 1, 2)
cv2.namedWindow('Frame')
cv2.createTrackbar('threshold_min','Frame',127,255,nothing)
cv2.createTrackbar('threshold_max','Frame',255,255,nothing)
cv2.createTrackbar('blur','Frame',5,25,nothing)
while True:
    t_min = cv2.getTrackbarPos('threshold_min','Frame')
    t_max = cv2.getTrackbarPos('threshold_max','Frame')
    blur = cv2.getTrackbarPos('blur','Frame')
    if not blur % 2:
        blur += 1
    blured_image = cv2.GaussianBlur(image,(blur,blur),0)
    _,thresh_image = cv2.threshold(blured_image,t_min,t_max,0)

    cv2.imshow("Frame", thresh_image)
    cv2.imshow("Frame2", blured_image)

    key = cv2.waitKey(1)
    if key== 27:
      break
