import pygame  as pg
import sys
from os import path
import math
from GUI import *

input_bow = InLineTextBox((0, 0), 200)

img_dir = path.join(path.dirname(__file__), 'assets')

FPS = 30

ROWS = 30
COLS = 30
PAD = 1


BTN_SIZE = 20

MIN_SIZE = (300,300)


WIDTH = BTN_SIZE * COLS + PAD * COLS + 90
HEIGHT =  BTN_SIZE * ROWS + PAD * (ROWS+1) + 135 + PAD
if WIDTH < MIN_SIZE[0]:
    WIDTH = MIN_SIZE[0]
if HEIGHT < MIN_SIZE[1]:
    HEIGHT = MIN_SIZE[1]

# Задаем цвета
WHITE = (255, 255, 255)
GREY = (150,150,150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CHOOSEN_STATE = 0
ENDPOINT = None


way = []
field = []
old_new_water = []
new_water = []
status_clr = [WHITE, BLACK, BLUE, RED]
border = [[1,0],[-1,0],[0,1],[0,-1]]


# Создаем игру и окно
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH , HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
button_sprites = pg.sprite.Group()
cell_sprites = pg.sprite.Group()
select_sprites = pg.sprite.Group()

def CreateField():
    #Creating Field
    global field, ENDPOINT

    # Copy field from file or Make empty cells
    f = open('save.txt', 'r')
    for i in range(ROWS):
        field.append([])
        for j in range(COLS):
            stat = f.read(1)
            if stat == '':
                stat = '0'
            elif int(stat) == 3:
                ENDPOINT = (i,j)

            cell = Cell( screen, int( stat ), i * ( BTN_SIZE + PAD ), j * (BTN_SIZE + PAD), i, j )
            field[i].append( cell )
    f.close()

def watering(i,j):
    # fill near cells water

    global field, new_water
    if i >= ROWS or j >= COLS or field[i][j].status != 2:
        return
    for k in border:
        newi = i + k[0]
        newj = j + k[1]
        in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        if in_field and field[newi][newj].status == 0:
            field[newi][newj].status = 2
            new_water.append((newi,newj))
#def checkBorders(i,j):
#    for k in border:
    #    newi = i + k[0]
    #    newj = j + k[1]
    #    in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        #if in_field and field[newi][newj].status == 0:
            #return True
#    return False


def water_logic():

    #calling once per frame

    global field, new_water, old_new_water
    old_new_water = new_water
    new_water = []

    for i in old_new_water:
        watering(i[0], i[1])


def save():
    #save field to file and exit

    global field
    f = open('save.txt', 'w')
    for i in field:
        for j in i:
            f.write(str(j.status))
    f.close()
    sys.exit()

def clear():  #fill the field with empty cells
    for i in cell_sprites:
        i.fill(0)

def delwatering():
    #   delete  water
    for i in cell_sprites:
        if i.status == 2:
            i.fill(0)

def start_bot():
    global way,field
    i = -1
    j = -1
    while i != ROWS-1 and j != COLS-1:
        if i+1 < ROWS and (field[i+1][j].status == 0 or field[i+1][j].status == 3):
            i += 1
        if j+1 < COLS and (field[i][j+1].status == 0 or field[i][j+1].status == 3):
            j += 1
        print(i,"   ", j)
        way.append([i,j])
    print(way)
    for i in way:
        ii = i[0]
        jj = i[1]
        field[ii][jj].image.fill(RED)

# Перенес в начало ---вернул сюда, оно только для draw_text нужно---
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Так может тогда завернуть это в сам draw_text?
#Если не хочешь жёстко привязывать, можно сделать как аргумент с дефолтным значением
font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class SelectButton(pg.sprite.Sprite):
    def __init__(self,x,y,img_name,format,state):
        pg.sprite.Sprite.__init__(self)

        self.pressed_img = pg.image.load(path.join(img_dir, img_name + "_pressed" + format)).convert()
        self.unpressed_img = pg.image.load(path.join(img_dir, img_name + format)).convert()
        self.image = self.unpressed_img

        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)

        self.selected = False
        self.state = state

        all_sprites.add(self)
        select_sprites.add(self)

    def update(self,l_click):
        global select_cap_x,select_cap_y

        if self.selected:
            select_cap_x =  self.rect.x
            select_cap_y = self.rect.y

        self.image = self.unpressed_img
        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.pressed_img
            if self.selected:
                select_cap_x =  self.rect.x + 2
                select_cap_y = self.rect.y + 2

        if l_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.select_me()
    def select_me(self):
        global CHOOSEN_STATE
        self.unselect_all()
        self.selected = True
        CHOOSEN_STATE = self.state
        select_cap_x =  self.rect.x
        select_cap_y = self.rect.y
    def unselect_all(self):
        for i in select_sprites:
            i.selected = False



class Button(pg.sprite.Sprite):
    def __init__(self, surface, x, y, w, h, color, text, command):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.command = command
        self.text = text
        self.image = pg.Surface((w, h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.coords = (x, y)
        self.rect.midtop = self.coords

        draw_text(self.image, text, 26, w//2, 5, BLACK)

        all_sprites.add(self)
        button_sprites.add(self)

    def update(self,l_click):
        pressed = pg.mouse.get_pressed()
        if l_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.command()
        self.image.fill(self.color)
        self.rect.midtop = self.coords

        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            self.rect.x += 2
            self.rect.y += 2
            self.image.fill(WHITE)
        draw_text(self.image, self.text, 26, self.rect.width//2, 5, BLACK)


class Cell(pg.sprite.Sprite):
    # Можно упростить конструктор, передвая только i, j
    # А x, y рассчитывать уже тут. Один фиг по формуле рассчитываешь
    def __init__(self, surface, status, x, y, i, j):
        pg.sprite.Sprite.__init__(self)

        # Мне кажется можно оставить просто слово status мы же и так в Cell ---Можно, но сеll_status
        self.status = status                            # 0 - empty        Часто упоминается,и много менять !!!!!!!!!!!!!!!!!!!!!!
        self.image = pg.Surface((BTN_SIZE,BTN_SIZE))    # 1 - wall         Тут самое время познакомится с удобствами среды разработки)
        self.image.fill(status_clr[self.status])        # 2 - watering        Жми контрол ф, появится две строки - файнд и реплэйс.
        self.rect = self.image.get_rect()               # 3 - endpoint     в файнд - ЧТО нужно заменить, в реплайс НА ЧТО заменить)
        self.rect.x = x
        self.rect.y = y
        self.i = i
        self.j = j
        self.click_indx = False

        all_sprites.add(self)
        cell_sprites.add(self)
    def update(self,l_click):
        global new_water, status_clr

        if CHOOSEN_STATE != 2:
            status_clr[3] = status_clr[0]
        else:
            status_clr[3] = RED

        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()) and not self.click_indx:
            # Эммм, кажется ниже есть метод для этого) ----Тебе кажется----
            self.on_click()
            if self.status == 2:
                new_water.append((self.i,self.j))

        self.image.fill(status_clr[self.status])
    def on_click(self, color = None):
        global ENDPOINT
        if self.status == 3:
            ENDPOINT = None
        self.fill(CHOOSEN_STATE)
        self.click_indx = True

    def fill(self, state):
        self.status = state
        self.image.fill(status_clr[self.status])


# Переснес в начало --- Зачем? ------
#!!!!!!!!!!!!!ну вроде как глобальное объявление групп, это больше похоже на насройки и константы

# all_sprites = pg.sprite.Group()
# Button_sprites = pg.sprite.Group()
# Cell_sprites = pg.sprite.Group()



CreateField()

#BottomBar buttons

# surface, x, y, width, height, color, text, command
SaveBut = Button(screen, (WIDTH-90-PAD)//2, HEIGHT-45,
                WIDTH-90-PAD, 45, GREY, 'Save & Exit', save)
ClrBut =  Button(screen, (WIDTH-90-PAD)//2, HEIGHT-90-PAD,
                WIDTH-90-PAD, 45, GREY, 'Clear', clear)
DelwateringBut = Button(screen, (WIDTH-90-PAD)//2, HEIGHT-135-PAD*2,
                WIDTH-90-PAD, 45, GREY, 'Clear water', delwatering)

#SideBar buttons
SideBar = pg.Surface((90,HEIGHT))
SideBar.fill(GREY)

EmptySelect = SelectButton(WIDTH-45,2,'select_empty','.png',0)
EmptySelect.select_me()

WallSelect = SelectButton(WIDTH-45,54,'select_wall','.png' ,1)
WaterSelect = SelectButton(WIDTH-45,108,'select_water','.png',2)

StartBot = Button(screen, WIDTH-45, 162, 80, 50, (200,200,200), 'Start', start_bot)

select_cap_img = pg.image.load(path.join(img_dir, "select_highlight.png")).convert()
select_cap_img.set_colorkey(WHITE)
select_cap_x = EmptySelect.rect.x
select_cap_y = EmptySelect.rect.y

# Цикл игры
running = True
while running:
    l_click = False
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            l_click = True
            for i in cell_sprites:
                i.click_indx = False
        if event.type == pg.MOUSEBUTTONUP and event.button == 3 and CHOOSEN_STATE == 2:
            pos = pg.mouse.get_pos()
            i =  math.floor(pos[0] / (BTN_SIZE+PAD))
            j =  math.floor(pos[1] / (BTN_SIZE+PAD))
            if i >= 0 and j >= 0 and i < ROWS and j < COLS:
                field[i][j].status = 3
                field[i][j].fill(3)


    # Обновление
    water_logic()
    all_sprites.update(l_click)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(SideBar,(WIDTH-90,0))

    all_sprites.draw(screen)
    screen.blit(select_cap_img,(select_cap_x,select_cap_y))
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
