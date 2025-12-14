from tkinter import *

class PopTrappedEnemyPlatform:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 - 갇힌 적 터뜨리기 연습")
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
        self.platforms.append(self.canvas.create_rectangle(150, 540, 350, 560, fill="gray"))
        self.platforms.append(self.canvas.create_rectangle(400, 420, 600, 440, fill="gray"))


        self.trapped = []
        self.trapped.append(
            self.canvas.create_oval(300, 500, 340, 540,
                                    fill="skyblue", outline="blue", width=2)
        )
        self.trapped.append(
            self.canvas.create_oval(500, 380, 540, 420,
                                    fill="skyblue", outline="blue", width=2)
        )

        self.canvas.create_text(
            380, 120, font="Times 15 italic bold",
            text="←→ 이동 / ↑ 점프 / 발판을 이용해 갇힌 적을 터뜨려 보세요!"
        )

        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = 640


        while True:
            try:
                self.update_movement()
                self.check_pop()
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
        bottom = y2
        center_x = (x1 + x2) / 2

        on_platform = False

        if self.jump_power < 0:
            for p in self.platforms:
                px1, py1, px2, py2 = self.canvas.coords(p)
                if py1 <= bottom <= py1 + 15:
                    if px1 <= center_x <= px2:
                        diff = bottom - py1
                        self.canvas.move(self.jinu, 0, -diff)
                        self.is_jumping = False
                        on_platform = True
                        break

        if not on_platform:
            if bottom >= self.ground_y:
                diff = bottom - self.ground_y
                self.canvas.move(self.jinu, 0, -diff)
                self.is_jumping = False
            else:
                if not self.is_jumping:
                    self.is_jumping = True
                    self.jump_power = 0


    def check_pop(self):
        jx1, jy1, jx2, jy2 = self.canvas.coords(self.jinu)

        for t in self.trapped[:]:
            tx1, ty1, tx2, ty2 = self.canvas.coords(t)

            if jx1 < tx2 and jx2 > tx1 and jy1 < ty2 and jy2 > ty1:
                self.canvas.delete(t)
                self.trapped.remove(t)

    def keyPressHandler(self, event):
        self.keys.add(event.keycode)

        if event.keycode == 27:
            self.onClose()

        if event.keycode == 38 and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = 18

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

    def onClose(self):
        self.window.destroy()


if __name__ == '__main__':
    PopTrappedEnemyPlatform()
