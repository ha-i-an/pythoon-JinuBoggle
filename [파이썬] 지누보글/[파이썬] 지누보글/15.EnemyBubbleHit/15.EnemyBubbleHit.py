from tkinter import *
import time

class EnemyBubbleHitTest:
    def __init__(self):
        window = Tk()
        window.title("지누 버블 - 적 이동 + 버블 포획 테스트")
        window.geometry("768x672")
        window.resizable(0, 0)

        self.canvas = Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)


        self.keys = set()
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)


        self.right1 = PhotoImage(file="15.EnemyBubbleHit/image/Rightwalk1.png")
        self.right2 = PhotoImage(file="15.EnemyBubbleHit/image/Rightwalk2.png")
        self.left1  = PhotoImage(file="15.EnemyBubbleHit/image/Leftwalk1.png")
        self.left2  = PhotoImage(file="15.EnemyBubbleHit/image/Leftwalk2.png")
        self.idle_right = PhotoImage(file="15.EnemyBubbleHit/image/jinu_right.png")
        self.idle_left  = PhotoImage(file="15.EnemyBubbleHit/image/jinu_left.png")

        self.bubble_img = PhotoImage(file="15.EnemyBubbleHit/image/bubble.png")

        self.enemy_img = PhotoImage(file="15.EnemyBubbleHit/image/beer.png")
        self.enemy_captured_img = PhotoImage(file="15.EnemyBubbleHit/image/beer_bubble.png")

        self.start_x = 200
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

        self.enemy = self.canvas.create_image(500, 520, image=self.enemy_img)
        self.enemy_dx = -3
        self.enemy_state = "normal" 
        self.capture_start_time = 0

        self.canvas.create_text(384, 50, font="Times 15 bold",
                                text="← → 이동 / ↑ 점프 / Space 버블 발사")

        while True:
            try:
                self.updateMovement()
                self.updateJump()
                self.updateAnimation()
                self.updateBubbles()
                self.updateEnemy()

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
            img = self.idle_right if self.direction == 1 else self.idle_left
            self.canvas.itemconfigure(self.jinu, image=img)
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

        bubble = self.canvas.create_image(start_x, y, image=self.bubble_img)
        self.bubbles.append((bubble, self.direction))


    def updateBubbles(self):
        for b, d in self.bubbles[:]:
            self.canvas.move(b, 10 * d, 0)
            bx, by = self.canvas.coords(b)

            if bx < 0 or bx > 768:
                self.canvas.delete(b)
                self.bubbles.remove((b, d))
                continue

            if self.enemy_state == "normal":
                ex, ey = self.canvas.coords(self.enemy)

                if abs(bx - ex) < 40 and abs(by - ey) < 40:
                    self.enemy_state = "captured"
                    self.capture_start_time = time.time()

                    self.canvas.itemconfigure(self.enemy,
                                              image=self.enemy_captured_img)

                    self.canvas.delete(b)
                    self.bubbles.remove((b, d))
                    continue


    def updateEnemy(self):
        if self.enemy_state == "normal":
            self.canvas.move(self.enemy, self.enemy_dx, 0)
            ex, ey = self.canvas.coords(self.enemy)

            if ex < 50 or ex > 700:
                self.enemy_dx *= -1

        elif self.enemy_state == "captured":
            self.canvas.move(self.enemy, 0, -2)
            elapsed = time.time() - self.capture_start_time

            if elapsed > 3:  
                self.canvas.delete(self.enemy)
                self.enemy_state = "removed"


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
    EnemyBubbleHitTest()
