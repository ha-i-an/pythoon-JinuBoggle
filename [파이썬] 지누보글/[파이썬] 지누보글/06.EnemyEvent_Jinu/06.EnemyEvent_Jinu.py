from tkinter import *
import time
import random

class EnemyEvent:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 - 적 생성 연습")
        self.window.geometry("768x672")

        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.enemies = []

        self.last_enemy_time = 0
        self.enemy_delay = 1.8  

        self.spawn_levels = [200, 350, 500]

        self.canvas.create_text(
            380, 100, font="Times 14 italic bold",
            text="적이 오른쪽에서 생성되어 왼쪽으로 이동합니다!"
        )

        while True:
            try:
                self.update_enemies()
            except TclError:
                return

            self.window.after(33)
            self.window.update()

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

    def onClose(self):
        self.window.destroy()


if __name__ == '__main__':
    EnemyEvent()
