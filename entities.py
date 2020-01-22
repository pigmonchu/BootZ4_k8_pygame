import pygame as pg
from pygame.locals import *
from random import choice, randint

FPS = 60

level1 = ['-X-XXX-X',
          'XXXXXXXXX',
          'XX-X'
]



class Map:
    def __init__(self, strmap)
        self.group = sprite.Group()

        <Toda la lógica de la creación de los Tiles, su posición y agruparlos>

        return self.group



class Racket(pg.sprite.Sprite):
    pictures = 'racket_horizontal.png'
    speed = 10
    lives = 3

    def __init__(self, x=355, y=580):
        self.x = x
        self.y = y

        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = self.rect.w
        self.h = self.rect.h

    def go_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)
        
    def go_right(self):
        self.rect.x = min(self.rect.x + self.speed, 800-self.w)
        
class Ball(pg.sprite.Sprite):
    pictures = 'ball.png'
    dx = 1
    dy = 1
    speed = 5

    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y

        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()
        self.ping = pg.mixer.Sound('resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('resources/sounds/lost-point.wav')

        self.rect = self.image.get_rect()
        self.w = self.rect.w
        self.h = self.rect.h

        self.start()

    def start(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 5
        self.dy = 1
        self.dx = choice([-1, 1])

    def update(self, dt):
        self.rect.x = self.rect.x + self.speed * self.dx
        self.rect.y = self.rect.y + self.speed * self.dy

        if self.rect.y >= 600 - self.h:
            self.speed = 0
            self.lost_point.play()

        if self.rect.y <= 0:
            self.dy = self.dy * -1
            self.ping.play()

        if self.rect.x <=0:
            self.dx = self.dx * -1
            self.ping.play()

        if self.rect.x >= 800 - self.w:
            self.dx = self.dx * -1        
            self.ping.play()

    def test_collisions(self, group, borra=False):
        candidates = pg.sprite.spritecollide(self, group, borra)
        nC = len(candidates)
        if nC > 0:
            self.dy *= -1
            self.ping.play()
        return nC

class Tile(pg.sprite.Sprite):
    w = 50
    h = 32

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((self.w, self.h), SRCALPHA, 32)
        pg.draw.rect(self.image, (randint(0, 255), randint(0, 255), randint(0, 255)),(2, 2, self.w-4, self.h-4))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y