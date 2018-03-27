import pyscreenshot as ImageGrab
import numpy as np
import cv2
import time
import pyautogui
from PIL import Image

# take screenshot and calculate params
class EnvObserver:

    START_SCREEN_PART = '../data/screen_shoot/start.png'

    # Screen set up
    TAP_TEXT_POS = (126, 384)
    GROUND_Y = 548
    START_BIRD_POS = (211, 336)
    BOTTOM_RIGHT_POS = (423, 604)

    def __init__(self):
        return

    def scr_capture(self):
        im = ImageGrab.grab()

        self.detect_start_screen()

        #im.show()
        return

    def params_extract(self):

        return

    # detect start screen
    def detect_start_screen(self):

        im_gray = self.capture_grayscale()

        # test by load image from file
        # im = cv2.imread(self.START_SCREEN_PART_TEST, cv2.IMREAD_COLOR)
        # im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        #load the part of start screen image
        part = cv2.imread(self.START_SCREEN_PART, cv2.IMREAD_GRAYSCALE)
        #part = cv2.cvtColor(part_color, cv2.COLOR_BGR2GRAY)

        scr_found = False

        while not scr_found:

            start_time = time.time()
            try:
                x, y = self.find_image(im_gray, part)
                print(x, y)
                scr_found = True
            except ValueError:
                print('Sleep...')
                time.sleep(2)
                im_gray = self.capture_grayscale()

            print('Execution time: ', time.time() - start_time)


        #cv2.imshow('gray_image', part)
        #cv2.waitKey(0)

    def find_image(self, im, tpl):

        res = cv2.matchTemplate(im, tpl, cv2.TM_CCOEFF_NORMED)

        threshold = 0.9

        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            p_y = loc[0][0]
            p_x = loc[1][0]
            return (p_x, p_y)

        return (-1, -1)

    # capture screenshot in grayscale
    def capture_grayscale(self):
        # capture the screen and convert to gray scale
        im = ImageGrab.grab()
        im_data = np.asarray(im)
        im_gray =  cv2.cvtColor(im_data, cv2.COLOR_BGR2GRAY)

        return im_gray
