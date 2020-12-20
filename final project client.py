import cv2 as cv
import numpy as np
import dlib
import random
import socket
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


def face_change(img, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2):  # 把調整好的圖和在臉上
    image_area_no_face = cv.bitwise_not(pic_mask)
    pic_area = img[pic_y1 : pic_y2, pic_x1 : pic_x2]

    face_part = cv.bitwise_and(pic_area, pic_area, mask=image_area_no_face)
    final_part = cv.add(face_part, pic_part)

    img[pic_y1 : pic_y2, pic_x1 : pic_x2] = final_part

    return img
# 剪刀石頭布的function
def paper_scissor_stone():
    while True:
        ret, image = capture.read()
        final_image = image
        final_image = cv.flip(final_image, 1)
        image_hight = image.shape[0]
        image_width = image.shape[1]
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

            # 如果要放圖的位置超過視窗，就不能繼續往下執行
            pic_y1 = y1-pic_hight2
            pic_y2 = y1+pic_hight1-pic_hight2
            pic_x1 = x1+pic_width2
            pic_x2 = x1+pic_width1+pic_width2

            if pic_y2 <= image_width and pic_x2 <= image_hight and pic_x1 >= 0 and pic_y1 >= 0:  # 沒有超出範圍
                type = random.randrange(0, 3)  # 三個函數隨機變動，所以剪刀石頭布可以隨機換
                if type == 0:
                    pic_mask, pic_part = stone_change(stone, pic_width1, pic_hight1)

                elif type == 1:
                    pic_mask, pic_part = paper_change(paper, pic_width1, pic_hight1)

                elif type == 2:
                    pic_mask, pic_part = scissor_change(scissor, pic_width1, pic_hight1)

                # 額頭要放上剪刀石頭布的位置的處理
                image = face_change(image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)
            else:  # 要放的圖超出範圍的時候
                pass
            # 最後要show出的image的處理，然後show出
        cv.imshow('image', image)

        key = cv.waitKey(50)
        if key == ord('r'):  # 最後要出石頭
            pic_mask, pic_part = stone_change(stone, pic_width1, pic_hight1)
            final_image = face_change(final_image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)           
            capture.release()
            cv.destroyAllWindows()
            break
        elif key == ord('p'):  # 最後要出布
            pic_mask, pic_part = paper_change(paper, pic_width1, pic_hight1)
            final_image = face_change(final_image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)           
            capture.release()
            cv.destroyAllWindows()
            break        
        elif key == ord('s'):  # 最後要出剪刀
            pic_mask, pic_part = scissor_change(scissor, pic_width1, pic_hight1)
            final_image = face_change(final_image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)           
            capture.release()
            cv.destroyAllWindows()
            break
    return final_image
final_image = paper_scissor_stone()


TCP_IP = socket.gethostname()  # 要改成自己電腦的IP
TCP_PORT = 8002
sock = socket.socket()
frame = final_image
sock.connect((TCP_IP, TCP_PORT))
while True:
    result, imgencode = cv.imencode('.jpg', frame)
    data = np.array(imgencode)
    stringData = data.tobytes()
    sock.send( str(len(stringData)).ljust(16).encode())
    sock.send( stringData )