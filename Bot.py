import ctypes
import time
import PIL.Image
import PIL.ImageGrab
import keyboard
import mss
import winsound
from tkinter import *

PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 60
GRABZONE = 5
GRABZONEUP = "ctrl + up"
GRABZONEDOWN = "ctrl + down"
TRIGGER_KEY = "ctrl + alt"
COLOR_KEY = "alt"
MODECHANGEKEY = "ctrl + tab"
CURRENTMODE = "SLOW"

S_HEIGHT, S_WIDTH = PIL.ImageGrab.grab().size

#TRIGGERBOT
class FoundEnemy(Exception):
    pass

class TriggerBot:
    def __init__(self):
        self.toggled = False
        self.mode = 0
        self.last_reac = 0

    def toggle(self):
        self.toggled = not self.toggled

    def switch(self):
        if self.mode != 2:
            self.mode += 1
        else:
            self.mode = 0
        if self.mode == 0:
            CURRENTMODE = "SLOW (0.5/CPS)"
            winsound.Beep(200, 200)
        if self.mode == 1:
            CURRENTMODE = "MEDIUM (0.25/CPS)"
            winsound.Beep(500, 200)
        if self.mode == 2:
            CURRENTMODE = "FAST (0.12/CPS)"
            winsound.Beep(700, 200)
            time.sleep(0.1)
        print_banner(self)

    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.25)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def approx(self, r, g, b):
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE

    def grab(self):
        with mss.mss() as sct:
            bbox = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE),
                    int(S_WIDTH / 2 + GRABZONE))
            sct_img = sct.grab(bbox)
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self):
        start_time = time.time()
        pmap = self.grab()
        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.approx(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 1000)
            self.click()
            if self.mode == 0:
                time.sleep(0.5)
            if self.mode == 1:
                time.sleep(0.25)
            if self.mode == 2:
                time.sleep(0.12)
            print_banner(self)


def print_banner(bot: TriggerBot):
    print("Valorant TriggerBot - AustXnSheep")
    print("====== controls ======")
    print("TRIGGER: " + TRIGGER_KEY)
    print("ENLARGE GRABZONE: " + GRABZONEUP)
    print("REDUCE GRABZONE: " + GRABZONEDOWN)
    print("====== INFO ======")
    print("GRABZONE: " + str(GRABZONE))
    print("SHOTSPEED: " + str(CURRENTMODE))


if __name__ == "__main__":
    bot = TriggerBot()
    print_banner(bot)
    while True:
        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            print_banner(bot)
            if bot.toggled:
                winsound.Beep(440, 75)
                winsound.Beep(700, 100)
            else:
                winsound.Beep(440, 75)
                winsound.Beep(200, 100)
            while keyboard.is_pressed(TRIGGER_KEY):
                pass
        if keyboard.is_pressed(GRABZONEUP):
            GRABZONE = GRABZONE + 1
            print_banner(bot)
            winsound.Beep(440, 75)
            winsound.Beep(700, 100)
        if keyboard.is_pressed(GRABZONEDOWN):
            GRABZONE = GRABZONE - 1
            print_banner(bot)
            winsound.Beep(440, 75)
            winsound.Beep(200, 100)
        if keyboard.is_pressed(MODECHANGEKEY):
            bot.switch()
            print_banner(bot)
        if bot.toggled:
            bot.scan()

            # switch(self)
