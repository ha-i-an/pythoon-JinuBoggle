from tkinter import *
import pygame
import sys

class GameSound:
    def __init__(self):
        self.window = Tk()
        self.window.title("지누 버블 - 사운드 테스트")
        self.window.geometry("768x672")
        self.window.resizable(0, 0)

        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)


        pygame.init()

        pygame.mixer.music.load("03.Sound/gametheme.wav")
        pygame.mixer.music.play(-1) 

        self.canvas.create_text(
            384, 540, font="Times 15 italic bold",
            text="A: 버블 소리 / S: 점프 소리"
        )
        self.canvas.create_text(
            384, 580, font="Times 15 italic bold",
            text="ESC 종료"
        )


        self.sounds = pygame.mixer
        self.sounds.init()

        self.ch1 = pygame.mixer.Channel(0)  
        self.ch2 = pygame.mixer.Channel(1)  

        self.s_bubble = self.sounds.Sound("03.Sound/bubble.wav")
        self.s_jump = self.sounds.Sound("03.Sound/jump.wav")

        while True:
            self.window.after(33)
            self.window.update()

    def keyReleaseHandler(self, event):
        pass

    def keyPressHandler(self, event):
        print(event.keycode)

        if event.keycode == 27:
            self.onClose()

        elif event.keycode == 65:  
            if not self.ch1.get_busy():
                self.ch1.play(self.s_bubble)

        elif event.keycode == 83: 
            if not self.ch2.get_busy():
                self.ch2.play(self.s_jump)

    def onClose(self):
        pygame.mixer.music.stop()
        pygame.quit()
        self.window.destroy()


if __name__ == '__main__':
    GameSound()
