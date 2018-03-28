import pyscreenshot as ImageGrab
import numpy as np
import cv2
import time
import _thread as thread
import pyautogui
from PIL import Image

# take screenshot and calculate params
class EnvObserver:

    START_SCREEN_PART = '../data/screen_shoot/start.png'
    BIRD_UP_PART = '../data/screen_shoot/test.png'
    BIRD_DOWN_PART = '../data/screen_shoot/bird_down.png'
    TEST = '../data/screen_shoot/test1.png'

    BIRD_TYPE = ['RED', 'GREEN', 'BLUE', 'PINK', 'PURPLE', 'YELLOW']

    # Screen set up
    TAP_TEXT_POS = (126, 384)
    GROUND_Y = 548
    START_BIRD_POS = (211, 336)
    BOTTOM_RIGHT_POS = (423, 604)

    RED_BIRD_RGB = (232, 54, 15)
    RED_DEVIATION = (25, 10, 15)
    GREEN_BIRD_RGB = (29, 220, 87)
    GREEN_DEVIATION = (5, 2, 5)
    BLUE_BIRD_RGB = (5, 172, 230)
    BLUE_DEVIATION = (5, 20, 22)
    PINK_BIRD_RGB = (211, 105, 105)
    PINK_DEVIATION = (7, 5, 5)
    PURPLE_BIRD_RGB = (177, 92, 205)
    PURPLE_DEVIATION = (10, 4, 10)
    YELLOW_BIRD_RGB = (250, 185, 30)
    YELLOW_DEVIATION = (4, 4, 40)

    GAME_OVER = (223, 216, 150)

    scr_root_pos = (-1, -1)

    curr_bird_type = 0

    reset_game = True

    thread_created = False

    def __init__(self):
        return

    def scr_capture(self):

        while True:

            if self.reset_game:
                # detect start screen
                self.detect_start_screen()
                self.reset_game = False

            if not self.thread_created:
                # start multi-threading tasks
                # NOTE: only put the name of function, not call function
                thread.start_new_thread(self.detect_game_over, ())

                thread.start_new_thread(self.detect_bird_pos, ())
                
                self.thread_created = True
            #
            # # self.detect_bird_pos()

        while 1:
            pass

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
                self.scr_root_pos = (pos[0] - self.TAP_TEXT_POS[0], pos[1] - self.TAP_TEXT_POS[1])
                self.detect_bird_type()
                print('BIRD COLOR:', self.BIRD_TYPE[self.curr_bird_type])
            else:
                print('Waiting for start screen...')
                time.sleep(2)
                im_gray = self.capture_grayscale()

            #print('Execution time: ', time.time() - start_time)


        print(self.scr_root_pos)

        return pos

    def detect_bird_pos(self):

        while True:

            start_time = time.time()

            bbox = (self.scr_root_pos[0] + 109, self.scr_root_pos[1],
                    self.scr_root_pos[0] + 109 + 4, self.scr_root_pos[1] + 548)

            bird_space = self.capture_color(bbox)

            #if self.curr_bird_type == 0:
            bird_color = self.RED_BIRD_RGB
            deviation = self.RED_DEVIATION

            if self.curr_bird_type == 1:
                bird_color = self.GREEN_BIRD_RGB
                deviation = self.GREEN_DEVIATION

            elif self.curr_bird_type == 2:
                bird_color = self.BLUE_BIRD_RGB
                deviation = self.BLUE_DEVIATION

            elif self.curr_bird_type == 3:
                bird_color = self.PINK_BIRD_RGB
                deviation = self.PINK_DEVIATION

            elif self.curr_bird_type == 4:
                bird_color = self.PURPLE_BIRD_RGB
                deviation = self.PURPLE_DEVIATION

            elif self.curr_bird_type == 1:
                bird_color = self.YELLOW_BIRD_RGB
                deviation = self.YELLOW_DEVIATION


            pos = self.bird_search(bird_space, bird_color, deviation)

            #print('Bird search time: ', time.time() - start_time)

            if pos != (-1, -1):
                print(pos[1])

    def detect_game_over(self):
        while True:
            start_time = time.time()

            bbox = (self.scr_root_pos[0] + 109, self.scr_root_pos[1],
                    self.scr_root_pos[0] + 109 + 1, self.scr_root_pos[1] + 604)

            v_line = self.capture_color(bbox)

            pos = self.bird_search(v_line, self.GAME_OVER, (3,3,3))

            if pos != (-1, -1):
                if not self.reset_game:
                    print('GAME OVER!!!')
                self.reset_game = True

            #print('Game over search time: ', time.time() - start_time)

    def detect_bird_type(self):

        bbox = (self.scr_root_pos[0] + 109, self.scr_root_pos[1] + 316,
                self.scr_root_pos[0] + 109 + 4, self.scr_root_pos[1] + 356)

        bird_space = self.capture_color(bbox)

        pos = self.bird_search(bird_space, self.YELLOW_BIRD_RGB, self.YELLOW_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 5
            return

        pos = self.bird_search(bird_space, self.RED_BIRD_RGB, self.RED_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 0
            return

        pos = self.bird_search(bird_space, self.GREEN_BIRD_RGB, self.GREEN_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 1
            return

        pos = self.bird_search(bird_space, self.BLUE_BIRD_RGB, self.BLUE_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 2
            return

        pos = self.bird_search(bird_space, self.PINK_BIRD_RGB, self.PINK_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 3
            return

        pos = self.bird_search(bird_space, self.PURPLE_BIRD_RGB, self.PURPLE_DEVIATION)
        if pos != (-1, -1):
            self.curr_bird_type = 4
            return

    def bird_search(self, bird_space, bird_color, deviation):
        h, w, d = bird_space.shape

        # search from bottom up
        for y in range(h-1, -1, -1):
            for x in range(0, w):
                # BGR mode
                if abs(bird_space[y][x][0] - bird_color[0]) < deviation[0] \
                        and abs(bird_space[y][x][1] - bird_color[1]) < deviation[1] \
                        and abs(bird_space[y][x][2] - bird_color[2]) < deviation[2]:
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
        #im_data = cv2.cvtColor(im_data, cv2.COLOR_BGRA2RGBA)
        im_data = cv2.cvtColor(im_data, cv2.COLOR_RGBA2RGB)

        return im_data
