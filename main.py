from easygui import fileopenbox
from easygui import filesavebox
import pygame  as pg
import sys
import math
from os import path
import random

from set import *
from init import *


def CreateField():
    global field, temp_field

    # Copy field from file or Make empty cells
    for i in range(ROWS):
        field.append([])
        for j in range(COLS):
            cell = Cell( screen, 0, i * ( BTN_SIZE + PAD ), j * (BTN_SIZE + PAD), i, j )
            field[i].append( cell )

    coords = []
    with open(str(save_file) , 'r', encoding="UTF-8") as f:
        try:
            for ex in f.read().split():
                coords.append(int(ex))
        except UnicodeDecodeError:
            f.close()
        except PermissionError:
            f.close()
    f.close()
    c = 0
    for i in range(len(coords)):
        if c % 2 == 0:
            try:
                field[ coords[c] ][ coords[c+1] ].status = 1
            except:
                pass
        c += 1

    for i in range(ROWS):
        temp_field.append([])
        for j in range(COLS):
            temp_field[i].append(TempCell(i,j,field[i][j].status))   # create table of cells and visual objeckts
def delete_field():
    global field, temp_field
    field = []
    temp_field = []
    for i in cell_sprites:
        i.kill()
    for i in bot_sprites:
        i.kill()
    delwatering()

def open_file():
    path_save = ""

    path_save = fileopenbox(default = "C:\Field\saved\*.txt")
    if path_save == "." or (path_save.find(saved_check) == -1 and save_file.find(saved_check1) == -1):
        path_save = save_file
    return path_save   # return path to choosen file
def change_file():
    global save_file

    new_save = open_file()
    if save_file != new_save:
        save_file = new_save
        delete_field()
        CreateField()   # change choosen file
def create_file():
    global save_file
    try:
        save_file = filesavebox(default = "C:\Field\saved\*.txt") + ".txt"
        f = open(save_file, "w")
        f.close()
        delete_field()
        CreateField()
    except TypeError:
        pass


def edit():
    close_start_screen()
    pg.display.set_caption("Edit")
def run():
    close_start_screen()
    pg.display.set_caption("Run")

def watering(i,j):
    # fill near cells water

    global field, new_water
    if i >= ROWS or j >= COLS or temp_field[i][j].status != 2:
        return

    childStep = temp_field[i][j].getStep() + 1

    for k in border:
        newi = i + k[0]
        newj = j + k[1]

        in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        if not in_field:
            continue
        currCell = temp_field[newi][newj]

        if currCell.status == 0 or ( currCell.status == 2 and currCell.getStep() > childStep ):
            currCell.setParent(i,j)
            currCell.setStep(childStep)
            new_water.append((newi,newj))

            currCell.status = 2   # fill near cells by water
def water_logic():

    global field, new_water, old_new_water

    old_new_water = new_water
    new_water = []


    for i in old_new_water:
        watering(i[0], i[1])   # fill field with function "watering"
def delwatering():
    #   delete  water
    for i in cell_sprites:
        if i.status == 2 or i.status == 3:
            i.fill(0)
            i.resetWay()
    for i in temp_field:
        for j in i:
            if j.status == 2 or j.status == 3:
                j.status == 0
                j.resetWay()  # clear all water cells


def save():
    #save field to file and exit

    global field
    f = open(save_file, 'w')
    for i in field:
        for j in i:
            if j.status == 1:
                f.write(str(j.i))
                f.write(" ")
                f.write(str(j.j))
                f.write(" ")
    f.close()   # save field to save_file
def clear():
    for i in cell_sprites:
        i.fill(0)
    for i in temp_field:
        for j in i:
            j.status = 0
            j.resetWay()  # fill the field with empty cells

def start_bot():
    global temp_field, point_a, point_b
    delwatering()
    for i in range(ROWS):
        for j in range(COLS):
            temp_field[i][j].status = field[i][j].status

    new_water.append(point_b)
    temp_field[ point_b[0] ][ point_b[1] ].status = 2

    water_logic()
    while len(new_water) != 0 and temp_field[ point_a[0] ][ point_a[1] ].status != 2:
        water_logic()

    run = True
    cell = point_a
    way = [count_xy(point_a)]
    while run:
        try:
            if len(cell) == 0 or temp_field[ cell[0] ][ cell[1] ].getStep() == 0:
                run = False


            temp_field[ cell[0] ][ cell[1] ].status = 3
            cell = temp_field[ cell[0] ][ cell[1] ].getParent()

            way.append(count_xy(cell))
            temp_field[ cell[0] ][ cell[1] ].status = 3

        except IndexError:
            print('Error: No way to endpoint')
            return

    bot = Bot(point_a[0],point_a[1], way)

    bot_sprites.add(bot)
    all_sprites.add(bot)   # make bot and it's way

def count_ij(xy):
    i =  math.floor(xy[0] / (BTN_SIZE+PAD))
    j =  math.floor(xy[1] / (BTN_SIZE+PAD))
    return (i,j)
def count_xy(ij):
    x = ij[0] * (BTN_SIZE + PAD )
    y = ij[1] * (BTN_SIZE + PAD )
    return [x,y]
def count_coof(x):
    if x >= 0:
        return 1
    else:
        return -1

def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def start_screen():
    global waiting
    screen.blit(BACKGROUND, (0,0))

    editor_mode = Button(screen,WIDTH//4, HEIGHT//2 - 40, WIDTH//4,
                         80, BLUE , "Edit", 30, edit, YELLOW,DARK_BLUE)
    run_mode = Button(screen,WIDTH-WIDTH//4, HEIGHT//2 - 40, WIDTH//4,
                      80, BLUE , "Run",30, run, YELLOW,DARK_BLUE)

    waiting_sprites.add(editor_mode)
    waiting_sprites.add(run_mode)
    pg.display.flip()

    waiting = True
    while waiting:
        l_click = False
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                l_click = True
        screen.blit(BACKGROUND, (0,0))
        waiting_sprites.update(l_click)
        waiting_sprites.draw(screen)
        pg.display.flip()

def close_start_screen():
    global waiting
    waiting = False
    for i in waiting_sprites:
        i.kill()
    CreateField()
def return_start_screen():
    delete_field()
    start_screen()


class Button(pg.sprite.Sprite):
    def __init__(self, surface, x, y, w, h, color, text, text_size,
                 command, text_color = BLACK, pressed_clr = WHITE):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.command = command
        self.text = text
        self.text_size = text_size
        self.image = pg.Surface((w, h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.coords = (x, y)
        self.rect.midtop = self.coords
        self.text_color = text_color
        self.pressed_clr = pressed_clr

        draw_text(self.image, text, 26, w//2, 5, BLACK)

    def update(self,l_click):
        pressed = pg.mouse.get_pressed()
        if l_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.command()
        self.image.fill(self.color)
        self.rect.midtop = self.coords

        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            self.rect.x += 2
            self.rect.y += 2
            self.image.fill(self.pressed_clr)
        draw_text(self.image, self.text, self.text_size , self.rect.width//2,
                  self.rect.height//2 - self.text_size, self.text_color)

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
        global select_cap_x,select_cap_y, CHOOSEN_STATE

        if self.selected:
            select_cap_x =  self.rect.x
            select_cap_y = self.rect.y

        self.image = self.unpressed_img
        pressed = pg.mouse.get_pressed()
        keystate = pg.key.get_pressed()

        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.pressed_img
            if self.selected:
                select_cap_x =  self.rect.x + 2
                select_cap_y = self.rect.y + 2

        if keystate[pg.K_1]:
            CHOOSEN_STATE = 0
        elif keystate[pg.K_2]:
            CHOOSEN_STATE = 1
        elif keystate[pg.K_3]:
            CHOOSEN_STATE = 2
        if self.state == CHOOSEN_STATE:
            self.unselect_all()
            self.select_me()

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

class Cell(pg.sprite.Sprite):

    def __init__(self, surface, status, x, y, i, j):
        pg.sprite.Sprite.__init__(self)

        self.status = status                            # 0 - empty
        self.image = pg.Surface((BTN_SIZE,BTN_SIZE))    # 1 - wall
        self.image.fill(status_clr[self.status])        # 2 - watering        
        self.rect = self.image.get_rect()               # 3 - way marker
        self.rect.x = x                                 # 4 - endpoint
        self.rect.y = y
        self.i = i
        self.j = j
        self.click_indx = False

        self._parent = []
        self._step = -1
        all_sprites.add(self)
        cell_sprites.add(self)

    # Хранить откуда пришли
    def setParent(self, i, j):
        self._parent = [i, j]
    def getParent(self):
        return self._parent

    # Хранит номер шага
    def setStep(self, x):
        self._step = x
    def getStep(self):
        return self._step

    # Сбрасывает параметры пути
    def resetWay(self):
        self._parent = []
        self._step = -1


    def update(self,l_click):
        global new_water, status_clr

        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()) and not self.click_indx and not CHOOSEN_STATE==2:

            delwatering()
            self.on_click(l_click,r_click)

        else:
            self.image.fill(status_clr[self.status])
    def on_click(self,l_click,r_click):

        self.fill(CHOOSEN_STATE)
        self.click_indx = True

    def fill(self, state):
        self.status = state
        self.image.fill(status_clr[self.status])

class TempCell():
    def __init__(self, i, j, status):
        self.i = i
        self.j = j
        self._parent = []
        self._step = -1
        self.status = status

    # Хранить откуда пришли
    def setParent(self, i, j):
        self._parent = [i, j]
    def getParent(self):
        return self._parent

    # Хранит номер шага
    def setStep(self, x):
        self._step = x
    def getStep(self):
        return self._step

    # Сбрасывает параметры пути
    def resetWay(self):
        self._parent = []
        self._step = -1

class Bot(pg.sprite.Sprite):
    def __init__(self,i,j, way_xy):
        pg.sprite.Sprite.__init__(self)

        self.image = random.choice(BOTS_IMG)
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image,(BTN_SIZE,BTN_SIZE))

        self.start_img = self.image

        self.rect = self.image.get_rect()
        self.rect.x = i * ( BTN_SIZE + PAD )
        self.rect.y = j * ( BTN_SIZE + PAD )

        self.x = self.rect.x
        self.y = self.rect.y

        self.i = i
        self.j = j

        self.way_xy = way_xy
        self.way_ij = []

        self.step = 0

        for i in self.way_xy:
            self.way_ij.append(i)

        for i in range(len(self.way_ij)):
            self.way_ij[i] = count_ij(self.way_ij[i])

        self.next_xy = (self.way_xy[self.step+1][0], self.way_xy[self.step+1][1])
        self.next_ij = (self.way_ij[self.step+1][0], self.way_ij[self.step+1][1])

        self.delta = (self.next_xy[0]-self.x ,self.next_xy[1]-self.y)

        self.rotate = (self.next_ij[0] - self.way_ij[self.step][0], self.next_ij[1] - self.way_ij[self.step][1])
        self.rotate = rotations[str(self.rotate)]

        self.old_rotate = self.rotate

        self.condition_rotation = {
                                   'RIGHT':self.rect.left,
                                   'LEFT': self.rect.right,
                                   'UP': self.rect.bottom,
                                   'DOWN': self.rect.top
                                  }

        self.angles = { 'UP': 0,
                        'RIGHT': 270,
                        'DOWN': 180,
                        'LEFT': 90,
                        '_UP': 360
                        }

        self.sprites = {'UP' : self.image,
                        'RIGHT' : pg.transform.rotate(self.image, 270),
                        'DOWN' : pg.transform.rotate(self.image, 180),
                        'LEFT' : pg.transform.rotate(self.image, 90)
                        }
        self.rotating = False
        self.rotate_step = 0


        self.speedPartOfCell = BOT_SPEED
        self.rotStepsCount = BOT_ROTATE_SPEED

    def update(self,l_click):
        if self.step+2 >= len(self.way_xy):
            self.kill()
            return
        self.rotate_settings()
        self.image = self.sprites[self.rotate]
        self.move()
        if not self.rotating: self.check_transition()
        if self.rotating: self.rotate_action()

    def set_condition(self):
        self.condition_rotation = {
                                   'RIGHT':self.rect.left,
                                   'LEFT': self.rect.right,
                                   'UP': self.rect.bottom,
                                   'DOWN': self.rect.top
                                  }

    def rotate_settings(self):
        self.rotate = (self.next_ij[0] - self.way_ij[self.step][0], self.next_ij[1] - self.way_ij[self.step][1])
        self.rotate = rotations[str(self.rotate)]

        self.set_condition()
        self.cond = self.condition_rotation[self.rotate]
    def move(self):
        if not self.rotating:
            self.rect.x += self.delta[0] // self.speedPartOfCell
            self.rect.y += self.delta[1] // self.speedPartOfCell
    def check_transition(self):
        if self.rotate == 'RIGHT':
            cond_coords = (self.rect.left,self.rect.center[1])
        elif self.rotate == 'DOWN':
            cond_coords = (self.rect.center[0],self.rect.top)
        elif self.rotate == 'UP' or self.rotate == '_UP':
            cond_coords = (self.rect.center[0], self.rect.bottom)
        elif self.rotate == 'LEFT':
            cond_coords = (self.rect.right,self.rect.center[1])

        ij_coords = count_ij(cond_coords)
        in_field = ij_coords[0] >= 0 and ij_coords[0] < ROWS and ij_coords[1] >= 0 and ij_coords[1] < COLS


        if  ij_coords == self.next_ij or not in_field:
            self.rect.x = self.next_xy[0]
            self.rect.y = self.next_xy[1]


            self.old_rotate = self.rotate

            self.step += 1
            ij = count_ij((self.rect.x,self.rect.y))

            self.i = ij[0]
            self.j = ij[1]

            field[self.i][self.j].status = 3

            self.next_xy = (self.way_xy[self.step+1][0], self.way_xy[self.step+1][1])
            self.next_ij = (self.way_ij[self.step+1][0], self.way_ij[self.step+1][1])
            self.delta = (self.next_xy[0]-self.rect.x ,self.next_xy[1]-self.rect.y)

            self.rotate_settings()
            if self.old_rotate != self.rotate:
                self.rotating = True
                self.make_sprites(self.old_rotate, self.rotate)

    def rotate_action(self):
        old_rect_center = self.rect.center
        self.image = self.rotation_sprites[self.rotate_step]
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_center
        self.rotate_step += 1
        if self.rotate_step >= len(self.rotation_sprites):
            self.rotating = False
            self.rotate_step = 0


    def make_sprites(self, old , new):
        gap = (self.angles[new] - self.angles[old]) // self.rotStepsCount

        if old == 'UP' and new == 'RIGHT':
            gap = -90 // self.rotStepsCount
            old = '_UP'
        if old == 'RIGHT' and new == 'UP':
            gap = 90 // self.rotStepsCount
            new = '_UP'
        self.rotation_sprites = []
        for i in range(self.angles[old] , self.angles[new] + gap , gap):
            self.rotation_sprites.append(pg.transform.rotate(self.start_img, i))


SideBar = pg.Surface((90,HEIGHT))
SideBar.fill(GREY)

#BottomBar buttons

# surface, x, y, width, height, color, text, text_size , command
SaveBut = Button(screen, (WIDTH-90-PAD)//2, HEIGHT-90 - PAD,
                WIDTH-90-PAD, 45, GREY, 'Save', 26, save)
ClrBut =  Button(screen, (WIDTH-90-PAD)//2, HEIGHT-45,
                WIDTH-90-PAD, 45, GREY, 'Clear', 26, clear)

all_sprites.add(SaveBut)
button_sprites.add(SaveBut)

all_sprites.add(ClrBut)
button_sprites.add(ClrBut)
#SideBar buttons

# x , y , img_name , format , state

# height = 50
EmptySelect = SelectButton(WIDTH-45,3,'select_empty','.png',0)
EmptySelect.select_me()

WallSelect = SelectButton(WIDTH-45,50 + 3 * 2,'select_wall','.png' ,1)
WaterSelect = SelectButton(WIDTH-45,50 * 2 + 3 * 3,'select_points','.png',2)

StartBot = Button(screen, WIDTH-45, 50 * 3 + 3 * 4, 80, 50, (200,200,200), 'Start',26, start_bot)
ChangefFile = Button(screen,WIDTH-45, 50 * 4 + 3 * 5, 80, 50, (200,200,200), 'Change',26, change_file)
NewFile = Button(screen,WIDTH-45, 50 * 5 + 3 * 6, 80, 50, (200,200,200), 'New file',26, create_file)
Back = Button(screen,WIDTH-45, 50 * 6 + 3 * 7,80,50, (200,200,200), 'Back',26, return_start_screen)

all_sprites.add(StartBot)
button_sprites.add(StartBot)

all_sprites.add(ChangefFile)
button_sprites.add(ChangefFile)

all_sprites.add(NewFile)
button_sprites.add(NewFile)

all_sprites.add(Back)
button_sprites.add(Back)

select_cap_img = pg.image.load(path.join(img_dir, "select_highlight.png")).convert()
select_cap_img.set_colorkey(WHITE)
select_cap_x = EmptySelect.rect.x
select_cap_y = EmptySelect.rect.y

start_screen()



# Цикл игры
running = True
while running:
    l_click = False
    r_click = False
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
            pos = pg.mouse.get_pos()
            if pos[0] > WIDTH or pos[0] < 0 or pos[1] > HEIGHT or pos[1] < 0:
                l_click = False
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            r_click = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 3 and CHOOSEN_STATE == 2:
            ij = count_ij(pg.mouse.get_pos())
            if ij[0] >= 0 and ij[1] >= 0 and ij[0] < ROWS and ij[1] < COLS:
                point_b = ij
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and CHOOSEN_STATE == 2:
            ij = count_ij(pg.mouse.get_pos())
            if ij[0] >= 0 and ij[1] >= 0 and ij[0] < ROWS and ij[1] < COLS:
                point_a = ij

    # Обновление
    all_sprites.update(l_click)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(SideBar,(WIDTH-90,0))

    field[point_a[0] ][point_a[1] ].image.fill(WATER_BLUE)
    field[point_b[0] ][point_b[1] ].image.fill(YELLOW)

    all_sprites.draw(screen)
    screen.blit(select_cap_img,(select_cap_x,select_cap_y))

    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
