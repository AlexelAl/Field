import pygame  as pg
import sys

FPS = 30

rows = 15
cols = 15
pad = 1

BTN_SIZE = 35
WIDTH = BTN_SIZE * cols + pad * (cols-1)
HEIGHT =  BTN_SIZE * rows + pad * cols + 90 + pad

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

field = []
status_clr = [WHITE, BLACK, BLUE]
border = [[1,0],[-1,0],[0,1],[0,-1]]

# Создаем игру и окно
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH , HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()


def CreateField():
    global field
    f = open('save.txt', 'r')
    for i in range(rows):
        field.append([])
        for j in range(cols):
            stat = f.read(1)
            if stat == '' or int(stat) > 2:
                stat = '0'
            cell = Cell(screen,int(stat), i * (BTN_SIZE + pad), j * (BTN_SIZE + pad),i,j)
            field[i].append( cell )
    f.close()
def water(i,j):
    global field
    if field[i][j].cell_status != 2:
        return
    for k in border:
        newi = i + k[0]
        newj = j + k[1]
        in_field = not(0 > newi or newi >= rows or 0 > newj or newj >= cols)
        if in_field and not field[newi][newj].cell_status == 1:
            field[newi][newj].cell_status = 2
def parse():
    global field
    for ii in range(rows):
        for jj in range(cols):
            if field[ii][jj].cell_status == 2:
                water(ii,jj)
    ii = 0
    jj = 0
    for ii in range(rows):
        for jj in range(cols):
            if field[rows-1-ii][cols-1-jj].cell_status == 2:
                water(rows-1-ii,cols-1-jj)
def save():
    global field
    f = open('save.txt', 'w')
    for i in field:
        for j in i:
            f.write(str(j.cell_status))
    f.close()
    sys.exit()
def clear():
    for i in Cell_sprites:
        i.fill(0)

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Button(pg.sprite.Sprite):
    def __init__(self,surface,x,y,w,h,color, text, command):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.command = command
        self.text = text
        self.image = pg.Surface((w,h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.coords = (x,y)
        self.rect.midtop = self.coords

        draw_text(self.image,text, 26,w//2,5,BLACK)

        all_sprites.add(self)
        Button_sprites.add(self)

    def update(self,was_click):
        if was_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.command()
        self.image.fill(self.color)
        self.rect.midtop = self.coords

        pressed = pg.mouse.get_pressed()
        if pressed[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            self.rect.x += 2
            self.rect.y += 2
            self.image.fill(WHITE)
        draw_text(self.image,self.text, 26,self.rect.width//2,5,BLACK)
    def draw(self):
        screen.blit(self.image, self.rect)


class Cell(pg.sprite.Sprite):
    def __init__(self, surface,status,x,y,i,j):
        pg.sprite.Sprite.__init__(self)
        self.cell_status = status                            # 0 - empty
        self.image = pg.Surface((BTN_SIZE,BTN_SIZE))         # 1 - wall
        self.image.fill(status_clr[self.cell_status])        # 2 - water
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = i
        self.j = j

        all_sprites.add(self)
        Cell_sprites.add(self)
    def update(self, was_click):
        if was_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.cell_status = (self.cell_status + 1)%3
            self.image.fill(status_clr[self.cell_status])
            if self.cell_status == 2:
                water(self.i,self.j)
        self.image.fill(status_clr[self.cell_status])
    def fill(self, stat):
        self.cell_status = stat
        self.image.fill(status_clr[self.cell_status])

all_sprites = pg.sprite.Group()
Button_sprites = pg.sprite.Group()
Cell_sprites = pg.sprite.Group()


CreateField()
SaveBut = Button(screen,WIDTH//2, HEIGHT-45, WIDTH,45, (150,150,150),'Save & Exit',save)
ClrBut =  Button(screen,WIDTH//2, HEIGHT-90-pad, WIDTH,45, (150,150,150), 'Clear', clear)
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


    # Обновление
    parse()
    all_sprites.update(was_click)
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
