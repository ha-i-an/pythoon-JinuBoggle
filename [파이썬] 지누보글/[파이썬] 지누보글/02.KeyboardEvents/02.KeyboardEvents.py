from tkinter import *
import time

class JumpAndBubble:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 -  (이동 + 점프 + 버블 )")
        self.window.geometry("768x672")

        self.keys = set()
        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.jinu = self.canvas.create_oval(
            360, 320, 400, 360, fill="lightgreen", outline="green", width=3
        )

        self.direction = 1  

        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = 360

        self.bubbles = []
        self.last_fire_time = 0
        self.fire_delay = 0.25

        self.keystr = "Key: "
        self.key_id = self.canvas.create_text(
            20, 20, anchor="nw", font="Times 14 bold", text=self.keystr
        )

        self.canvas.create_text(
            320, 200, font="Times 13 italic bold",
            text="← → 이동 / ↑ 점프 / Space 버블"
        )


        while True:
            try:
                self.keystr = "Key: " + str(self.keys)
                self.canvas.itemconfigure(self.key_id, text=self.keystr)

                if 37 in self.keys:
                    self.canvas.move(self.jinu, -5, 0)
                    self.direction = -1
                if 39 in self.keys:
                    self.canvas.move(self.jinu, 5, 0)
                    self.direction = 1

                if self.is_jumping:
                    self.canvas.move(self.jinu, 0, -self.jump_power)
                    self.jump_power -= self.gravity
                    pos = self.canvas.coords(self.jinu)
                    bottom = pos[3]
                    if bottom >= self.ground_y:
                        diff = bottom - self.ground_y
                        self.canvas.move(self.jinu, 0, -diff)
                        self.is_jumping = False

                if 32 in self.keys:
                    now = time.time()
                    if now - self.last_fire_time > self.fire_delay:
                        self.last_fire_time = now
                        self.fireBubble()

                self.update_bubbles()

            except TclError:
                return

            self.window.after(33)
            self.window.update()


    def update_bubbles(self):
        for bubble, direction in self.bubbles[:]:
            speed = 8 * direction
            self.canvas.move(bubble, speed, 0)

            x1, y1, x2, y2 = self.canvas.coords(bubble)

            if x2 < 0 or x1 > self.window.winfo_width():
                self.canvas.delete(bubble)
                self.bubbles.remove((bubble, direction))


    def fireBubble(self):
        x1, y1, x2, y2 = self.canvas.coords(self.jinu)
        center_y = (y1 + y2) / 2

        if self.direction == 1:  
            start_x = x2
        else:  
            start_x = x1 - 20

        bubble = self.canvas.create_oval(
            start_x, center_y - 10, start_x + 20, center_y + 10,
            fill="skyblue", outline="blue"
        )

        self.bubbles.append((bubble, self.direction))


    def keyPressHandler(self, event):
        if event.keycode == 27:
            self.onClose()
        else:
            self.keys.add(event.keycode)

            if event.keycode == 38 and not self.is_jumping:
                self.is_jumping = True
                self.jump_power = 18

            if event.keycode == 32:
                now = time.time()
                if now - self.last_fire_time > self.fire_delay:
                    self.last_fire_time = now
                    self.fireBubble()

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

    def onClose(self):
        self.window.destroy()


if __name__ == '__main__':
    JumpAndBubble()
