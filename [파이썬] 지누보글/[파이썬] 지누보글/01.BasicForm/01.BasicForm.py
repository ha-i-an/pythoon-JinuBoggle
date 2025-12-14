from tkinter import *

class BasicForm:
    def __init__(self):
        window = Tk()#윈도우 생성
        window.title("지누 버블")#윈도우 이름 
        window.geometry("768x672")#윈도우 크기 설정
        
        self.canvas = Canvas(window, bg="white")#그림판 생성
        self.canvas.pack(expand=True, fill=BOTH)#그림판을 윈도우에 붙이기

        self.canvas.create_text(
            380, 400,
            font="Times 13 bold",
            text="지누 보글 - 기본 화면",
            fill='blue'
        )

        self.jinu = self.canvas.create_oval(
            350, 300, 390, 340,
            fill="lightgreen", outline="green"
        )

        #게임 Main 루프
        while True:
            try:
                #게임구현
                pass  

            except TclError:
                return

            window.after(33)#33ms 대기
            window.update()#화면 업데이트

if __name__ == '__main__':
    BasicForm()
