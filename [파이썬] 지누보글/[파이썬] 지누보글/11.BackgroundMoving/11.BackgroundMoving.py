from tkinter import *

class BackgroundMoving:
    def __init__(self):
        window = Tk()
        window.title("지누 버블 - 배경 고정")
        window.geometry("768x672")

        self.canvas = Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.bg_img = PhotoImage(file="11.BackgroundMoving/image/GNUcampus.png")

        self.canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

        while True:
            try:
                window.after(33)
                window.update()
            except TclError:
                return

if __name__ == "__main__":
    BackgroundMoving()
