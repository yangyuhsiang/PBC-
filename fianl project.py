import cv2 as cv
import numpy as np
import dlib
import random
from math import hypot


stone = cv.imread('C:\\Users\\user\\Desktop\\rock.png', cv.IMREAD_UNCHANGED)
capture = cv.VideoCapture(0, cv.CAP_DSHOW)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\\Users\\user\\Desktop\\project\\PBC--final-project\\shape_predictor_68_face_landmarks.dat")

while True:
    ret, image = capture.read()
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = detector(gray_image, 0)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()            

        width = int(x2 - x1)
        high = int(y2 - y1)
            
        w1 = width//2
        h1 = high//2
            
        w2 = width//4
        h2 = high//4

        resize_stone = cv.resize(stone, (w1, h1))
        stone_mask_bgr = resize_stone[:, :, :3]
        stone_alpha_ch = resize_stone[:, :, 3]
        _, stone_mask = cv.threshold(stone_alpha_ch, 220, 255, cv.THRESH_BINARY)


            
        stone_area_no_face = cv.bitwise_not(stone_mask)
        stone_area = image[y1-h2:y1+h1-h2, x1+w2:x1+w1+w2]

        stone_part = cv.bitwise_and(stone_mask_bgr, stone_mask_bgr, mask=stone_mask)
        face_part = cv.bitwise_and(stone_area, stone_area, mask=stone_area_no_face)
            
        final_stone = cv.add(face_part, stone_part)
        image[y1-h2:y1+h1-h2, x1+w2:x1+w1+w2] = final_stone
            
        image = cv.flip(image, 1)
        cv.imshow('stone_mask', image)
    key = cv.waitKey(50)
    if key == 27:
        break
