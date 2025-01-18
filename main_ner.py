import pygame
import  os
import sys
import random
from math import *




pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60

sc = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
from load_ing import *

def restart():
    global player_group,spider_group, axe_group, block_group, water_group, spawner_group,player
    player_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()
    spawner_group = pygame.sprite.Group()
    axe_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    player = Player(player_image,(0,0))
    player.group.add(player)





def gamelvl():
    sc.fill('white')
    player_group.draw(sc)
    player_group.update()
    spider_group.draw(sc)
    spider_group.update()
    spawner_group.draw(sc)
    spawner_group.update()
    axe_group.draw(sc)
    axe_group.update()
    block_group.draw(sc)
    block_group.update()
    water_group.draw(sc)
    water_group.update()

    pygame.display.update()








class Axe(pygame.sprite.Sprite):
    def __init__(self,image,pos,start_deg):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.deg_rotate = 0
        self.deg = start_deg
        self.timer_attack = 0

    def rotate(self):
        self.deg_rotate -= 20
        self.image = pygame.transform.rotate(axe_image,self.deg_rotate)



    def move(self):
        self.deg += 3
        self.rect.centerx = 150 * cos(radians(self.deg)) + player.rect.centerx
        self.rect.centery = 150 * sin(radians(self.deg)) + player.rect.centery














class Player(pygame.sprite.Sprite):
        def __init__(self, image, pos):
            pygame.sprite.Sprite.__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos [1]
            self.key = pygame.key.get_pressed()
            self.speed = 10
            self.timer_anime = 0
            self.anime = False
            self.frame = 0
            self.pos_maps = [0,0]
            self.score = 0
            self.axe = 1
            self.camera = False



        def add_axe(self):
            global axe_group
            axe_group = pygame.sprite.Group()
            for i in range(self.axe):
                axe = Axe(axe_image,(self.rect.centerx + 70,self.rect.rectery + 70),(360// self.axe * i))
                axe_group.add(axe)
































































restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    gamelvl()
    clock.tick(FPS)
































































