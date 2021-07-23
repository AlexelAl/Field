from os import path

img_dir = path.join(path.dirname(__file__), 'assets')
save_maps = path.join(path.dirname(__file__), 'saved')


FPS = 30

BTN_SIZE = 40
ROWS = 15
COLS = 15
PAD = 1

BOT_SPEED = 3
BOT_ROTATE_SPEED = BOT_SPEED


# Задаем цвета
WHITE = (255, 255, 255)
GREY = (150,150,150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0,0,155)
WATER_BLUE = (82, 222, 190)
YELLOW = (255, 255, 0)


MIN_SIZE = (300,300)
WIDTH = BTN_SIZE * ROWS + PAD * ROWS + 90
HEIGHT =  BTN_SIZE * COLS + PAD * (COLS+1) + 90
if WIDTH < MIN_SIZE[0]:
    WIDTH = MIN_SIZE[0]
if HEIGHT < MIN_SIZE[1]:
    HEIGHT = MIN_SIZE[1]



CHOOSEN_STATE = 0

way = []
field = []
temp_field = []
old_new_water = []
new_water = []

status_clr = [WHITE, BLACK, BLUE, RED]
border = [[1,0],[-1,0],[0,1],[0,-1]]
rotations = {
             '(0, 1)': 'DOWN',
             '(1, 0)': 'RIGHT',
             '(-1, 0)': 'LEFT',
             '(0, -1)': 'UP'
            }

point_a = [0,0]
point_b = [ROWS-1, COLS-1]

saved_check = "saved"
saved_check1 = "Field"

save_file = save_maps + "\save.txt"


waiting = True
