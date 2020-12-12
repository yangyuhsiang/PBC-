import cv2 as cv
import numpy as np
import dlib
from math import hypot

cap = cv.VideoCapture(0)

nose_image = cv.imread("C:\\Users\\user\\Desktop\\project\\PngItem_4084291.png")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\\Users\\user\\Desktop\\project\\shape_predictor_68_face_landmarks.dat")

while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    faces = detector(gray_frame)
    for face in faces:
        landmarks = predictor(gray_frame, face)  # 不懂，去查
        
        # 找到圖像中，nose的位置
        top_nose = (landmarks.part(29).x, landmarks.part(29).y)
        center_nose = (landmarks.part(33).x, landmarks.part(33).y)
        left_nose = (landmarks.part(31).x, landmarks.part(31).y)
        right_nose = (landmarks.part(35).x, landmarks.part(35).y)
        
        # cv.circle(frame, top_nose, 3, (0,255,0), -1)#(name, position, radius, color, thickness)
        
        # 處理豬鼻子，計算豬鼻子要縮成的大小
        nose_width = hypot(right_nose[0] - left_nose[0],
                               right_nose[1] - left_nose[1])*1.3  # 這是要處理豬鼻子的像素，所以不會有小數
        nose_hight = nose_width * 0.78  # 要用等比例的處理，不然可能看起來怪怪的


        # new nose position，建立一個新的影像只存在於rectangle之中
        bottom_left = (int(center_nose[0] - nose_width/2),int(center_nose[1] - nose_hight/2))
        #top_right = (int(center_nose[0] + nose_width/2),int(center_nose[1] + nose_hight/2))
        #cv.rectangle(frame, bottom_left, top_right, (0,0,255), 3)
        
        nose_width = int(nose_width)
        nose_hight = int(nose_hight)
        
        # create new nose
        nose_pig = cv.resize(nose_image, (nose_width, nose_hight))
        nose_pig_gray = cv.cvtColor(nose_pig,  cv.COLOR_BGR2GRAY)
        _, nose_mask = cv.threshold(nose_pig_gray, 35, 230, cv.THRESH_BINARY_INV)
                # pixel的value低於35的時候就變成白色，其他就是黑色
        
        nose_area = frame[bottom_left[1] : bottom_left[1] + nose_hight,  # row is y axis
                          bottom_left[0] : bottom_left[0] + nose_width]
            # 把mask的部分裝在我的鼻子上
        nose_area_no_nose = cv.bitwise_and(nose_area, nose_area, mask=nose_mask)

        final_nose = cv.add(nose_area_no_nose, nose_pig)  # 把兩張圖和一起
        
        frame[bottom_left[1] : bottom_left[1] + nose_hight,
                          bottom_left[0] : bottom_left[0] + nose_width] = final_nose

    #cv.imshow('nose area', nose_area)    
    cv.imshow('Frame', frame)
    #cv.imshow('nose pig', nose_pig)
    #cv.imshow('nose_mask', nose_mask)
    
    key = cv.waitKey(1)
    if key == 27:
        break
    
