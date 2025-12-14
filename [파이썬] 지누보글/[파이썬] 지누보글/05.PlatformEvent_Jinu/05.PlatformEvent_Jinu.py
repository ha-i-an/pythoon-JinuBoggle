from tkinter import *

class PlatformEvent:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 - 발판 연습")
        self.window.geometry("768x672")

        self.keys = set()
        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.jinu = self.canvas.create_oval(
            360, 600, 400, 640,
            fill="lightgreen", outline="green", width=3
        )

        self.platforms = []
        self.platforms.append(
            self.canvas.create_rectangle(150, 540, 350, 560, fill="gray")
        )
        self.platforms.append(
            self.canvas.create_rectangle(450, 420, 650, 440, fill="gray")
        )

        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = 640  

        self.canvas.create_text(
            380, 150, font="Times 14 italic bold",
            text="← → 이동 / ↑ 점프 / 발판에 착지해보세요!"
        )

        while True:
            try:
                self.update_movement()
            except TclError:
                return

            self.window.after(33)
            self.window.update()


    def update_movement(self):
        if 37 in self.keys:
            self.canvas.move(self.jinu, -5, 0)
        if 39 in self.keys:
            self.canvas.move(self.jinu, 5, 0)

        if self.is_jumping:
            self.canvas.move(self.jinu, 0, -self.jump_power)
            self.jump_power -= self.gravity

        x1, y1, x2, y2 = self.canvas.coords(self.jinu)
        jinu_bottom = y2
        jinu_center_x = (x1 + x2) / 2

        on_platform = False

        if self.jump_power < 0:
            for p in self.platforms:
                px1, py1, px2, py2 = self.canvas.coords(p)

                if py1 <= jinu_bottom <= py1 + 15:
                    if px1 <= jinu_center_x <= px2:
                        diff = jinu_bottom - py1
                        self.canvas.move(self.jinu, 0, -diff)
                        self.is_jumping = False
                        on_platform = True
                        break

        if not on_platform:
            if jinu_bottom >= self.ground_y:
                diff = jinu_bottom - self.ground_y
                self.canvas.move(self.jinu, 0, -diff)
                self.is_jumping = False
            else:
                if not self.is_jumping:
                    self.is_jumping = True
                    self.jump_power = 0

    def keyPressHandler(self, event):
        if event.keycode == 27:
            self.onClose()
            return

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
    PlatformEvent()
