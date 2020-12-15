import cv2 as cv
import numpy as np
import dlib
import random
from math import hypot

stone = cv.imread('C:\\Users\\user\\Desktop\\rock.png', cv.IMREAD_UNCHANGED)
paper = cv.imread('C:\\Users\\user\\Desktop\\paper.png', cv.IMREAD_UNCHANGED)
scissor = cv.imread('C:\\Users\\user\\Desktop\\scissor.png', cv.IMREAD_UNCHANGED)

capture = cv.VideoCapture(0, cv.CAP_DSHOW)
detector = dlib.get_frontal_face_detector()


# stone 的大小調整，還有遮罩的函數
def stone_change(stone, w1, h1):
    resize_stone = cv.resize(stone, (w1, h1))
    stone_mask_bgr = resize_stone[:, :, :3]
    stone_alpha_ch = resize_stone[:, :, 3]
    _, pic_mask = cv.threshold(stone_alpha_ch, 220, 255, cv.THRESH_BINARY)
    pic_part = cv.bitwise_and(stone_mask_bgr, stone_mask_bgr, mask=pic_mask)
    return pic_mask, pic_part


# paper的大小調整函數，還有遮罩的函數
def paper_change(paper, w1, h1):
    resize_paper = cv.resize(paper, (w1, h1))
    paper_mask_bgr = resize_paper[:, :, :3]
    paper_alpha_ch = resize_paper[:, :, 3]
    _, pic_mask = cv.threshold(paper_alpha_ch, 220, 255, cv.THRESH_BINARY)
    pic_part = cv.bitwise_and(paper_mask_bgr, paper_mask_bgr, mask=pic_mask)
    return pic_mask, pic_part


# 剪刀的大小調整函數，還有遮罩的函數
def scissor_change(scissor, w1, h1):
    resize_scissor = cv.resize(scissor, (w1, h1))
    scissor_mask_bgr = resize_scissor[:, :, :3]
    scissor_alpha_ch = resize_scissor[:, :, 3]
    _, pic_mask = cv.threshold(scissor_alpha_ch, 220, 255, cv.THRESH_BINARY)
    pic_part = cv.bitwise_and(scissor_mask_bgr, scissor_mask_bgr, mask=pic_mask)
    return pic_mask, pic_part

Round = 0  # 紀錄是第幾張臉的變數
while True:
    ret, image = capture.read()
    image = cv.flip(image, 1)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = detector(gray_image, 0)
    for face in faces:
        # 找到臉的座標
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()            

        # 定義剪刀石頭布的高和寬
        face_width = int(x2 - x1)
        face_hight = int(y2 - y1)

        pic_width1 = face_width//2  # 剪刀石頭布的圖要resize的寬跟高
        pic_hight1 = face_hight//2

        pic_width2 = face_width//4  # 剪刀石頭布的圖要放的位置
        pic_hight2 = face_hight//4

        # 三個函數隨機變動，所以剪刀石頭布可以隨機換
        type = random.randrange(0, 3)
        # 第一張臉的紀錄
        if Round == 0:
            if type == 0:
                pic_mask, pic_part = stone_change(stone, pic_width1, pic_hight1)
                first_choice = [1, 0, 0]
                first_position = [(x1, y1), (x2, y2)]

            elif type == 1:
                pic_mask, pic_part = paper_change(paper, pic_width1, pic_hight1)
                first_choice = [0, 1, 0]
                first_position = [(x1, y1), (x2, y2)]

            elif type == 2:
                pic_mask, pic_part = scissor_change(scissor, pic_width1, pic_hight1)
                first_choice = [0, 0, 1]
                first_position = [(x1, y1), (x2, y2)]
            Round = 1
            # 第一張臉的出拳紀錄完成，下一輪要記錄第二張臉的出拳

        # 第二張臉的紀錄
        else:
            if type == 0:
                pic_mask, pic_part = paper_change(stone, pic_width1, pic_hight1)
                second_choice = [1, 0, 0]
                second_position = [(x1, y1), (x2, y2)]

            elif type == 1:
                pic_mask, pic_part = paper_change(paper, pic_width1, pic_hight1)
                second_choice = [0, 1, 0]
                second_position  = [(x1, y1), (x2, y2)]

            elif type == 2:
                pic_mask, pic_part = paper_change(scissor, pic_width1, pic_hight1)
                second_choice = [0, 0, 1]
                second_position = [(x1, y1), (x2, y2)]
            Round = 0
            # 第二張臉的紀錄完成，可以重新記錄了

        # 額頭要放上剪刀石頭布的位置的處理
        image_area_no_face = cv.bitwise_not(pic_mask)
        pic_area = image[y1-pic_hight2 : y1+pic_hight1-pic_hight2,
                         x1+pic_width2 : x1+pic_width1+pic_width2]

        face_part = cv.bitwise_and(pic_area, pic_area, mask=image_area_no_face)
        final_part = cv.add(face_part, pic_part)

        image[y1-pic_hight2 : y1+pic_hight1-pic_hight2,
              x1+pic_width2 : x1+pic_width1+pic_width2] = final_part

    # 最後要show出的image的處理，然後show出
    cv.imshow('final', image)
    if cv.waitKey(1) &  0xFF == ord('q'):
        if len(faces) == 2:  # 如果有偵測到兩張臉才可以停下
            record_image = image
            capture.release()
            cv.destroyAllWindows()
            break

# 判斷誰輸誰贏
first_person = first_choice.index(1)
second_person = second_choice.index(1)

# 一開始先預設second person win
who_win = 2
win_position = second_position

# 平手
if((first_person == 0 and second_person == 0) or (first_person == 1 and second_person == 1)
    or (first_person == 2 and second_person == 2)):
    who_win = 0
    win_position = [(0,0), (50,50)]

# first_person 贏
elif((first_person == 0 and second_person == 2) or (first_person == 1 and second_person == 0)
    or(first_person == 2 and second_person == 1)):
    who_win = 1
    win_position = first_position

# show出結果(這邊之後要處理照片)
cv.imshow('record_image',record_image)
key = cv.waitKey(0)
cv.destroyAllWindows()
