from tkinter import *
import time

class JinuJumpRun:
    def __init__(self):
        window = Tk()
        window.title("지누 버블 - 점프 + 달리기 애니메이션")
        window.geometry("768x672")
        window.resizable(0, 0)

        self.canvas = Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)


        self.keys = set()
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)

        self.right1 = PhotoImage(file="13.JumpRunAnimation/image/Rightwalk1.png")
        self.right2 = PhotoImage(file="13.JumpRunAnimation/image/Rightwalk2.png")

        self.left1  = PhotoImage(file="13.JumpRunAnimation/image/Leftwalk1.png")
        self.left2  = PhotoImage(file="13.JumpRunAnimation/image/Leftwalk2.png")

        self.idle_right = PhotoImage(file="13.JumpRunAnimation/image/jinu_right.png")
        self.idle_left  = PhotoImage(file="13.JumpRunAnimation/image/jinu_left.png")

        self.start_x = 384
        self.start_y = 520   
        self.jinu = self.canvas.create_image(self.start_x, self.start_y,
                                             image=self.idle_right)

        self.direction = 1
        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = self.start_y   

        self.frame = 0
        self.last_time = time.time()
        self.delay = 0.15

        self.pos_id = self.canvas.create_text(
            200, 40, font="Times 15 bold",
            text="Position: (0, 0)"
        )

        self.canvas.create_text(
            384, 80, font="Times 15 italic",
            text="← → 이동 / ↑ 점프"
        )

        while True:
            try:
                self.updateMovement()
                self.updateJump()
                self.updateAnimation()
                self.updatePositionText()

                window.after(33)
                window.update()
            except TclError:
                return

    def updateMovement(self):
        if 37 in self.keys:   
            self.canvas.move(self.jinu, -5, 0)
            self.direction = -1

        if 39 in self.keys:   
            self.canvas.move(self.jinu, 5, 0)
            self.direction = 1


    def updateJump(self):
        if self.is_jumping:
            self.canvas.move(self.jinu, 0, -self.jump_power)
            self.jump_power -= self.gravity

            x, y = self.canvas.coords(self.jinu)

            if y >= self.ground_y:
                diff = self.ground_y - y
                self.canvas.move(self.jinu, 0, diff)
                self.is_jumping = False
                self.jump_power = 0


    def updateAnimation(self):
        now = time.time()

        moving = (37 in self.keys) or (39 in self.keys)

        if not moving:
            if self.direction == 1:
                self.canvas.itemconfigure(self.jinu, image=self.idle_right)
            else:
                self.canvas.itemconfigure(self.jinu, image=self.idle_left)
            return

        if now - self.last_time > self.delay:
            self.last_time = now
            self.frame = (self.frame + 1) % 2

            if self.direction == 1: 
                if self.frame == 0:
                    self.canvas.itemconfigure(self.jinu, image=self.right1)
                else:
                    self.canvas.itemconfigure(self.jinu, image=self.right2)
            else:                   
                if self.frame == 0:
                    self.canvas.itemconfigure(self.jinu, image=self.left1)
                else:
                    self.canvas.itemconfigure(self.jinu, image=self.left2)


    def updatePositionText(self):
        x, y = self.canvas.coords(self.jinu)
        self.canvas.itemconfigure(self.pos_id,
                                  text=f"Position: ({int(x)}, {int(y)})")


    def keyPressHandler(self, event):
        if event.keycode == 38 and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = 18

        self.keys.add(event.keycode)

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)


if __name__ == "__main__":
    JinuJumpRun()
