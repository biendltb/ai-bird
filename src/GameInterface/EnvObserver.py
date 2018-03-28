import pyscreenshot as ImageGrab
import numpy as np
import cv2
import time
import pyautogui
from PIL import Image

# take screenshot and calculate params
class EnvObserver:

    START_SCREEN_PART = '../data/screen_shoot/start.png'
    BIRD_UP_PART = '../data/screen_shoot/test.png'
    BIRD_DOWN_PART = '../data/screen_shoot/bird_down.png'
    TEST = '../data/screen_shoot/test1.png'

    # Screen set up
    TAP_TEXT_POS = (126, 384)
    GROUND_Y = 548
    START_BIRD_POS = (211, 336)
    BOTTOM_RIGHT_POS = (423, 604)

    RED_BIRD = (251, 56, 15)

    scr_root_pos = (-1, -1)

    def __init__(self):
        return

    def scr_capture(self):

        # detect start screen
        self.detect_start_screen()

        self.detect_bird_pos()


        #im.show()
        return

    def params_extract(self):

        return

    # detect start screen
    def detect_start_screen(self):

        im_gray = self.capture_grayscale()

        #load the part of start screen image
        part = cv2.imread(self.START_SCREEN_PART, cv2.IMREAD_GRAYSCALE)

        scr_found = False

        pos = (-1, -1)

        while not scr_found:

            start_time = time.time()
            pos = self.find_image(im_gray, part)

            if pos != (-1, -1):
                scr_found = True
            else:
                print('Waiting for start screen...')
                time.sleep(2)
                im_gray = self.capture_grayscale()

            #print('Execution time: ', time.time() - start_time)

        self.scr_root_pos = (pos[0] - self.TAP_TEXT_POS[0], pos[1] - self.TAP_TEXT_POS[1])

        print(self.scr_root_pos)

        return pos

    def detect_bird_pos(self):

        while True:

            start_time = time.time()

            bbox = (self.scr_root_pos[0] + 109, self.scr_root_pos[1],
                    self.scr_root_pos[0] + 109 + 4, self.scr_root_pos[1] + 548)

            bird_space = self.capture_color(bbox)

            bird_color = self.RED_BIRD


            pos = self.bird_search(bird_space, bird_color, (10, 10, 20))

            print('Time consumed: ', time.time() - start_time)
            if pos != (-1, -1):
                print(pos[1])

            #print('Sleep...')
            #time.sleep(2)
            #im = self.capture_color()



    def bird_search(self, bird_space, bird_color, threshold):
        h, w, d = bird_space.shape

        # search from bottom up
        for y in range(h-1, -1, -1):
            for x in range(0, w):
                # BGR mode
                if abs(bird_space[y][x][0] - bird_color[0]) < threshold[0] \
                        and abs(bird_space[y][x][1] - bird_color[1]) < threshold[1] \
                        and abs(bird_space[y][x][2] - bird_color[2]) < threshold[2]:
                    return (x, y)

        return (-1, -1)

    def find_image(self, im, tpl):

        res = cv2.matchTemplate(im, tpl, cv2.TM_CCOEFF_NORMED)

        threshold = 0.7

        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            p_y = loc[0][0]
            p_x = loc[1][0]
            return (p_x, p_y)

        return (-1, -1)

    # capture screenshot in grayscale
    def capture_grayscale(self):
        im_data = self.capture_color()
        im_gray =  cv2.cvtColor(im_data, cv2.COLOR_BGR2GRAY)

        return im_gray

    def capture_color(self, bbox = None):

        if bbox is None:
            im = ImageGrab.grab()
        else:
            im = ImageGrab.grab(bbox)

        im_data = np.asarray(im)
        im_data = cv2.cvtColor(im_data, cv2.COLOR_RGBA2RGB)

        return im_data
