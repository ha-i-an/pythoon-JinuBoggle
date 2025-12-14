from tkinter import *
import time

class ImageMoveTest:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 이미지 이동 테스트")
        self.window.geometry("768x672")

        self.keys = set()
        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)


        self.jinu_right = PhotoImage(file="10.ImageApplyEvent/jinu_right.png")
        self.jinu_left = PhotoImage(file="10.ImageApplyEvent/jinu_left.png")

        self.jinu = self.canvas.create_image(380, 340, image=self.jinu_right)

        self.direction = 1  

        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = 360

        self.canvas.create_text(
            320, 200, font="Times 13 italic bold",
            text="← → 이동 / ↑ 점프 (이미지 방향 테스트)"
        )

        while True:
            try:

                if 37 in self.keys: 
                    self.canvas.move(self.jinu, -5, 0)
                    if self.direction != -1:
                        self.direction = -1
                        self.canvas.itemconfig(self.jinu, image=self.jinu_left)

                if 39 in self.keys:  
                    self.canvas.move(self.jinu, 5, 0)
                    if self.direction != 1:
                        self.direction = 1
                        self.canvas.itemconfig(self.jinu, image=self.jinu_right)


                if self.is_jumping:
                    self.canvas.move(self.jinu, 0, -self.jump_power)
                    self.jump_power -= self.gravity

                    x, y = self.canvas.coords(self.jinu)
                    bottom = y + 20

                    if bottom >= self.ground_y:
                        diff = bottom - self.ground_y
                        self.canvas.move(self.jinu, 0, -diff)
                        self.is_jumping = False

            except TclError:
                return
            
            self.window.after(33)
            self.window.update()

    def keyPressHandler(self, event):
        if event.keycode == 27:
            self.onClose()
        else:
            self.keys.add(event.keycode)

            if event.keycode == 38 and not self.is_jumping:
                self.is_jumping = True
                self.jump_power = 18

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

    def onClose(self):
        self.window.destroy()

if __name__ == '__main__':
    ImageMoveTest()
