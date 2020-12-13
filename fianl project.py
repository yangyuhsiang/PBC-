import cv2 as cv
import numpy as np
import dlib
import random
from math import hypot


# 讀取剪刀石頭布的圖檔
stone_pic = cv.imread("C:\\Users\\user\\Desktop\\project\\PBC--final-project\\rock.png", cv.IMREAD_UNCHANGED)
predictor_dat = dlib.shape_predictor("C:\\Users\\user\\Desktop\\project\\PBC--final-project\\shape_predictor_68_face_landmarks.dat")


def paper_scissor_stone(stone, predictor):
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    detector = dlib.get_frontal_face_detector()
    while True:
        ret, image = capture.read()
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = detector(gray_image)
        for face in faces:
            landmarks = predictor(gray_image, face)

            # 算你的圖要多大(先用鼻子的大小去算)
            nose_top = (landmarks.part(27).x, landmarks.part(27).y)
            nose_bottom = (landmarks.part(33).x, landmarks.part(33).y)

            pic_high = int(hypot((nose_top[0] - nose_bottom[0]),(nose_top[1] - nose_bottom[1])))
            '''因為每張圖的形狀不同，所以用圖片的比例去做調整'''
            stone_width = int(pic_high * 1.17)

            # 要替換的區域
            stone_bottom = (int(nose_top[0]), int(nose_top[1]))
            stone_top = (int(nose_top[0]), int(nose_top[1] - pic_high))
            stone_left_under_corner = (int(stone_bottom[0]-stone_width/2), int(stone_bottom[1]))
            stone_right_top_corner = (int(stone_top[0]+stone_width/2), int(stone_top[1]))


            # 重新製作石頭的大小
            stone = cv.resize(stone, (pic_high, stone_width))
            stone_gray = cv.cvtColor(stone, cv.COLOR_BGR2GRAY)
            _, stone_mask = cv.threshold(stone_gray, 35, 255, cv.THRESH_BINARY_INV)

            '''不知道為什麼不能局部顯示要放石頭的區域'''
            stone_area = image[stone_left_under_corner[1]:stone_right_top_corner[1],
                               stone_left_under_corner[0]:stone_right_top_corner[0]]
            
            face_no_stone = cv.bitwise_and(stone_area, stone_area, mask = stone_mask)

            final_face = cv.add(face_no_stone, resize_stone)

            image[stone_left_under_corner[1]:stone_right_top_corner[1],
                  stone_left_under_corner[0]:stone_right_top_corner[0]] = final_face
            

        image = cv.flip(image, 1)
        cv.imshow('image', stone_area)
        key = cv.waitKey(50)
        if key == 27:
            break

paper_scissor_stone(stone_pic, predictor_dat)
