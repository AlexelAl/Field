import pygame  as pg
import sys

FPS = 30

rows = 100
cols = 100
pad = 1

BTN_SIZE = 1
WIDTH = BTN_SIZE * cols + pad * (cols-1)
HEIGHT =  BTN_SIZE * (rows+1) + pad * cols

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
            cell = Cell(screen,0, i * BTN_SIZE + pad * i, j * BTN_SIZE + pad * j,i,j)
            field[i].append( cell )
    f.close()
def water(i,j):
    global field
    for k in border:
        newi = i + k[0]
        newj = j + k[1]
        if not(0 > newi or newi >= rows or 0 > newj or newj >= cols) and not field[newi][newj].cell_status == 1:
            field[newi][newj].cell_status = 2
def parse():
    global field
    # 7. Не понял зачем выносить функцию в отдельнуб переменную
    funk = water
    for ii in range(rows):
        for jj in range(cols):
            if field[ii][jj].cell_status == 2:
                funk(ii,jj)

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def create_button(surface,x,y,w,h,color):
    but_surf = pg.Surface((w,h))
    but_surf.fill(color)
    but_rect = but_surf.get_rect()
    but_rect.midtop = (x , y)
    draw_text(but_surf,'Save & exit', 26,w//2,5,BLACK)
    surface.blit(but_surf,but_rect)

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
    def update(self, was_click):
        if was_click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.cell_status = (self.cell_status + 1)%3
            self.image.fill(status_clr[self.cell_status])
            if self.cell_status == 2:
                water(self.i,self.j)
                for i in range((rows+cols)*2):
                    parse()

        self.image.fill(status_clr[self.cell_status])


all_sprites = pg.sprite.Group()
CreateField()
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
        if event.type == pg.MOUSEBUTTONUP:
            was_click = True

    # Обновление
    all_sprites.update(was_click)
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    create_button(screen,WIDTH//2, HEIGHT-BTN_SIZE, WIDTH,BTN_SIZE * 1.5, (150,150,150))
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
