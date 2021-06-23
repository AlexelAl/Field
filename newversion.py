import pygame  as pg
import sys
from os import path
import math

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
WATER_BLUE = (82, 222, 190)

CHOOSEN_STATE = 0



way = []
field = []
old_new_water = []
new_water = []
status_clr = [WHITE, BLACK, BLUE, RED, WATER_BLUE]
border = [[1,0],[-1,0],[0,1],[0,-1]]

endpoint = (0,0)


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
    global field

    # Copy field from file or Make empty cells
    f = open('save.txt', 'r')
    for i in range(ROWS):
        field.append([])
        for j in range(COLS):
            stat = f.read(1)
            if stat == '':
                stat = '0'

            cell = Cell( screen, int( stat ), i * ( BTN_SIZE + PAD ), j * (BTN_SIZE + PAD), i, j )
            field[i].append( cell )
    f.close()

def watering(i,j):
    # fill near cells water

    global field, new_water
    if i >= ROWS or j >= COLS or field[i][j].status != 2:
        return

    childStep = field[i][j].getStep() + 1

    for k in border:
        newi = i + k[0]
        newj = j + k[1]

        in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        if not in_field:
            continue
        currCell = field[newi][newj]
        # if in_field and field[newi][newj].status == 0:
        #     field[newi][newj].status = 2
        #     field[newi][newj].way = field[i][j].way
        #     field[newi][newj].way.append([i,j])
        #     new_water.append((newi,newj))
        if currCell.status == 0 or ( currCell.status == 2 and currCell.getStep() > childStep ):
            currCell.setParent(i,j)
            currCell.setStep(childStep)
            new_water.append((newi,newj))

            currCell.status = 2


#def checkBorders(i,j):
#    for k in border:
    #    newi = i + k[0]
    #    newj = j + k[1]
    #    in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        #if in_field and currCell.status == 0:
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
        if i.status == 2 or i.status == 3:
            i.fill(0)
            i.resetWay()

def start_bot():

    # run = True
    # cell = endpoint
    # while run == True:
    #     try:
    #         if len(cell) == 0 or field[ cell[0] ][ cell[1] ].getStep() == 0:
    #             run = False
    #         if not  field[ cell[0] ][ cell[1] ].endpoint:
    #             field[ cell[0] ][ cell[1] ].status = 3
    #         cell = field[ cell[0] ][ cell[1] ].getParent()
    #     except IndexError:
    #         print('Error: No way to endpoint')
    #         return
    # for i in cell_sprites:
    #     if i.endpoint:
    #         i.endpoint = False
    #         i.status = 3
    global field
    point_a = (0,0)
    point_b = (ROWS-1,COLS-1)

    temp_field = []
    for i in range(ROWS):
        temp_field.append([])
        for j in range(COLS):
            temp_field[i].append(tempCell(i,j,field[i][j].status))

    temp_field[point_a[0]][point_a[1]].status = 2
    temp_field[point_a[0]][point_a[1]].setStep = 0

    near_cells = [point_a]

    while len(near_cells) != 0:
        cell = near_cells.pop()
        i = cell[0]
        j = cell[1]

        childStep = temp_field[i][j].getStep() + 1

        for k in border:
            newi = i + k[0]
            newj = j + k[1]

            in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
            if not in_field:
                continue

            currCell = temp_field[newi][newj]
            if currCell.status == 0 or ( currCell.status == 2 and currCell.getStep() > childStep ):
                temp_field[newi][newj].setParent(i,j)
                temp_field[newi][newj].setStep(childStep)
                near_cells.append((newi,newj))

                temp_field[newi][newj].status = 2
            if newi == point_b[0] and newj == point_b[1]:
                near_cells = []
                break
    run = True
    cell = temp_field[point_b[0] ][ point_b[1]]
    while run:
        if cell.getStep() == 0:
            run = False
        field[cell.i][cell.j].status = 3
        
        cell = cell.getParent()
        cell = temp_field[ cell[0] ][ cell[1]]












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

class tempCell():
    def __init__(self, i, j, status):
        self.i = i
        self.j = j
        self._parent = [i,j]
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
        self._parent = [i,j]
        self._step = -1



class Cell(pg.sprite.Sprite):
    # Можно упростить конструктор, передвая только i, j
    # А x, y рассчитывать уже тут. Один фиг по формуле рассчитываешь
    def __init__(self, surface, status, x, y, i, j):
        pg.sprite.Sprite.__init__(self)

        # Мне кажется можно оставить просто слово status мы же и так в Cell ---Можно, но сеll_status
        self.status = status                            # 0 - empty        Часто упоминается,и много менять !!!!!!!!!!!!!!!!!!!!!!
        self.image = pg.Surface((BTN_SIZE,BTN_SIZE))    # 1 - wall         Тут самое время познакомится с удобствами среды разработки)
        self.image.fill(status_clr[self.status])        # 2 - watering        Жми контрол ф, появится две строки - файнд и реплэйс.
        self.rect = self.image.get_rect()               # 3 - way marker     в файнд - ЧТО нужно заменить, в реплайс НА ЧТО заменить)
        self.rect.x = x                                 # 4 - endpoint
        self.rect.y = y
        self.i = i
        self.j = j
        self.click_indx = False

        self.endpoint = False
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

        if CHOOSEN_STATE != 2:
            status_clr[3] = status_clr[0]
        else:
            status_clr[3] = RED

        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()) and not self.click_indx:
            # Эммм, кажется ниже есть метод для этого) ----Тебе кажется----
            delwatering()
            self.on_click()
            if self.status == 2:
                new_water.append((self.i,self.j))
                self.setParent(self.i,self.j)
                self.setStep(0)

        if self.endpoint:
            self.image.fill(status_clr[4])
        else:
            self.image.fill(status_clr[self.status])
    def on_click(self, color = None):
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
field[0][0].endpoint = True

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
                for k in cell_sprites:
                    if k.endpoint:
                        k.endpoint = False
                field[i][j].endpoint = True

                endpoint = (i,j)



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
