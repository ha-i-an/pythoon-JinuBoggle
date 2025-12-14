from tkinter import *
import time
import random

class BubbleHitEnemyPlatform:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 - 발판 위에서 적 맞추기 연습")
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
        self.direction = 1  
        self.platforms = []
        self.platforms.append(self.canvas.create_rectangle(150, 540, 350, 560, fill="gray"))
        self.platforms.append(self.canvas.create_rectangle(400, 420, 600, 440, fill="gray"))
        self.platforms.append(self.canvas.create_rectangle(100, 300, 300, 320, fill="gray"))


        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1
        self.ground_y = 640


        self.bubbles = []
        self.last_fire_time = 0
        self.fire_delay = 0.25

        self.enemies = []
        self.last_enemy_time = 0
        self.enemy_delay = 2.0
        self.spawn_levels = [560, 450, 330, 230]  

        self.canvas.create_text(
            380, 80, font="Times 15 italic bold",
            text="←→ 이동 / ↑ 점프 / Space 버블 — 발판 위에서 적을 맞춰보세요!"
        )


        while True:
            try:
                self.update_movement()
                self.update_bubbles()
                self.update_enemies()
            except TclError:
                return

            self.window.after(33)
            self.window.update()


    def update_movement(self):
        if 37 in self.keys:
            self.canvas.move(self.jinu, -5, 0)
            self.direction = -1
        if 39 in self.keys:
            self.canvas.move(self.jinu, 5, 0)
            self.direction = 1

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


    def update_bubbles(self):
        for bubble, direction in self.bubbles[:]:
            self.canvas.move(bubble, 10 * direction, 0)

            bx1, by1, bx2, by2 = self.canvas.coords(bubble)

            if bx2 < 0 or bx1 > 768:
                self.canvas.delete(bubble)
                self.bubbles.remove((bubble, direction))
                continue

            for enemy in self.enemies[:]:
                ex1, ey1, ex2, ey2 = self.canvas.coords(enemy)

                if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)

                    self.canvas.delete(bubble)
                    self.bubbles.remove((bubble, direction))
                    break


    def fireBubble(self):
        x1, y1, x2, y2 = self.canvas.coords(self.jinu)
        center_y = (y1 + y2) / 2

        if self.direction == 1:
            start_x = x2
        else:
            start_x = x1 - 20

        bubble = self.canvas.create_oval(
            start_x, center_y - 10,
            start_x + 20, center_y + 10,
            fill="skyblue", outline="blue"
        )

        self.bubbles.append((bubble, self.direction))


    def update_enemies(self):
        now = time.time()

        if now - self.last_enemy_time > self.enemy_delay:
            self.last_enemy_time = now
            self.spawn_enemy()

        for enemy in self.enemies[:]:
            self.canvas.move(enemy, -4, 0)

            x1, y1, x2, y2 = self.canvas.coords(enemy)

            if x2 < 0:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)

    def spawn_enemy(self):
        y = random.choice(self.spawn_levels)
        enemy = self.canvas.create_oval(
            760, y - 20, 780, y + 20,
            fill="pink", outline="red"
        )
        self.enemies.append(enemy)

    def keyPressHandler(self, event):
        self.keys.add(event.keycode)

        if event.keycode == 27:
            self.onClose()

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
    BubbleHitEnemyPlatform()
