import sys, pygame
import os
import time
from pygame.locals import *
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1,31)
size = width, height = 1400, 800

def idleAnimation(tick, potat):
    if(tick // 4 % 4 == 3):
        return pygame.transform.rotate(potat, -(tick // 4 %2))
    else:
        return pygame.transform.rotate(potat, tick // 4 % 2)
def heroMove(presses):
    move = [0,0]
    if(pressed[K_UP] == True):
        move[1] -=6
    if(pressed[K_DOWN] == True):
        move[1] +=6
    if(pressed[K_RIGHT] == True):
        move[0] += 6
    if(pressed[K_LEFT] == True):
        move[0] -= 6
    return move
class hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ = pygame.image.load("potat.png")
        self.image = None
        self.rect = self.image_.get_rect()
        self.rect.move_ip(620,610)
        self.hero_library = {0:"hatpotat.png"}
    def update(self, move):
        self.rect.move_ip(move[0],move[1])
    def itemPickup(self, itemID):
        self.image_ = pygame.image.load(self.hero_library.get(itemID))

class itemGenerator:
    def __init__(self):
        self.spawns = [("starterhat.png", [900,500])]
    def spawnItem(self, itemID):
        spawn = self.spawns[itemID]
        self.image = pygame.image.load(spawn[0])
        self.rect = self.image.get_rect()
        self.rect.move_ip(spawn[1][0],spawn[1][1])
        return item(self.image, self.rect,itemID)

class item(pygame.sprite.Sprite):
    def __init__(self, image_, rect_,itemID):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_
        self.rect = rect_
        self.itemID = itemID

screen = pygame.display.set_mode(size)
background = pygame.image.load("forestbackround.png")
backrect = background.get_rect()
potat = hero()
heroSprite = pygame.sprite.GroupSingle()
heroSprite.add(potat)
item_spawns = itemGenerator()
current_spawns = pygame.sprite.Group()
current_spawns.add(item_spawns.spawnItem(0))
tick = 0 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    potat.image = idleAnimation(tick, potat.image_)
    tick += 1
    pressed = pygame.key.get_pressed()
    move = heroMove(pressed)
    item_pickups = pygame.sprite.spritecollide(potat, current_spawns, True)
    for item in item_pickups:
        potat.itemPickup(item.itemID)
    potat.update(move)
    screen.blit(background, backrect)
    current_spawns.draw(screen)
    heroSprite.draw(screen)
    pygame.display.flip()
