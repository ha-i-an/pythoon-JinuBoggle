from tkinter import *
import time

class JinuJumpRunBubble:
    def __init__(self):
        window = Tk()
        window.title("지누 버블 - 점프 + 달리기 + 버블 발사")
        window.geometry("768x672")
        window.resizable(0, 0)

        self.canvas = Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)


        self.keys = set()
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)

        self.right1 = PhotoImage(file="14.JumpRunBubble/image/Rightwalk1.png")
        self.right2 = PhotoImage(file="14.JumpRunBubble/image/Rightwalk2.png")
        self.left1  = PhotoImage(file="14.JumpRunBubble/image/Leftwalk1.png")
        self.left2  = PhotoImage(file="14.JumpRunBubble/image/Leftwalk2.png")
        self.idle_right = PhotoImage(file="14.JumpRunBubble/image/jinu_right.png")
        self.idle_left  = PhotoImage(file="14.JumpRunBubble/image/jinu_left.png")

        self.bubble_img = PhotoImage(file="14.JumpRunBubble/image/bubble.png")


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

        self.bubbles = []

        self.pos_id = self.canvas.create_text(
            200, 40, font="Times 15 bold", text="Position: (0,0)"
        )

        self.canvas.create_text(
            380, 80, font="Times 14 italic",
            text="← → 이동 / ↑ 점프 / Space 버블 발사"
        )

        while True:
            try:
                self.updateMovement()
                self.updateJump()
                self.updateAnimation()
                self.updateBubbles()
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
                img = self.right1 if self.frame == 0 else self.right2
            else:
                img = self.left1 if self.frame == 0 else self.left2

            self.canvas.itemconfigure(self.jinu, image=img)


    def fireBubble(self):
        x, y = self.canvas.coords(self.jinu)

        start_x = x + 30 if self.direction == 1 else x - 30

        bubble = self.canvas.create_image(start_x, y,
                                          image=self.bubble_img)

        self.bubbles.append((bubble, self.direction))

    def updateBubbles(self):
        for b, d in self.bubbles[:]:
            self.canvas.move(b, 10 * d, 0)

            bx, by = self.canvas.coords(b)

            if bx < 0 or bx > 768:
                self.canvas.delete(b)
                self.bubbles.remove((b, d))


    def updatePositionText(self):
        x, y = self.canvas.coords(self.jinu)
        self.canvas.itemconfigure(self.pos_id,
                                  text=f"Position: ({int(x)}, {int(y)})")


    def keyPressHandler(self, event):
        self.keys.add(event.keycode)

        if event.keycode == 38 and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = 18

        if event.keycode == 32:
            self.fireBubble()


    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)


if __name__ == "__main__":
    JinuJumpRunBubble()
