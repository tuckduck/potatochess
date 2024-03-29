import sys, pygame
import os
import time
from pygame.locals import *

def idleAnimation(tick, potat):
    '''Rotates the Hero image to produce an idle animation
    '''
    if(tick // 4 % 4 == 3): #slow down the animation, only change image every 4 frames/ticks
        return pygame.transform.rotate(potat, -(tick // 8 %2))
    else:
        return pygame.transform.rotate(potat, tick // 8 % 2)
def heroMove(presses):
    '''Moves the Hero
       Takes: List of Pressed Keys
    '''
    move = [0,0]
    if(presses[K_w] or presses[K_UP]):
        move[1] -=6
    if(presses[K_s] or presses[K_DOWN]):
        move[1] +=6
    if(presses[K_d] or presses[K_RIGHT]):
        move[0] += 6
    if(presses[K_a] or presses[K_LEFT]):
        move[0] -= 6
    return move
def inventoryMenu(background, hero):
    '''The Inventory/Equipped items menu
       Takes: Backround snapshot surface of the game, to draw the menu on
    '''
    text = pygame.font.Font(None, 46)
    text.set_bold(True)

    hat = text.render("Hat", True, [0,0,0],[119,136,153])
    hatRect = hat.get_rect()
    hatRect.center = [1300,225]
    body = text.render("Body", True, [0,0,0],[119,136,153])
    bodyRect = body.get_rect()
    bodyRect.center = [1300,425]
    legs = text.render("Legs", True, [0,0,0],[119,136,153])
    legsRect = legs.get_rect()
    legsRect.center = [1300,625]
    weapon = text.render("Weapon", True, [0,0,0],[119,136,153])
    weaponRect = weapon.get_rect()
    weaponRect.center = [1100,425]

    invent_rects = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}

    equip_text = {0:[hat, hatRect],1:[body, bodyRect], 2:[legs, legsRect], 3:[weapon, weaponRect]}

    equip_slots = drawInventoryMenu(background)
    pygame.display.flip()

    menu = pygame.display.get_surface().copy()
    while(1):
        screen.fill([0,0,0])
        screen.blit(menu, [0,0])
        for i in range(8):
            if hero.inventory[i] is not None:
                image = hero.inventory[i].image
                rect = image.get_rect()
                rect.center = [120 + i * 200, 550 + (i // 4) * 150]
                invent_rects[i] = rect
                screen.blit(image, rect)
        for k in range(4):
            if hero.equip[k] is not None:
                item = hero.equip[k]
                image = item.image
                rect = image.get_rect()
                rect.center = equip_slots[k].center
                screen.blit(image, rect)
            else:
                screen.blit(equip_text[k][0], equip_text[k][1])
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0]:
            pos = pygame.mouse.get_pos()
            for j in range(8):
                if j < 4:
                    if hero.equip[j]:
                        if equip_slots[j].collidepoint(pos):
                            hero.itemUnequip(hero.equip[j])
                if invent_rects[j]:
                    if invent_rects[j].collidepoint(pos):
                        hero.itemEquip(hero.inventory[j])
                        invent_rects.update({j:None})
                        hero.inventory[j] = None
        pygame.display.flip()
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        
        if pressed[K_q]:
            break
def drawInventoryMenu(snapshot):
    '''Draws the base shapes of the Inventory menu
       Takes: Backround snapshot of game to draw on
    '''
    screen.blit(snapshot,[0,0])
    pygame.draw.rect(screen, [139,69,19],pygame.Rect(10,465,820,325))
    pygame.draw.rect(screen, [101,67,33],pygame.Rect(20,475,800,305))

    pygame.draw.rect(screen, [47, 79, 79],pygame.Rect(1215,340,170,170))
    bodySlot = pygame.draw.rect(screen, [119,136,153],pygame.Rect(1225,350,150,150))

    pygame.draw.rect(screen, [47, 79, 79],pygame.Rect(1215,540,170,170))
    legsSlot = pygame.draw.rect(screen, [119,136,153],pygame.Rect(1225,550,150,150))

    pygame.draw.rect(screen, [47, 79, 79],pygame.Rect(1015,340,170,170))
    weaponSlot = pygame.draw.rect(screen, [119,136,153],pygame.Rect(1025,350,150,150))

    pygame.draw.rect(screen, [47, 79, 79],pygame.Rect(1215,140,170,170))
    hatSlot = pygame.draw.rect(screen, [119,136,153],pygame.Rect(1225,150,150,150))

    return {0:hatSlot, 1:bodySlot, 2:legsSlot, 3:weaponSlot}

class enemyGenerator:
    def __init__(self):
        self.spawns = [[0, "Tomato.png"]]
    def spawnEnemy(self, enemyId, location):
        return enemy(self.spawns[enemyId], location)
    def spawnEnemies(self, enemySpriteGroup, spawnLocations):
        for location in spawnLocations:
            enemySpriteGroup.add(self.spawnEnemy(0, [750,200])) 

class enemy(pygame.sprite.Sprite):
    def __init__(self, vector, location):
        pygame.sprite.Sprite.__init__(self)
        self.enemyId = vector[0]
        self.image = pygame.image.load(vector[1])
        self.rect = self.image.get_rect()
        self.rect.move_ip(location[0], location[1])

class hero(pygame.sprite.Sprite):
    '''Class for the player's sprite. Stores the inventory/equipment data, handles changing 
       it's image according to equipped items
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original = pygame.image.load("potat.png")
        self.image_ = self.original
        self.image = None
        self.rect = self.image_.get_rect()
        self.rect.move_ip(620,610)
        self.hero_library = {0:"hatpotat.png"}
        self.equip = {0:None, 1:None, 2:None, 3:None}
        self.inventory = {0:None,1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
    def update(self, move):
        self.rect.move_ip(move[0],move[1])
    def updateImage(self):
        if self.equip[0] and not self.equip[3]:
            width, height = 137, 250   #gross hardcode, needs revision
        elif self.equip[0] and self.equip[3]:
            width, height = 160, 250
        elif not self.equip[0] and self.equip[3]:
            width, height = 160,177
        else:
            width, height = 137, 177
        new_surf = pygame.Surface([width, height],pygame.SRCALPHA)
        ori_rect = self.original.get_rect()
        ori_rect.bottomright = new_surf.get_rect().bottomright
        new_surf.blit(self.original, ori_rect)
        if self.equip[0]:
            new_surf.blit(self.equip[0].image, [width-137,0])
        if self.equip[1]:
            new_surf.blit(self.equip[1].image, [width-137,height-97])
        if self.equip[2]:
            new_surf.blit(self.equip[2].image, [width-137,height-45])
        if self.equip[3]:
            new_surf.blit(self.equip[3].image, [0,height-170])
        self.image_ = new_surf
        new_rect = self.image_.get_rect()
        new_rect.bottomright = self.rect.bottomright
        self.rect = new_rect
    def itemEquip(self, item):
        self.equip.update({item.type:item})
        self.updateImage()
        #self.image_ = pygame.image.load(self.hero_library.get(itemID))
    def itemUnequip(self,item):
        self.equip.update({item.type:None})
        self.placeInInventory(item)
        self.updateImage()
    def placeInInventory(self, item):
        for i in range(8):
            if self.inventory[i] is None:
                self.inventory[i] = item
                break

class itemGenerator:
    def __init__(self):
        self.spawns = [("starterhat.png", [900,500],0),("starterrobe.png", [440,400], 1),("starterlegs.png", [770,300], 2),("staff.png", [640,90], 3)]
    def spawnItem(self, itemID):
        spawn = self.spawns[itemID]
        image = pygame.image.load(spawn[0])
        rect = image.get_rect()
        rect.move_ip(spawn[1][0],spawn[1][1])
        itemObj = item(image, rect,itemID,spawn[2])
        return itemObj
    def spawnItems(self, itemIDs, itemSpriteGroup):
        for item in itemIDs:
            itemSpriteGroup.add(self.spawnItem(item)) 

class item(pygame.sprite.Sprite):
    def __init__(self, image_, rect_,itemID,itemType):
        pygame.sprite.Sprite.__init__(self)
        self.type = itemType
        self.image = image_
        self.rect = rect_
        self.itemID = itemID

def level(background, heroSprite, potat, item_spawner, enemy_spawner, screen):
    background = pygame.image.load(background)
    backrect = background.get_rect()
    current_item_spawns = pygame.sprite.Group()
    current_enemy_spawns = pygame.sprite.Group()
    enemy_spawn_locs = [0]

    enemy_spawner.spawnEnemies(current_enemy_spawns, enemy_spawn_locs)
    item_spawner.spawnItems([0,1,2,3], current_item_spawns) #spawns all 4 items

    tick = 0 
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        potat.image = idleAnimation(tick, potat.image_)
        tick += 1
        pressed = pygame.key.get_pressed()
        move = heroMove(pressed)
        fights = pygame.sprite.spritecollide(potat, current_enemy_spawns, True)
        for enemy in fights:
            battle(pygame.display.get_surface(), potat, enemy)
        item_pickups = pygame.sprite.spritecollide(potat, current_item_spawns, True)
        potat.update(move)
        screen.blit(background, backrect)
        current_item_spawns.draw(screen)
        current_enemy_spawns.draw(screen)
        heroSprite.draw(screen)
        pygame.display.flip()
        
        for item in item_pickups:
            potat.placeInInventory(item)
        if(pressed[K_e] == True):
            inventoryMenu(pygame.display.get_surface(), potat)
        #if tick is 200:
         #   battle(pygame.display.get_surface(), potat, "enemy")
def setup():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1,31)
    size = width, height = 1400, 800

    screen = pygame.display.set_mode(size)

    potat = hero()
    heroSprite = pygame.sprite.GroupSingle()
    heroSprite.add(potat)

    item_spawner = itemGenerator()
    enemy_spawner = enemyGenerator()
    return screen, potat, heroSprite, item_spawner, enemy_spawner

def battleStartup(background, potat_img, enemy_img):
    setting = pygame.image.load("forestBattle.png")
    black = pygame.Surface([1400, 800])
    black.set_alpha(100)
    shaded = background.copy()
    shaded.blit(black, [0,0])
    black.set_alpha(170)
    for i in range(6):
        screen.blit(black, [0,0])
        time.sleep(.2)
        pygame.display.flip()
        screen.blit(shaded, [0,0])
        time.sleep(.2)
        pygame.display.flip()
    screen.blit(black, [0,0])
    time.sleep(.2)
    pygame.display.flip()
    black.set_alpha(200)
    screen.blit(black, [0,0])
    time.sleep(.2)
    pygame.display.flip()
    black.set_alpha(100)
    screen.blit(setting, [0,0])
    screen.blit(black, [0,0])
    time.sleep(.2)
    pygame.display.flip()
    clock = pygame.time.Clock()
    for i in range(0, 1400, 20):
        screen.blits([(setting, [0,0]), (potat_img, [i-200,500]), (enemy_img, [1400-i, 200])])
        
        
        pygame.display.flip()
        clock.tick(35)
        #print(i)
    screen.blits([(setting, [0,0]), (potat_img, [1200,500]), (enemy_img, [0, 200])])
    i = 0
    while(i < 1000000):
        i += 1
        
    

def battle(background, potat, enemy):
    snapshot = background.copy()
    platform = pygame.image.load("grass3.png")
    hero_surf = createBattleSprite(potat, platform)
    enemy_surf = createBattleSprite(enemy, platform)
    battleStartup(snapshot, hero_surf, enemy_surf)
def createBattleSprite(character, platform):
    width, height = character.rect.width, character.rect.width
    battle_surf = pygame.Surface([220, character.image.get_height()+20],pygame.SRCALPHA)
    battle_surf.blit(platform, [0,battle_surf.get_height()-60])
    offset = (220-width) / 2
    battle_surf.blit(character.image, [offset, 0])
    return battle_surf
pygame.init()
screen, potat, heroSprite, item_spawner, enemy_spawner = setup()
current_item_spawns = pygame.sprite.Group()

#level("dirtbackround.png", heroSprite, potat, item_spawner, screen)
level("forestbackround.png", heroSprite, potat, item_spawner, enemy_spawner, screen)
