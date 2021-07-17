import pygame as pg
from set import *
from os import path
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH , HEIGHT))
pg.display.set_caption("Field")

ICON = pg.image.load(path.join(img_dir, "bot.png"))
ICON.set_colorkey(WHITE)
pg.display.set_icon(ICON)

all_sprites = pg.sprite.Group()
button_sprites = pg.sprite.Group()
cell_sprites = pg.sprite.Group()
select_sprites = pg.sprite.Group()
bot_sprites = pg.sprite.Group()
clock = pg.time.Clock()

BOTS_IMG = [pg.image.load(path.join(img_dir, "tank01.png")).convert(),
            pg.image.load(path.join(img_dir, "bot.png")).convert()]
font_name = pg.font.match_font('arial')
