from tkinter import *
import sys

class MenuWindow:
    def __init__(self):
        window = Tk()
        window.title("지누 버블 메뉴 선택")
        window.geometry("768x672")

        self.menu_idx = 0
        self.canvas = Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)


        self.canvas.create_text(384, 260, font="Times 18 bold", text="1. 게임 시작")
        self.canvas.create_text(384, 320, font="Times 18 bold", text="2. 종료")

        self.arrow = self.canvas.create_text(310, 260, font="Times 18 bold", text="▶")

        self.menustr = "Menu selection: "
        self.menu_id = self.canvas.create_text(384, 480, font="Times 15 italic", text=self.menustr)

        while True:
            window.after(33)
            window.update()


    def keyReleaseHandler(self, event):

        if event.keycode == 38 and self.menu_idx > 0:
            self.menu_idx -= 1
            self.canvas.move(self.arrow, 0, -40)

        if event.keycode == 40 and self.menu_idx < 1:
            self.menu_idx += 1
            self.canvas.move(self.arrow, 0, 40)

        if event.keycode == 32:
            self.handleSelection()

    def keyPressHandler(self, event):
        print(event.keycode)


    def handleSelection(self):
        self.menustr = "Menu selection: " + str(self.menu_idx + 1)
        self.canvas.itemconfigure(self.menu_id, text=self.menustr)

        if self.menu_idx == 0:
            print("게임 시작!")

        if self.menu_idx == 1:
            print("프로그램 종료")
            sys.exit()

MenuWindow()
