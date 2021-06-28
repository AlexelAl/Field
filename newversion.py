import pygame  as pg
import sys
from os import path
import math

img_dir = path.join(path.dirname(__file__), 'assets')

FPS = 30

ROWS = 10
COLS = 10
PAD = 1


BTN_SIZE = 30

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
YELLOW = (255, 255, 0)

CHOOSEN_STATE = 0



way = []
field = []
temp_field = []
old_new_water = []
new_water = []
status_clr = [WHITE, BLACK, BLUE, RED, WATER_BLUE]
border = [[1,0],[-1,0],[0,1],[0,-1]]

point_b = [0,0]
point_a = [ROWS-1, COLS-1]



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
    global field, temp_field

    # Copy field from file or Make empty cells
    for i in range(ROWS):
        field.append([])
        for j in range(COLS):
            cell = Cell( screen, 0, i * ( BTN_SIZE + PAD ), j * (BTN_SIZE + PAD), i, j )
            field[i].append( cell )

    coords = []
    with open('save.txt' , 'r', encoding="UTF-8") as f:
        for ex in f.read().split():
            coords.append(int(ex))
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
            temp_field[i].append(tempCell(i,j,field[i][j].status))

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
            if j.status == 1:
                f.write(str(j.i))
                f.write(" ")
                f.write(str(j.j))
                f.write(" ")
    f.close()
    sys.exit()

def clear():  #fill the field with empty cells
    for i in cell_sprites:
        i.fill(0)
    for i in temp_field:
        for j in i:
            j.status = 0
            j.resetWay()

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
                j.resetWay()

def start_bot():
    global temp_field, point_a, point_b
    delwatering()
    for i in range(ROWS):
        for j in range(COLS):
            temp_field[i][j].status = field[i][j].status

    new_water.append(point_a)
    temp_field[ point_a[0] ][ point_a[1] ].status = 2

    water_logic()
    while len(new_water) != 0 and temp_field[ point_b[0] ][ point_b[1] ].status != 2:
        water_logic()

    run = True
    cell = point_b
    way = [point_b]
    while run:
        try:
            if len(cell) == 0 or temp_field[ cell[0] ][ cell[1] ].getStep() == 0:
                run = False


            temp_field[ cell[0] ][ cell[1] ].status = 3
            cell = temp_field[ cell[0] ][ cell[1] ].getParent()

            way.append((cell))
            temp_field[ cell[0] ][ cell[1] ].status = 3

        except IndexError:
            print('Error: No way to endpoint')
            return
    for i in range(ROWS):
        for j in range(COLS):
            if temp_field[i][j].status == 3:
                field[i][j].status = 3
    bot = Bot(point_b[0],point_b[1], way)
    all_sprites.add(bot)

def count_position(xy):
    i =  math.floor(xy[0] / (BTN_SIZE+PAD))
    j =  math.floor(xy[1] / (BTN_SIZE+PAD))
    return [i,j]



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
            # Эммм, кажется ниже есть метод для этого) ----Тебе кажется----
            delwatering()
            self.on_click(l_click,r_click)
            # if self.status == 2:
            #     new_water.append((self.i,self.j))
            #     self.setParent(self.i,self.j)
            #     self.setStep(0)

        else:
            self.image.fill(status_clr[self.status])
    def on_click(self,l_click,r_click):

        self.fill(CHOOSEN_STATE)
        self.click_indx = True

    def fill(self, state):
        self.status = state
        self.image.fill(status_clr[self.status])


class Bot(pg.sprite.Sprite):
    def __init__(self,i,j, way_ij):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(img_dir, "bot.png")).convert()
        self.image.set_colorkey(WHITE)

        self.image = pg.transform.scale(self.image,(BTN_SIZE,BTN_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = i * ( BTN_SIZE + PAD )
        self.rect.y = j * ( BTN_SIZE + PAD )

        self.x = self.rect.x
        self.y = self.rect.y

        self.i = i
        self.j = j

        self.way_ij = way_ij
        self.way_xy = self.way_ij
        self.step = 0

        for i in self.way_xy:
            i[0] = i[0] * ( BTN_SIZE + PAD )
            i[1] = i[1] * ( BTN_SIZE + PAD )

        self.next_xy = (self.way_xy[self.step+1][0], self.way_xy[self.step+1][1])
        self.next_ij = (self.way_ij[self.step+1][0], self.way_ij[self.step+1][1])
        self.delta = (self.next_xy[0]-self.x ,self.next_xy[1]-self.y)
    def update(self,l_click):
        if self.step+1 >= len(self.way_xy):
            self.kill()
            return
        self.rect.x += self.delta[0] / 3
        self.rect.y += self.delta[1] / 3

        ij_coords = count_position((self.rect.x,self.rect.y))
        in_field = ij_coords[0] >= 0 and ij_coords[0] < ROWS and ij_coords[1] >= 0 and ij_coords[1] < COLS

        if  ij_coords == self.next_ij or not in_field:
            self.rect.x = self.next_xy[0]
            self.rect.y = self.next_xy[1]

            self.step += 1
            ij = count_position((self.rect.x,self.rect.y))
            self.i = ij[0]
            self.j = ij[1]
            self.next_xy = (self.way_xy[self.step+1][0], self.way_xy[self.step+1][1])
            self.next_ij = (self.way_ij[self.step+1][0], self.way_ij[self.step+1][1])
            self.delta = (self.next_xy[0]-self.rect.x ,self.next_xy[1]-self.rect.y)
        # self.rect.x = self.way[self.step][0] * ( BTN_SIZE + PAD )
        # self.rect.y = self.way[self.step][1] * ( BTN_SIZE + PAD )


class CarBot(pg.sprite.Sprite):
    def __init__(self,i,j, way):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(img_dir, "bot.png")).convert()
        self.image.set_colorkey(WHITE)

        self.image = pg.transform.scale(self.image,(BTN_SIZE,BTN_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = i * ( BTN_SIZE + PAD )
        self.rect.y = j * ( BTN_SIZE + PAD )

        self.i = i
        self.j = j

        self.moving = False
        self.speedx = 0
        self.speedy = 0
        self.step = 0
        self.way = way
    def update(self, l_click):
        if self.moving:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.step==2:
                self.moving = False
            self.step += 1
        else:
            self.step = 0
            for i in border:
                in_field = self.i+i[0] >= 0 and self.i+i[0] < ROWS and self.j+i[1] >= 0 and ROWS and self.j+i[1] < COLS
                if  in_field and field[self.i+i[0]][self.j+i[1]].status == 3:
                    self.speedx = BTN_SIZE / 2 * i[0]
                    self.speedy = BTN_SIZE / 2 * i[1]
                    self.moving = True
                    self.i = self.i + i[0]
                    self.j = self.j + i[1]

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
WaterSelect = SelectButton(WIDTH-45,108,'select_points','.png',2)

StartBot = Button(screen, WIDTH-45, 162, 80, 50, (200,200,200), 'Start', start_bot)


select_cap_img = pg.image.load(path.join(img_dir, "select_highlight.png")).convert()
select_cap_img.set_colorkey(WHITE)
select_cap_x = EmptySelect.rect.x
select_cap_y = EmptySelect.rect.y

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
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            r_click = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 3 and CHOOSEN_STATE == 2:
            ij = count_position(pg.mouse.get_pos())
            if ij[0] >= 0 and ij[1] >= 0 and ij[0] < ROWS and ij[1] < COLS:
                point_b = ij
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and CHOOSEN_STATE == 2:
            ij = count_position(pg.mouse.get_pos())
            if ij[0] >= 0 and ij[1] >= 0 and ij[0] < ROWS and ij[1] < COLS:
                point_a = ij


    # Обновление
    all_sprites.update(l_click)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(SideBar,(WIDTH-90,0))

    print(point_a, "----------", point_b)
    field[point_a[0] ][point_a[1] ].image.fill(WATER_BLUE)
    field[point_b[0] ][point_b[1] ].image.fill(YELLOW)

    all_sprites.draw(screen)
    screen.blit(select_cap_img,(select_cap_x,select_cap_y))

    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
