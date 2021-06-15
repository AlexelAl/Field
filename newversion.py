import pygame  as pg
import sys
from os import path

img_dir = path.join(path.dirname(__file__), 'assets')

FPS = 30

ROWS = 15
COLS = 15
PAD = 1


BTN_SIZE = 30
WIDTH = BTN_SIZE * COLS + PAD * COLS + 90
HEIGHT =  BTN_SIZE * ROWS + PAD * COLS + 90 + PAD

# Задаем цвета
WHITE = (255, 255, 255)
GREY = (150,150,150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CHOOSEN_STATE = 0


field = []
status_clr = [WHITE, BLACK, BLUE]
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
    global field
    f = open('save.txt', 'r')
    for i in range(ROWS):
        field.append([])
        for j in range(COLS):
            stat = f.read(1)
            if stat == '' or int(stat) > 2:
                stat = '0'

            cell = Cell( screen, int( stat ), i * ( BTN_SIZE + PAD ), j * (BTN_SIZE + PAD), i, j )
            field[i].append( cell )
    f.close()

def water(i,j):
    global field
    if field[i][j].cell_status != 2:
        return
    for k in border:
        newi = i + k[0]
        newj = j + k[1]
        in_field = not(0 > newi or newi >= ROWS or 0 > newj or newj >= COLS)
        if in_field and not field[newi][newj].cell_status == 1:
            field[newi][newj].cell_status = 2

def parse():
    global field
    for ii in range(ROWS):
        for jj in range(COLS):
            if field[ii][jj].cell_status == 2:
                water(ii,jj)
                break

    ii = 0
    jj = 0
    for ii in range(ROWS):
        for jj in range(COLS):
            if field[ROWS-1-ii][COLS-1-jj].cell_status == 2:
                water(ROWS-1-ii,COLS-1-jj)
                break

def save():
    global field
    f = open('save.txt', 'w')
    for i in field:
        for j in i:
            f.write(str(j.cell_status))
    f.close()
    sys.exit()

def clear():
    for i in cell_sprites:
        i.fill(0)

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
    def __init__(self,x,y,img_name,state):
        pg.sprite.Sprite.__init__(self)

        self.unselected_img = pg.image.load(path.join(img_dir, img_name)).convert()
        self.image = self.unselected_img

        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)

        self.selected = False
        self.state = state

        all_sprites.add(self)
        select_sprites.add(self)

    def update(self,was_click):
        global select_cap_x,select_cap_y
        if was_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.select_me()
            select_cap_x =  self.rect.x
            select_cap_y = self.rect.y
    def select_me(self):
        global CHOOSEN_STATE
        self.unselect_all()
        self.selected = True
        CHOOSEN_STATE = self.state
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

    def update(self,was_click):
        pressed = pg.mouse.get_pressed()
        if was_click and self.rect.collidepoint(pg.mouse.get_pos()):
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
        self.cell_status = status                            # 0 - empty        Часто упоминается,и много менять !!!!!!!!!!!!!!!!!!!!!!
        self.image = pg.Surface((BTN_SIZE,BTN_SIZE))         # 1 - wall         Тут самое время познакомится с удобствами среды разработки)
        self.image.fill(status_clr[self.cell_status])        # 2 - water        Жми контрол ф, появится две строки - файнд и реплэйс.
        self.rect = self.image.get_rect()                    #                  в файнд - ЧТО нужно заменить, в реплайс НА ЧТО заменить)
        self.rect.x = x
        self.rect.y = y
        self.i = i
        self.j = j
        self.click_indx = False

        all_sprites.add(self)
        cell_sprites.add(self)
    def update(self,was_click):
        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()) and not self.click_indx:
            # Эммм, кажется ниже есть метод для этого) ----Тебе кажется----
            self.on_click()
            if self.cell_status == 2:
                water(self.i, self.j)
        self.image.fill(status_clr[self.cell_status])
    def on_click(self, color = None):
        self.fill(CHOOSEN_STATE)
        self.click_indx = True

    def fill(self, state):
        self.cell_status = state
        self.image.fill(status_clr[self.cell_status])

# Переснес в начало --- Зачем? ------
#!!!!!!!!!!!!!!!!!!!!!!!!ну вроде как глобальное объявление групп, это больше похоже на насройки и константы

# all_sprites = pg.sprite.Group()
# Button_sprites = pg.sprite.Group()
# Cell_sprites = pg.sprite.Group()

select_cap_img = pg.image.load(path.join(img_dir, "select_highlight.png")).convert()
select_cap_img.set_colorkey(WHITE)
select_cap_x = WIDTH + 100
select_cap_y = HEIGHT + 100


CreateField()
SaveBut = Button(screen, (WIDTH-90-PAD)//2, HEIGHT-45, WIDTH-90-PAD, 45, GREY, 'Save & Exit', save)
ClrBut =  Button(screen, (WIDTH-90-PAD)//2, HEIGHT-90-PAD, WIDTH-90-PAD, 45, GREY, 'Clear', clear)

SideBar = pg.Surface((90,HEIGHT))
SideBar.fill(GREY)

#self,x,y,img_name,state
EmptySelect = SelectButton(WIDTH-45,2,'select_empty.png',0)
WallSelect = SelectButton(WIDTH-45,39,'select_wall.png' ,1)
WaterSelect = SelectButton(WIDTH-45,78,'select_water.png',2)


# Цикл игры
running = True
while running:
    was_click = False
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            was_click = True
            for i in cell_sprites:
                i.click_indx = False


    # Обновление
    parse()
    all_sprites.update(was_click)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(SideBar,(WIDTH-90,0))

    all_sprites.draw(screen)
    screen.blit(select_cap_img,(select_cap_x,select_cap_y))
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()

# Глобальные комментарии
# ?4. добавь задержку в распростронении воды, чтоб это было красиво
    # -------------В процессе------------------
# 5. Иногда вода глючит, надо поправить

# !!!!!!!!!!!!!!! В целом уже классно все работает, можно переходить к третьему этапу
# 3 Этап. Нужно сделать так, чтобы вода заканчивала распространяться, как только достигнет какой то заданной клетки
# Соответсвенно нужна возможность отметить клетку до которой мы распростроняем воду.
# Т.е. что то типо финальная точка, потом выбираем воду и тыкаем в любую клетку и как только вода попадает в целевую клетку - она перестает распространяться


#В СЛЕДУЮЩЕМ ОБНОВЛЕНИИ:
#----Красивое распростронение воды
