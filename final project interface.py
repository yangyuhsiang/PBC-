import cv2 as cv
import numpy as np
import dlib
from math import hypot
import time


# 按下確認connected後才開始進行
stone = cv.imread("rock.png", cv.IMREAD_UNCHANGED)
paper = cv.imread("paper.png", cv.IMREAD_UNCHANGED)
scissor = cv.imread("scissor.png", cv.IMREAD_UNCHANGED)
sad_face = cv.imread("small_lose.png", cv.IMREAD_UNCHANGED)
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


'''new'''
# 每一局贏的人的小特效
def small_winer_effect():
    pass


# small_lose的大小調整函數，還有遮罩的函數
def small_loser_effect(sad_face ,w1, h1):
    resize_sad_face = cv.resize(sad_face, (w1, h1))
    sad_face_mask_bgr = resize_sad_face[:, :, :3]
    sad_face_alpha_ch = resize_sad_face[:, :, 3]
    _, pic_mask = cv.threshold(sad_face_alpha_ch, 220, 255, cv.THRESH_BINARY)
    pic_part = cv.bitwise_and(sad_face_mask_bgr, sad_face_mask_bgr, mask=pic_mask)
    return pic_mask, pic_part


# 把調整好的圖和在臉上
def face_change(img, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2):
    image_area_no_face = cv.bitwise_not(pic_mask)
    pic_area = img[pic_y1 : pic_y2, pic_x1 : pic_x2]

    face_part = cv.bitwise_and(pic_area, pic_area, mask=image_area_no_face)
    final_part = cv.add(face_part, pic_part)

    img[pic_y1 : pic_y2, pic_x1 : pic_x2] = final_part

    return img


# 放在gui上面的照片，會依照你按的鍵去改變臉上的出拳，如果要改變照片就在這個function裡面做變動
def show_image(image, pressed):
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
        '''下面的function 傳入前就先加文字上去'''
        if main_inter.pressed == 0:  # random
            image = paper_scissor_stone(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1)
        elif main_inter.pressed == 1:  # scissor
            image = only_scissor(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1)
        elif main_inter.pressed == 2:  # rock
            image = only_paper(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1)
        else:  # paper
            image = only_stone(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1)
    return image


# random剪刀石頭布的function
def paper_scissor_stone(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1):
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
    return image


# 只有剪刀的function
def only_scissor(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1):
    if pic_y2 <= image_width and pic_x2 <= image_hight and pic_x1 >= 0 and pic_y1 >= 0:  # 沒有超出範圍
        pic_mask, pic_part = scissor_change(scissor, pic_width1, pic_hight1)
        image = face_change(image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)
    else:
        pass
    return image


# 只有布的funtion
def only_paper(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1):
    if pic_y2 <= image_width and pic_x2 <= image_hight and pic_x1 >= 0 and pic_y1 >= 0:  # 沒有超出範圍
        pic_mask, pic_part = paper_change(paper, pic_width1, pic_hight1)
        image = face_change(image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)
    else:
        pass
    return image


# 只有石頭的function
def only_stone(image, image_width, image_hight, pic_x1, pic_x2, pic_y1, pic_y2, pic_width1, pic_hight1):
    if pic_y2 <= image_width and pic_x2 <= image_hight and pic_x1 >= 0 and pic_y1 >= 0:  # 沒有超出範圍
        pic_mask, pic_part = stone_change(stone, pic_width1, pic_hight1)
        image = face_change(image, pic_mask, pic_part, pic_y1, pic_y2, pic_x1, pic_x2)
    else:
        pass
    return image


# 讀取相機的function
def video_stream():
    global frame
    ret, image = capture.read()
    pressed = main_inter.pressed
    frame = show_image(image, pressed)
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    main_inter.lblMain.imgtk = imgtk
    main_inter.lblMain.configure(image=imgtk)
    main_inter.lblMain.after(1, video_stream)


class MainInterfacePlayer1(tk.Frame):

    
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()
        self.pressed = 0

    
    def createWidgets(self):
        f1 = tkFont.Font(size=16, family='Microsoft JhengHei')
        f2 = tkFont.Font(size=16, family='Courier New')
        self.draw_count = 0
        self.win_count = 0
        self.lose_count = 0
        # 主視窗以及右方回合、勝、負顯示
        self.lblMain = tk.Label(self)

        self.lblDraw = tk.Label(self, text='平手', height=1, width=4, font=f1)
        self.lblShowDraw = tk.Label(self, text='0', height=1, width=4, font=f2)
        self.lblWin = tk.Label(self, text='勝', height=1, width=4, font=f1)
        self.lblShowWin = tk.Label(self, text='0', height=1, width=4, font=f2)
        self.lblLose = tk.Label(self, text='負', height=1, width=4, font=f1)
        self.lblShowLose = tk.Label(self, text='0', height=1, width=4, font=f2)
        
        
        # 剪刀石頭布按鈕
        self.stone = Image.open("rock.png")
        self.stone = self.stone.resize((50,50), Image.ANTIALIAS)
        self.stone_tk = ImageTk.PhotoImage(self.stone)
        self.paper = Image.open("paper.png")
        self.paper = self.paper.resize((50, 50), Image.ANTIALIAS)
        self.paper_tk = ImageTk.PhotoImage(self.paper)
        self.scissor = Image.open("scissor.png")
        self.scissor = self.scissor.resize((50, 50), Image.ANTIALIAS)
        self.scissor_tk = ImageTk.PhotoImage(self.scissor)
        self.btnScissor = tk.Button(self, height=50, width=50, image=self.scissor_tk, command=self.scissor_fun)
        self.btnStone = tk.Button(self, height=50, width=50, image=self.stone_tk, command=self.stone_fun)
        self.btnPaper = tk.Button(self, height=50, width=50, image=self.paper_tk, command=self.paper_fun)
        
        
        # 上方選擇模式欄
        self.mode = tk.StringVar()
        self.lblMode = tk.Label(self, text='選擇模式', height=1, width=16, font=f1)
        
        self.rb7_4 = tk.Radiobutton(self, text='七戰四勝', variable=self.mode, value='七戰四勝', command=self.print_selection, font=f1)
        self.rb5_3 = tk.Radiobutton(self, text='五戰三勝', variable=self.mode, value='五戰三勝', command=self.print_selection, font=f1)
        self.rb3_2 = tk.Radiobutton(self, text='三戰兩勝', variable=self.mode, value='三戰兩勝', command=self.print_selection, font=f1)
        
        self.btnSend = tk.Button(self, text='確認', height=1, width=4, command=self.send_request, font=f1)
        
        
        # 遊戲說明按鈕,點一下會跳出出拳說明
        self.btnIns = tk.Button(self, text='遊戲\n說明', height=2, width=4, command=self.instruction, font=f1)
        
        
        # 排版
        self.lblMain.grid(row=2, rowspan=5, column=0, columnspan=6, sticky=tk.NE+tk.SW)
        self.lblDraw.grid(row=2, column=6, sticky=tk.NE+tk.SW)
        self.lblShowDraw.grid(row=3, column=6, sticky=tk.NE+tk.SW)
        self.lblWin.grid(row=4, column=6, sticky=tk.NE+tk.SW)
        self.lblShowWin.grid(row=5, column=6, sticky=tk.NE+tk.SW)
        self.lblLose.grid(row=6, column=6, sticky=tk.NE+tk.SW)
        self.lblShowLose.grid(row=7, column=6, sticky=tk.NE+tk.SW)
        
        self.lblMode.grid(row=0, rowspan=2, column=0, sticky=tk.NE+tk.SW)
        self.rb7_4.grid(row=0, rowspan=2, column=1)
        self.rb5_3.grid(row=0, rowspan=2, column=2)
        self.rb3_2.grid(row=0, rowspan=2, column=3)
        self.btnSend.grid(row=0, rowspan=2, column=4)
        
        self.btnIns.grid(row=0, rowspan=2, column=6)
        
        self.btnScissor.grid(row=7, column=0)
        self.btnStone.grid(row=7, column=2)
        self.btnPaper.grid(row=7, column=4)
    
    
    def print_selection(self):
        self.lblMode.config(text='您已選擇 ' + self.mode.get())
        
    
    def send_request(self):
        if self.mode.get() == '七戰四勝':
            client.send('2'.encode())
        elif self.mode.get() == '五戰三勝':
            client.send('1'.encode())
        else:
            client.send('0'.encode())
        mode_yes_or_no = client.recv(2048).decode()
        if mode_yes_or_no == 'N':
            tkinter.messagebox.showinfo(title='重新選擇模式', message='對方要求重新選擇模式，請重新選擇')
            self.createWidgets()


    def instruction(self):  # 這裡放出拳的說明
        tkinter.messagebox.showinfo(title='遊戲說明', message='如果你希望出剪刀：剪刀剪刀剪刀\n如果你希望出石頭：石頭石頭石頭\n如果你希望出布：布布布')


    # pressed = 1 是按完之後才會回傳出來
    def scissor_fun(self):
        self.pressed = 1
        client.send('S'.encode())
        ans = client.recv(2048).decode()  # 加一個try except 如果沒有收到就跑等待收取照片(opencv放文字)
                                          # 加一個變數，讓show image function 可以加上文字
        if ans == 'W':
            self.win_count += 1
            # 這邊應該要對照片加上輸贏的特效
            # 加上一個變數，讓外面的show image function 可以去判斷你是輸是贏
            # 再加一個time.sleep(5) ，有輸贏的特效5秒，然後就回到原本的隨便跳來跳去。

            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            print('recv')
            self.result_image = frame
            while True:
                result, imgencode = cv.imencode('.jpg', self.result_image)
                data = np.array(imgencode)
                stringData = data.tobytes()
                client.send( str(len(stringData)).ljust(16).encode())
                client.send(stringData)


    def stone_fun(self):
        self.pressed = 2
        client.send('R'.encode())
        ans = client.recv(2048).decode()
        if ans == 'W':
            self.win_count += 1
            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            print('recv')
            self.result_image = frame
            while True:
                result, imgencode = cv.imencode('.jpg', self.result_image)
                data = np.array(imgencode)
                stringData = data.tobytes()
                client.send( str(len(stringData)).ljust(16).encode())
                client.send(stringData)
        
    
    def paper_fun(self):
        self.pressed = 3
        client.send('P'.encode())
        ans = client.recv(2048).decode()
        if ans == 'W':
            self.win_count += 1
            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            self.imgFile = open('moonsave.png', 'w')  # 開始寫入圖片檔
            self.imgData = frame  # 接收遠端主機傳來的數據
            self.imgFile.write(self.imgData)
            self.imgFile.close()
            print('start send image')
            self.imgFile = open("moon.png", "rb")

            while True:
                self.imgData = self.imgFile.readline(512)
                if not self.imgData:
                    break  # 讀完檔案結束迴圈
                client.send(self.imgData)
            self.imgFile.close()
            print('transmit end')

            # 接收來自server的照片
            socks = [client]
            while True:
                readySocks, _, _ = select.select(socks, [], [], 5)
                for sock1 in readySocks:
                    length_client = recvall(sock1, 16)
                    stringData_client = recvall(sock1, int(length_client))
                    data_client = np.frombuffer(stringData_client, dtype='uint8')
                    decimg_client = cv.imdecode(data_client, 1)
                    cv.imshow('SERVER', decimg_client)
                    key = cv.waitKey(1)
                    if key == ord('q'):
                        cv.destroyAllWindows()
                        break


class MainInterfacePlayer2(tk.Frame):
    
    
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.recv_info()
        self.createWidgets()
        self.pressed = 0

    
    # 接收client1傳送要怎麼玩的邀請
    def recv_info(self):
        self.game_mode = client.recv(2048).decode()
        if self.game_mode == '0':
            self.mode = '三戰兩勝'
        elif self.game_mode == '1':
            self.mode = '五戰三勝'
        elif self.game_mode == '2':
            self.mode = '七戰四勝'
        self.player1_addr = client.recv(2048).decode()


    def createWidgets(self):
        f1 = tkFont.Font(size=16, family='Microsoft JhengHei')
        f2 = tkFont.Font(size=16, family='Courier New')
        self.draw_count = 0
        self.win_count = 0
        self.lose_count = 0
        # 主視窗以及右方回合、勝、負顯示
        self.lblMain = tk.Label(self)

        self.lblDraw = tk.Label(self, text='平手', height=1, width=4, font=f1)
        self.lblShowDraw = tk.Label(self, text='0', height=1, width=4, font=f2)
        self.lblWin = tk.Label(self, text='勝', height=1, width=4, font=f1)
        self.lblShowWin = tk.Label(self, text='0', height=1, width=4, font=f2)
        self.lblLose = tk.Label(self, text='負', height=1, width=4, font=f1)
        self.lblShowLose = tk.Label(self, text='0', height=1, width=4, font=f2)
        
        
        # 剪刀石頭布按鈕
        self.stone = Image.open("rock.png")
        self.stone = self.stone.resize((50,50), Image.ANTIALIAS)
        self.stone_tk = ImageTk.PhotoImage(self.stone)
        self.paper = Image.open("paper.png")
        self.paper = self.paper.resize((50, 50), Image.ANTIALIAS)
        self.paper_tk = ImageTk.PhotoImage(self.paper)
        self.scissor = Image.open("scissor.png")
        self.scissor = self.scissor.resize((50, 50), Image.ANTIALIAS)
        self.scissor_tk = ImageTk.PhotoImage(self.scissor)
        self.btnScissor = tk.Button(self, height=50, width=50, image=self.scissor_tk, command=self.scissor_fun)
        self.btnStone = tk.Button(self, height=50, width=50, image=self.stone_tk, command=self.stone_fun)
        self.btnPaper = tk.Button(self, height=50, width=50, image=self.paper_tk, command=self.paper_fun)
        

        # 上方接受挑戰欄
        self.lblText1 = tk.Label(self, text='是否接受來自', height=1, width=12, font=f1)
        self.lblCom = tk.Label(self, text=self.player1_addr, height=1, width=13, font=f2)
        self.lblReMode = tk.Label(self, text=self.mode, height=1, width=8, font=f1)
        self.lblText2 = tk.Label(self, text='的挑戰', height=1, width=6, font=f1)

        self.btnY = tk.Button(self, text='是', height=1, width=4, command=self.yes, font=f1)
        self.btnN = tk.Button(self, text='否', height=1, width=4, command=self.no, font=f1)
        
        
        # 遊戲說明按鈕,點一下會跳出出拳說明
        self.btnIns = tk.Button(self, text='遊戲\n說明', height=2, width=4, command=self.instruction, font=f1)


        # 排版
        self.lblMain.grid(row=2, rowspan=5, column=0, columnspan=6, sticky=tk.NE+tk.SW)
        self.lblDraw.grid(row=2, column=6, sticky=tk.NE+tk.SW)
        self.lblShowDraw.grid(row=3, column=6, sticky=tk.NE+tk.SW)
        self.lblWin.grid(row=4, column=6, sticky=tk.NE+tk.SW)
        self.lblShowWin.grid(row=5, column=6, sticky=tk.NE+tk.SW)
        self.lblLose.grid(row=6, column=6, sticky=tk.NE+tk.SW)
        self.lblShowLose.grid(row=7, column=6, sticky=tk.NE+tk.SW)
        
        self.lblText1.grid(row=0, rowspan=2, column=0, sticky=tk.NE+tk.SW)
        self.lblCom.grid(row=0, rowspan=2,column=1, sticky=tk.NE+tk.SW)
        self.lblReMode.grid(row=0, rowspan=2, column=2, sticky=tk.NE+tk.SW)
        self.lblText2.grid(row=0, rowspan=2, column=3, sticky=tk.NE+tk.SW)
        self.btnY.grid(row=0, rowspan=2, column=4)
        self.btnN.grid(row=0, rowspan=2, column=5)
        
        self.btnIns.grid(row=0, rowspan=2, column=6)
 
        self.btnScissor.grid(row=7, column=0)
        self.btnStone.grid(row=7, column=2)
        self.btnPaper.grid(row=7, column=4)


    def yes(self):
        client.send('Y'.encode())



    def no(self):
        client.send('N'.encode())
        self.recv_info()
        self.createWidgets()
        
    def instruction(self):  # 這裡放出拳的說明
        tkinter.messagebox.showinfo(title='遊戲說明', message='如果你希望出剪刀：剪刀剪刀剪刀\n如果你希望出石頭：石頭石頭石頭\n如果你希望出布：布布布')


    def scissor_fun(self):
        self.pressed = 1
        client.send('S'.encode())
        ans = client.recv(2048).decode()
        if ans == 'W':
            self.win_count += 1
            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            self.result_image = imgtk
            while True:
                result, imgencode = cv.imencode('.jpg', self.result_image)
                data = np.array(imgencode)
                stringData = data.tobytes()
                client.send( str(len(stringData)).ljust(16).encode())
                client.send(stringData)



    def stone_fun(self):
        self.pressed = 2
        client.send('R'.encode())
        ans = client.recv(2048).decode()
        if ans == 'W':
            self.win_count += 1
            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            self.result_image = imgtk
            while True:
                result, imgencode = cv.imencode('.jpg', self.result_image)
                data = np.array(imgencode)
                stringData = data.tobytes()
                client.send( str(len(stringData)).ljust(16).encode())
                client.send(stringData)


    def paper_fun(self):
        self.pressed = 3
        client.send('P'.encode())
        ans = client.recv(2048).decode()
        if ans == 'W':
            self.win_count += 1
            self.pressed = 0
            self.lblShowWin.configure(text=str(self.win_count))
        elif ans == 'L':
            self.lose_count += 1
            self.pressed = 0
            self.lblShowLose.configure(text=str(self.lose_count))
        elif ans == 'D':
            self.draw_count += 1
            self.pressed = 0
            self.lblShowDraw.configure(text=str(self.draw_count))
        else:
            self.result_image = imgtk
            while True:
                result, imgencode = cv.imencode('.jpg', self.result_image)
                data = np.array(imgencode)
                stringData = data.tobytes()
                client.send( str(len(stringData)).ljust(16).encode())
                client.send(stringData)


# 接收照片data然後處理的函數
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


msg_box = tkinter.messagebox.askquestion(title='連線狀態', message='您已連線成功，是否進入遊戲？')
if msg_box == 'yes':
    # 先顯示已經連線的視窗
    FORMAT = 'utf-8'
    SERVER = '140.112.87.31'
    PORT = 5050
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(ADDR)
    except:
        print('connetion fail')  # 可以加一個視窗是連線失敗

    connected_msg = client.recv(2048).decode()  # your are connected
    player_num = client.recv(2048).decode()  # player number
    print(player_num)

    # 玩家1
    if player_num == '1':
        main_inter = MainInterfacePlayer1()
        main_inter.master.title('Paper Scissor Stone')
        video_stream()
        main_inter.mainloop()

    # 玩家2
    else:
        main_inter = MainInterfacePlayer2()
        main_inter.master.title('Paper Scissor Stone')
        video_stream()
        main_inter.mainloop()
