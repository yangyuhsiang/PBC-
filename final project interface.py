import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox


class MainInterface(tk.Frame):
    
    
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()
    
    
    def createWidgets(self):
        f1 = tkFont.Font(size=16, family='Microsoft JhengHei')
        f2 = tkFont.Font(size=16, family='Courier New')
        # 主視窗以及右方回合、勝、負顯示
        self.cvsMain = tk.Canvas(self, height=600, width=800, bg='white')
        self.lblRound = tk.Label(self, text='回合', height=1, width=4, font=f1)
        self.lblShowRound = tk.Label(self, text='4', height=1, width=4, font=f2)
        self.lblWin = tk.Label(self, text='勝', height=1, width=4, font=f1)
        self.lblShowWin = tk.Label(self, text='3', height=1, width=4, font=f2)
        self.lblLose = tk.Label(self, text='負', height=1, width=4, font=f1)
        self.lblShowLose = tk.Label(self, text='1', height=1, width=4, font=f2)
        
        
        # 上方選擇模式欄
        self.mode = tk.StringVar()
        self.lblMode = tk.Label(self, text='選擇模式', height=1, width=16, font=f1)
        
        self.rb7_4 = tk.Radiobutton(self, text='七戰四勝', variable=self.mode, value='七戰四勝', command=self.print_selection, font=f1)
        self.rb5_3 = tk.Radiobutton(self, text='五戰三勝', variable=self.mode, value='五戰三勝', command=self.print_selection, font=f1)
        self.rb3_2 = tk.Radiobutton(self, text='三戰兩勝', variable=self.mode, value='三戰兩勝', command=self.print_selection, font=f1)
        
        self.btnSend = tk.Button(self, text='確認', height=1, width=4, command=self.send_request, font=f1)
        
        
        # 上方接受挑戰欄
        self.lblText1 = tk.Label(self, text='是否接受來自', height=1, width=12, font=f1)
        self.lblCom = tk.Label(self, text='192.168.1.100', height=1, width=13, font=f2)
        self.lblReMode = tk.Label(self, text='五戰三勝', height=1, width=8, font=f1)
        self.lblText2 = tk.Label(self, text='的挑戰', height=1, width=6, font=f1)

        self.btnY = tk.Button(self, text='是', height=1, width=4, command=self.yes, font=f1)
        self.btnN = tk.Button(self, text='否', height=1, width=4, command=self.no, font=f1)
        
        
        # 遊戲說明按鈕,點一下會跳出出拳說明
        self.btnIns = tk.Button(self, text='遊戲\n說明', height=2, width=4, command=self.instruction, font=f1)
        
        
        # 排版
        self.cvsMain.grid(row=2, rowspan=6, column=0, columnspan=6, sticky=tk.NE+tk.SW)
        self.lblRound.grid(row=2, column=6, sticky=tk.NE+tk.SW)
        self.lblShowRound.grid(row=3, column=6, sticky=tk.NE+tk.SW)
        self.lblWin.grid(row=4, column=6, sticky=tk.NE+tk.SW)
        self.lblShowWin.grid(row=5, column=6, sticky=tk.NE+tk.SW)
        self.lblLose.grid(row=6, column=6, sticky=tk.NE+tk.SW)
        self.lblShowLose.grid(row=7, column=6, sticky=tk.NE+tk.SW)
        
        self.lblMode.grid(row=0, column=0, sticky=tk.NE+tk.SW)
        self.rb7_4.grid(row=0, column=1)
        self.rb5_3.grid(row=0, column=2)
        self.rb3_2.grid(row=0, column=3)
        self.btnSend.grid(row=0, column=4)
        self.lblText1.grid(row=1, column=0, sticky=tk.NE+tk.SW)
        self.lblCom.grid(row=1, column=1, sticky=tk.NE+tk.SW)
        self.lblReMode.grid(row=1, column=2, sticky=tk.NE+tk.SW)
        self.lblText2.grid(row=1, column=3, sticky=tk.NE+tk.SW)
        self.btnY.grid(row=1, column=4)
        self.btnN.grid(row=1, column=5)
        
        self.btnIns.grid(row=0, rowspan=2, column=6)
    
    
    def print_selection(self):
        self.lblMode.config(text='您已選擇 ' + self.mode.get())
        
    
    def send_request(self):  # 未完成
        if self.mode.get() == '七戰四勝':
            pass
        elif self.mode.get() == '五戰三勝':
            pass
        else:
            pass
 
    
    def yes(self):  #未完成
        pass
    
    
    def no(self):  # 未完成
        pass
        
        
    def instruction(self):  # 這裡放出拳的說明
        tkinter.messagebox.showinfo(title='遊戲說明', message='如果你希望出剪刀：剪刀剪刀剪刀\n如果你希望出石頭：石頭石頭石頭\n如果你希望出布：布布布')


main_inter = MainInterface()
main_inter.master.title('Paper Scissor Stone')
main_inter.mainloop()