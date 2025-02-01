from distutils.file_util import move_file
from random import choice

import pygame
import os
import sys
import random
from math import *

from pygame.camera import Camera

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load_ing import *


def restart():
    global player_group, spider_group, axe_group, block_group, water_group, spawner_group, player, camera_group
    player_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()
    spawner_group = pygame.sprite.Group()
    axe_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    player = Player(player_image_b, (100, 100))
    player_group.add(player)
    player.add_axe()
    camera_group = SuperGroup()


def gamelvl():
    sc.fill('gray')
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


def drawmaps(nameFile):
    maps = []
    source = "lvl/" + str(nameFile)
    with open(source, "r") as file:
        for i in range(0, 100):
            maps.append(file.readline().replace("\n", "").split(",")[0:-1])

    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 80
        for j in range(0, len(maps[0])):
            pos[0] = 80 * j
            if maps[i][j] == '1':
                block = Block(block_image, pos)
                block_group.add(block)
                camera_group.add(block)
            elif maps[i][j] == '2':
                spawner = Spawner(spawnerImage, pos)
                spawner_group.add(spawner)

                camera_group.add(spawner)
            elif maps[i][j] == '3':
                water = Water(water_image, pos)
                water_group.add(water)

                camera_group.add(water)
class Camera():
    def camera_move(self, stepx, stepy):
        self.rect.x += stepx
        self.rect.y += stepy

class Spider(pygame.sprite.Sprite, Camera):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 3
        self.camera = False
        self.timer_move = 0

    def move(self):
        self.timer_move += 1
        if self.timer_move / FPS > 2:
            self.speedx = choice((-1,1))
            self.speedy = choice((-1,1))
            self.timer_move = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy



    def collide(self):
        if pygame.sprite.spritecollide(self, block_group,False):
            self.speedy *= -1
            self.speedx *= -1

    def update(self, *args, **kwargs):
        self.move()
        self.collide()


class Axe(pygame.sprite.Sprite):
    def __init__(self, image, pos, start_deg):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.deg_rotate = 0
        self.deg = start_deg
        self.timer_attack = 0

    def update(self):
        self.rotate()
        self.move()

    def rotate(self):
        self.deg_rotate -= 20
        self.image = pygame.transform.rotate(axe_image, self.deg_rotate)

    def move(self):
        self.deg += 3
        self.rect.centerx = 150 * cos(radians(self.deg)) + player.rect.centerx
        self.rect.centery = 80 * sin(radians(self.deg)) + player.rect.centery


class Block(pygame.sprite.Sprite, Camera):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        if pygame.sprite.spritecollide(self,player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            elif player.dir == "right":
                player.rect.right = self.rect.left
            elif player.dir == "top":
                    player.rect.top = self.rect.bottom
            elif player.dir == "bottom":
                player.rect.bottom = self.rect.top

class Spawner(pygame.sprite.Sprite, Camera):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timer_spawn = 0


    def update(self, *args, **kwargs):
        if 0 < self.rect.centerx < 1200 and 0 < self.rect.centery < 800:
            self.timer_spawn += 1
            if self.timer_spawn / FPS > 1:
                spider = Spider(spider_image[0],self.rect.center)
                spider_group.add(spider)
                camera_group.add(spider)
                self.timer_spawn = 0

class Water(pygame.sprite.Sprite, Camera):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class SuperGroup(pygame.sprite.Group):
    def camera_update(self, stepx, stepy):
        for sprite in self.sprites():
            sprite.camera_move(stepx, stepy)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.key = pygame.key.get_pressed()
        self.speed = 5
        self.timer_anime = 0
        self.anime = False
        self.frame = 0
        self.pos_maps = [0, 0]
        self.score = 0
        self.axe = 3
        self.camera = False
        self.dir = "top"

    def add_axe(self):
        global axe_group
        axe_group = pygame.sprite.Group()
        for i in range(self.axe):
            axe = Axe(axe_image, (self.rect.centerx + 70, self.rect.centery + 70), (360 // self.axe * i))
            axe_group.add(axe)

    def update(self):
        self.key = pygame.key.get_pressed()
        if self.key[pygame.K_a]:
            self.dir = "left"
            self.rect.x -= self.speed
            if self.rect.left < 300 and self.pos_maps[0] < 0:
                self.pos_maps[0] += self.speed
                camera_group.camera_update(self.speed, 0)
                self.rect.left = 300

        elif self.key[pygame.K_d]:
            self.dir = "right"
            self.rect.x += self.speed
            if self.rect.right > 900 and self.pos_maps[0] > -6800:
                self.pos_maps[0] -= self.speed
                camera_group.camera_update(-self.speed, 0)
                self.rect.right = 900
        elif self.key[pygame.K_w]:
            self.dir = "top"
            self.rect.y -= self.speed
            if self.rect.top < 300 and self.pos_maps[0] < 0:
                self.pos_maps[1] += self.speed
                camera_group.camera_update(0, self.speed)
                self.rect.top = 300
        elif self.key[pygame.K_s]:
            self.dir = "bottom"
            self.rect.y += self.speed
            if self.rect.bottom > 600 and self.pos_maps[1] > -7200:
                self.pos_maps[1] -= self.speed
                camera_group.camera_update(0, -self.speed)
                self.rect.bottom = 600
        if self.key[pygame.K_r]:
            restart()



restart()
drawmaps('1.txt')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    gamelvl()
    clock.tick(FPS)
