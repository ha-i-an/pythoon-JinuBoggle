from tkinter import *
import time
import pygame
import random


class JinuBubbleGame:
    def __init__(self):

        self.window = Tk()
        self.window.title("지누 보글")
        self.window.geometry("768x672")
        self.window.resizable(0, 0)

        self.canvas = Canvas(self.window, bg="black")
        self.canvas.pack(expand=True, fill=BOTH)

        self.keys = set()
        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.state = "menu"          
        self.menu_index = 0          
        self.game_overed = False     

        self.stage = 1
        self.max_stage = 3
        self.score = 0

        self.stage_score_table = {
            1: 10000,
            2: 15000,
            3: 20000
        }

        self.menu_bg = PhotoImage(file="99.JinuBubble/image/menu_bg.png")

        self.bg_stage1 = PhotoImage(file="99.JinuBubble/image/GNUcampus.png")
        self.bg_stage2 = PhotoImage(file="99.JinuBubble/image/GNUin.png")
        self.bg_stage3 = PhotoImage(file="99.JinuBubble/image/GNUlibrary.png")

        self.right1 = PhotoImage(file="99.JinuBubble/image/Rightwalk1.png")
        self.right2 = PhotoImage(file="99.JinuBubble/image/Rightwalk2.png")
        self.left1 = PhotoImage(file="99.JinuBubble/image/Leftwalk1.png")
        self.left2 = PhotoImage(file="99.JinuBubble/image/Leftwalk2.png")
        self.idle_right = PhotoImage(file="99.JinuBubble/image/jinu_right.png")
        self.idle_left = PhotoImage(file="99.JinuBubble/image/jinu_left.png")

        self.bubble_img = PhotoImage(file="99.JinuBubble/image/Bubble.png")
        self.enemy_img = PhotoImage(file="99.JinuBubble/image/beer.png")
        self.enemy_trapped_img = PhotoImage(file="99.JinuBubble/image/beer_bubble.png")
        self.enemy_dust_img = PhotoImage(file="99.JinuBubble/image/dust.png")
        self.enemy_dust_trapped_img = PhotoImage(file="99.JinuBubble/image/dust_bubble.png")
        self.enemy_phone_img = PhotoImage(file="99.JinuBubble/image/phone.png")
        self.enemy_phone_trapped_img = PhotoImage(file="99.JinuBubble/image/phone_bubble.png")



        self.score_500_img = None
        self.score_1000_img = None
        self.pop_img = None
        try:
            self.score_500_img = PhotoImage(file="99.JinuBubble/image/score_500.png")
        except:
            pass
        try:
            self.score_1000_img = PhotoImage(file="99.JinuBubble/image/score_1000.png")
        except:
            pass
        try:
            self.pop_img = PhotoImage(file="99.JinuBubble/image/pop.png")
        except:
            pass

        self.bonus_item_img = PhotoImage(file="99.JinuBubble/image/A.png")
        self.score_2000_img = PhotoImage(file="99.JinuBubble/image/score_2000.png")


        pygame.init()

        self.menu_bgm = "99.JinuBubble/sound/main.wav"
        self.game_bgm = "99.JinuBubble/sound/gametheme.wav"

        self.se_jump = pygame.mixer.Sound("99.JinuBubble/sound/jump.wav")
        self.se_trap = pygame.mixer.Sound("99.JinuBubble/sound/Bubble.wav")
        self.se_hit = pygame.mixer.Sound("99.JinuBubble/sound/hit.wav")

        self.se_gameover = pygame.mixer.Sound("99.JinuBubble/sound/gameover.wav")
        self.se_bonus = pygame.mixer.Sound("99.JinuBubble/sound/bonus.wav")
        self.se_gameclear = pygame.mixer.Sound("99.JinuBubble/sound/gameclear.wav")


        self.draw_menu()


        while True:
            try:
                if self.state == "game" and not self.game_overed:
                    self.update_game()
            except TclError:
                return

            self.window.after(33)
            self.window.update()


    def draw_menu(self):
        self.canvas.delete("all")
    
    
        self.canvas.create_image(
            0, 0,
            image=self.menu_bg,
            anchor=NW
        )

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu_bgm)
        pygame.mixer.music.play(-1)


        self.menu_panel = self.canvas.create_rectangle(
            210, 140,   
            560, 460,   
            fill="black",
            stipple="gray50",   
            outline=""
        )

        self.canvas.create_text(
            384, 180,
            text="지 누 보 글",
            font=("Times", 48, "bold"),
            fill="white"
        )

        self.menu_tutorial = self.canvas.create_text(
            384, 280,
            text="▶ 튜토리얼",
            font=("Times", 24, "bold"),
            fill="yellow"
        )

        self.menu_start = self.canvas.create_text(
            384, 340,
            text="  게임 시작",
            font=("Times", 24),
            fill="white"
        )

        self.menu_exit = self.canvas.create_text(
            384, 400,
            text="  게임 끝내기",
            font=("Times", 24),
            fill="white"
        )


        self.canvas.create_text(
            384, 470,
            text="↑ ↓ 선택 / Enter 결정",
            font=("Times", 16),
            fill="gray"
        )

    def update_menu(self):
        items = [
            (self.menu_tutorial, "튜토리얼"),
            (self.menu_start, "게임 시작"),
            (self.menu_exit, "게임 끝내기")
        ]

        for i, (item, text) in enumerate(items):
            if i == self.menu_index:
                self.canvas.itemconfigure(item, text=f"▶ {text}", fill="yellow")
            else:
                self.canvas.itemconfigure(item, text=f"  {text}", fill="white")


    def update_gameover_menu(self):
        if self.gameover_index == 0:
            self.canvas.itemconfigure(self.btn_restart, text="▶ 다시 시작하기", fill="yellow")
            self.canvas.itemconfigure(self.btn_menu, text="  메인으로 돌아가기", fill="white")
        else:
            self.canvas.itemconfigure(self.btn_restart, text="  다시 시작하기", fill="white")
            self.canvas.itemconfigure(self.btn_menu, text="▶ 메인으로 돌아가기", fill="yellow")

    def draw_tutorial(self):
        self.canvas.delete("all")

        self.canvas.create_rectangle(
            80, 80, 668, 560,
            fill="black", stipple="gray50", outline="white"
        )

        self.canvas.create_text(
            384, 130,
            font=("Times", 30, "bold"),
            fill="white",
            text="지누보글 튜토리얼"
        )

        story = (
            "지누의 시험 공부를 방해하러 오른쪽에서 날아오는\n"
            "여러 적들을 왼쪽끝에 도착하기 전에 버블로 가두며\n"
            "무사히 도서관에 도착해보자!\n\n"
            "Tip! 적들을 터뜨리면 더 많은 점수를 얻을 수 있어요!\n"
            "중간에 날아오는 비밀의 아이템을 획득해보세요!\n"
            "주의! 적들이 왼쪽끝에 도달하게 되면 피가 깎여요!\n"
            "왼쪽에 도달하기 전에 적들을 잡아주세요\n"
        )

        self.canvas.create_text(
            384, 300,
            font=("Times", 16),
            fill="white",
            text=story,
            justify="center"
        )

        controls = (
            "← → : 이동\n"
            "↑ : 점프\n"
            "Space : 버블 발사\n\n"
            "Enter / ESC : 메뉴로 돌아가기\n"
            "게임 중에는 ESC를 누르면 게임종료\n"
        )

        self.canvas.create_text(
            384, 500,
            font=("Times", 16, "bold"),
            fill="yellow",
            text=controls,
            justify="center"
        )




    def start_game(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="white")


        if self.stage == 1:
            self.current_bg = self.bg_stage1
        elif self.stage == 2:
            self.current_bg = self.bg_stage2
        else:
            self.current_bg = self.bg_stage3  

        self.canvas.create_image(0, 0, image=self.current_bg, anchor=NW)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game_bgm)
        pygame.mixer.music.play(-1)

        self.stage_clear_score = self.stage_score_table.get(self.stage, 10000)

        self.state = "game"
        self.game_overed = False

        self.score = 0

        self.life = getattr(self, "life", 5)
        self.life = min(5, max(0, self.life))


        self.invincible = False
        self.invincible_start = 0
        self.invincible_time = 2.0
        self.blink_delay = 0.15
        self.last_blink_time = 0
        self.jinu_visible = True


        self.platforms = [
            self.canvas.create_rectangle(120, 560, 360, 580, fill="gray"),
            self.canvas.create_rectangle(420, 440, 660, 460, fill="gray"),
            self.canvas.create_rectangle(80, 320, 320, 340, fill="gray"),
            self.canvas.create_rectangle(300, 200, 620, 220, fill="gray")
        ]


        self.jinu_hitbox = self.canvas.create_oval(
            180, 520, 220, 560, outline="", fill=""
        )
        self.jinu = self.canvas.create_image(200, 540, image=self.idle_right)

        self.direction = 1
        self.is_jumping = False
        self.jump_power = 0
        self.gravity = 1

        self.frame = 0
        self.last_time = time.time()
        self.delay = 0.15


        self.bubbles = []
        self.last_fire_time = 0
        self.fire_delay = 0.25


        self.normal_enemies = []
        self.trapped_enemies = []
        self.enemy_half = 18
        self.spawn_levels = [540, 420, 300, 180]
        self.last_enemy_time = 0


        self.bonus_items = []
        self.last_bonus_time = time.time()
        self.bonus_spawn_count = 0
        self.max_bonus_per_stage = random.randint(1, 2)
        self.next_bonus_delay = random.uniform(6, 10)


        if self.stage == 1:
            self.enemy_delay = 2.0
            self.enemy_speed = 4
        elif self.stage == 2:
            self.enemy_delay = 1.6
            self.enemy_speed = 5
        else:
            self.enemy_delay = 1.3
            self.enemy_speed = 6

        self.score_text = self.canvas.create_text(
            110, 30,
            font=("Times", 16, "bold"),
            fill="yellow",
            text=f"SCORE: {self.score} / {self.stage_clear_score}"
        )

        self.life_text = self.canvas.create_text(
            700, 30, font=("Times", 16, "bold"),
            fill="red", text=f"LIFE: {self.life}"
        )
        self.stage_text = self.canvas.create_text(
            384, 30, font=("Times", 16, "bold"),
            fill="white", text=f"STAGE {self.stage}"
        )

        self.canvas.create_text(
            384, 60, font=("Times", 15, "italic", "bold"),
            fill="black",
            text="← → 이동 / ↑ 점프 / Space : 버블"
        )


    def update_game(self):
        self.update_movement()
        self.update_invincible()
        self.update_animation()
        self.update_bubbles()
        self.update_normal_enemies()
        self.update_trapped_enemies()
        self.spawn_bonus_if_needed()
        self.update_bonus_items()


        if self.score >= self.stage_clear_score:
            self.stage_clear()


    def update_movement(self):
        if 37 in self.keys:
            self.canvas.move(self.jinu_hitbox, -5, 0)
            self.direction = -1
        if 39 in self.keys:
            self.canvas.move(self.jinu_hitbox, 5, 0)
            self.direction = 1

        if self.is_jumping:
            self.canvas.move(self.jinu_hitbox, 0, -self.jump_power)
            self.jump_power -= self.gravity

        x1, y1, x2, y2 = self.canvas.coords(self.jinu_hitbox)
        bottom = y2
        center_x = (x1 + x2) / 2
        on_platform = False

        for p in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(p)
            if px1 <= center_x <= px2 and bottom >= py1 and y1 < py1:
                self.canvas.move(self.jinu_hitbox, 0, -(bottom - py1))
                self.is_jumping = False
                self.jump_power = 0
                on_platform = True
                break

        if not on_platform and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = 0

        if bottom > 700:
            self.canvas.move(self.jinu_hitbox, 0, -(bottom + 40))
            self.is_jumping = True
            self.jump_power = -1

        x1, y1, x2, y2 = self.canvas.coords(self.jinu_hitbox)
        self.canvas.coords(self.jinu, (x1 + x2) / 2, (y1 + y2) / 2)


    def update_animation(self):
        moving = (37 in self.keys) or (39 in self.keys)
        now = time.time()

        if not moving:
            img = self.idle_right if self.direction == 1 else self.idle_left
            self.canvas.itemconfigure(self.jinu, image=img)
            return

        if now - self.last_time > self.delay:
            self.last_time = now
            self.frame = (self.frame + 1) % 2
            img = self.right1 if self.direction == 1 else self.left1
            if self.frame == 1:
                img = self.right2 if self.direction == 1 else self.left2
            self.canvas.itemconfigure(self.jinu, image=img)


    def fireBubble(self):
        x1, y1, x2, y2 = self.canvas.coords(self.jinu_hitbox)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        start_x = cx + 30 if self.direction == 1 else cx - 30

        bubble = self.canvas.create_image(start_x, cy, image=self.bubble_img)
        self.bubbles.append((bubble, self.direction))

    def add_score(self, value):
        self.score += value
        if self.score < 0:
            self.score = 0

        self.canvas.itemconfigure(
            self.score_text,
            text=f"SCORE: {self.score} / {self.stage_clear_score}"
        )

    def show_popup(self, x, y, img=None, text=None):
        if img is not None:
            item = self.canvas.create_image(x, y, image=img)
        else:
            item = self.canvas.create_text(x, y, text=text, font=("Times", 14, "bold"), fill="yellow")

        self.window.after(600, lambda: self.canvas.delete(item))

    def update_bubbles(self):
        for b, d in self.bubbles[:]:
            self.canvas.move(b, 10 * d, 0)
            bx, by = self.canvas.coords(b)

            if bx < 0 or bx > 768:
                self.canvas.delete(b)
                self.bubbles.remove((b, d))
                continue

            for enemy, enemy_type in self.normal_enemies[:]:
                ex, ey = self.canvas.coords(enemy)

                if abs(bx - ex) < 20 and abs(by - ey) < 20:
                    self.catch_enemy(enemy, enemy_type)


                    self.add_score(500)
                    if self.score_500_img:
                        self.show_popup(ex, ey - 22, img=self.score_500_img)
                    else:
                        self.show_popup(ex, ey - 22, text="500")

                    self.canvas.delete(b)
                    self.bubbles.remove((b, d))

                    self.se_trap.play()
                    break


    def catch_enemy(self, enemy, enemy_type):
        self.normal_enemies.remove((enemy, enemy_type))
        self.trapped_enemies.append((enemy, enemy_type))

        if enemy_type == "beer":
            self.canvas.itemconfigure(enemy, image=self.enemy_trapped_img)
        elif enemy_type == "dust":
            self.canvas.itemconfigure(enemy, image=self.enemy_dust_trapped_img)
        else:  
            self.canvas.itemconfigure(enemy, image=self.enemy_phone_trapped_img)


    def update_trapped_enemies(self):
        jx1, jy1, jx2, jy2 = self.canvas.coords(self.jinu_hitbox)

        for enemy, enemy_type in self.trapped_enemies[:]:
            self.canvas.move(enemy, 0, -2)
            ex, ey = self.canvas.coords(enemy)

            if ey + self.enemy_half < 0:
                self.canvas.delete(enemy)
                self.trapped_enemies.remove((enemy, enemy_type))
                continue

            e_left = ex - self.enemy_half
            e_right = ex + self.enemy_half
            e_top = ey - self.enemy_half
            e_bottom = ey + self.enemy_half

            if (jx1 < e_right and jx2 > e_left and
                jy1 < e_bottom and jy2 > e_top):

                if self.pop_img:
                    self.show_popup(ex, ey, img=self.pop_img)
                else:
                    self.show_popup(ex, ey, text="POP!")

                self.add_score(1000)
                if self.score_1000_img:
                    self.show_popup(ex, ey - 22, img=self.score_1000_img)
                else:
                    self.show_popup(ex, ey - 22, text="1000")

                self.canvas.delete(enemy)
                self.trapped_enemies.remove((enemy, enemy_type))


    def spawn_enemy(self):
        y = random.choice(self.spawn_levels)


        if self.stage == 1:
            enemy_type = "beer"
        elif self.stage == 2:
            enemy_type = random.choice(["beer", "dust"])
        else: 
            enemy_type = random.choice(["dust", "phone"])


        if enemy_type == "beer":
            img = self.enemy_img
        elif enemy_type == "dust":
            img = self.enemy_dust_img
        else:  
            img = self.enemy_phone_img

        enemy = self.canvas.create_image(780, y, image=img)
        self.normal_enemies.append((enemy, enemy_type))


    def update_normal_enemies(self):
        now = time.time()
        if now - self.last_enemy_time > self.enemy_delay:
            self.last_enemy_time = now
            self.spawn_enemy()

        jx1, jy1, jx2, jy2 = self.canvas.coords(self.jinu_hitbox)

        for enemy, enemy_type in self.normal_enemies[:]:
            self.canvas.move(enemy, -self.enemy_speed, 0)
            ex, ey = self.canvas.coords(enemy)


            if (jx1 < ex + self.enemy_half and jx2 > ex - self.enemy_half and
                jy1 < ey + self.enemy_half and jy2 > ey - self.enemy_half):
                self.lose_life()

            if ex + self.enemy_half < 0:
                self.canvas.delete(enemy)
                self.normal_enemies.remove((enemy, enemy_type))
                self.lose_life()


    def spawn_bonus_if_needed(self):
        now = time.time()
        if self.bonus_spawn_count < self.max_bonus_per_stage:
            if now - self.last_bonus_time > self.next_bonus_delay:
                y = random.choice(self.spawn_levels)
                item = self.canvas.create_image(780, y, image=self.bonus_item_img)
                self.bonus_items.append(item)
                self.bonus_spawn_count += 1
                self.last_bonus_time = now
                self.next_bonus_delay = random.uniform(6, 10)


    def update_bonus_items(self):
        jx1, jy1, jx2, jy2 = self.canvas.coords(self.jinu_hitbox)

        for item in self.bonus_items[:]:
            self.canvas.move(item, -7, 0)  
            ix, iy = self.canvas.coords(item)

            if ix < -30:
                self.canvas.delete(item)
                self.bonus_items.remove(item)
                continue

            if (jx1 < ix + 20 and jx2 > ix - 20 and
                jy1 < iy + 20 and jy2 > iy - 20):

                try:
                    self.se_bonus.play()
                except:
                    pass

                self.add_score(2000)
                self.show_popup(ix, iy - 22, img=self.score_2000_img)

                self.canvas.delete(item)
                self.bonus_items.remove(item)



    def lose_life(self):
        if self.invincible or self.game_overed:
            return

        try:
            self.se_hit.play()
        except:
            pass

        self.life -= 1

        if self.life < 0:
            self.life = 0

        self.canvas.itemconfigure(self.life_text, text=f"LIFE: {self.life}")

        if self.life == 0:
            self.game_over()
            return

        self.invincible = True
        self.invincible_start = time.time()
        self.last_blink_time = time.time()
        self.jinu_visible = True

    def update_invincible(self):
        if not self.invincible:
            return

        now = time.time()
        if now - self.invincible_start > self.invincible_time:
            self.invincible = False
            self.canvas.itemconfigure(self.jinu, state="normal")
            return

        if now - self.last_blink_time > self.blink_delay:
            self.last_blink_time = now
            self.jinu_visible = not self.jinu_visible
            self.canvas.itemconfigure(
                self.jinu,
                state="normal" if self.jinu_visible else "hidden"
            )

    def game_over(self):
        self.game_overed = True
        self.state = "game_over"

        pygame.mixer.music.stop()

        try:
            self.se_gameover.play()
        except:
            pass


        self.gameover_index = 0  

        self.canvas.create_rectangle(
            150, 230, 618, 460,
            fill="black", stipple="gray50", outline="white"
        )

        self.canvas.create_text(
            384, 270,
            font=("Times", 36, "bold"),
            fill="red",
            text="GAME OVER"
        )

        self.btn_restart = self.canvas.create_text(
            384, 350,
            font=("Times", 22, "bold"),
            fill="yellow",
            text="▶ 다시 시작하기"
        )

        self.btn_menu = self.canvas.create_text(
            384, 400,
            font=("Times", 22),
            fill="white",
            text="  메인으로 돌아가기"
        )



    def stage_clear(self):
        if self.state != "game":
            return

        self.state = "stage_clear"
        self.game_overed = True  

        self.canvas.create_rectangle(120, 240, 648, 430, fill="black", outline="white")
        self.canvas.create_text(
            384, 290,
            font=("Times", 28, "bold"),
            fill="white",
            text=f"STAGE {self.stage} CLEAR!"
        )
        self.canvas.create_text(
            384, 350,
            font=("Times", 18, "bold"),
            fill="yellow",
            text="Enter 키를 누르면 다음 스테이지"
        )

    def next_stage(self):
        self.stage += 1


        if self.stage > self.max_stage:
            self.state = "all_clear"
            self.game_overed = True

            pygame.mixer.music.stop()

            try:
                self.se_gameclear.play()
            except:
                pass

            self.canvas.delete("all")

            self.canvas.create_rectangle(
                120, 240, 648, 430,
                fill="black",
                stipple="gray50",
                outline="white"
            )

            self.canvas.create_text(
                384, 300,
                font=("Times", 30, "bold"),
                fill="yellow",
                text="ALL STAGE CLEAR!"
            )

            self.canvas.create_text(
                384, 360,
                font=("Times", 16),
                fill="white",
                text="Enter 키를 누르면 메인화면으로 돌아갑니다"
            )

            return


        self.life = min(5, self.life + 1)
        self.state = "game"
        self.game_overed = False
        self.start_game()


    def keyPressHandler(self, event):
        self.keys.add(event.keycode)

        if self.state == "menu":
            if event.keycode == 38: 
                self.menu_index = (self.menu_index - 1) % 3
                self.update_menu()
            elif event.keycode == 40: 
                self.menu_index = (self.menu_index + 1) % 3
                self.update_menu()
            elif event.keycode == 13:  
                if self.menu_index == 0:     
                    self.state = "tutorial"
                    self.draw_tutorial()
                elif self.menu_index == 1:    
                    self.stage = 1
                    self.life = 5
                    self.start_game()
                else:                        
                    self.onClose()
            return

        if self.state == "tutorial":
            if event.keycode in (13, 27):  
                self.state = "menu"
                self.menu_index = 0
                self.draw_menu()
            return


        if self.state == "stage_clear":
            if event.keycode == 13:
                self.next_stage()
            if event.keycode == 27:
                self.onClose()
            return

        if self.state == "all_clear":
            if event.keycode == 13:  
                self.state = "menu"
                self.menu_index = 0
                self.draw_menu()
            elif event.keycode == 27:
                self.onClose()
            return


        if self.state == "game_over":
            if event.keycode == 38: 
                self.gameover_index = (self.gameover_index - 1) % 2
                self.update_gameover_menu()
            elif event.keycode == 40:  
                self.gameover_index = (self.gameover_index + 1) % 2
                self.update_gameover_menu()
            elif event.keycode == 13:  
                if self.gameover_index == 0:
                    self.stage = 1
                    self.life = 5
                    self.score = 0
                    self.start_game()
                else:
                    self.state = "menu"
                    self.menu_index = 0
                    self.draw_menu()
            return


        if event.keycode == 27:
            self.onClose()
            return

        if self.game_overed:
            return

        if event.keycode == 38 and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = 18
            self.se_jump.play()

        if event.keycode == 32:
            if time.time() - self.last_fire_time > self.fire_delay:
                self.last_fire_time = time.time()
                self.fireBubble()

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

    def onClose(self):
        try:
            pygame.quit()
        except:
            pass
        try:
            self.window.destroy()
        except:
            pass


if __name__ == "__main__":
    JinuBubbleGame()
