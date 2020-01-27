import pygame as pg
from pygame.locals import *
from random import choice, randint

FPS = 60

class Map:
    def __init__(self, strmap, Frame, x=0, y=0):

        self.group = pg.sprite.Group()

        if not isinstance(strmap, list):
            raise ValueError('Mapa ha de ser lista de cadenas')
        for pf, fila in enumerate(strmap):
            if not isinstance(fila, str):
                raise ValueError('Cada fila ha de ser una cadena')

        w = Frame.w
        h = Frame.h

        for pf, fila in enumerate(strmap):
            for pc, t in enumerate(fila):
                if t == 'X':
                    f = Frame(x + pc * w, y + pf * h)
                    self.group.add(f)



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
        self.v = pg.math.Vector2(0, 0)


    def update(self, dt):
        self.rect.x += self.v.x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 800 - self.w:
            self.rect.x = 800-self.w
        self.rect.y += self.v.y
        if self.rect.y <0:
            self.rect.y = 0
        if self.rect.y > 600 - self.h:
            self.rect.y = 600-self.h
            
    @property
    def speed(self):
        return self.v
    
    @speed.setter
    def speed(self, v):
        self.v.x = v[0]
        self.v.y = v[1]


        
class Ball(pg.sprite.Sprite):
    pictures = 'ball.png'

    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y
        self.nC = 0

        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()
        self.ping = pg.mixer.Sound('resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('resources/sounds/lost-point.wav')

        self.rect = self.image.get_rect()
        self.w = self.rect.w
        self.h = self.rect.h

        self.v = pg.math.Vector2(0, 0)

        self.start()

    def start(self):
        self.nC = 0
        self.rect.x = self.x
        self.rect.y = self.y
        self.v.x = choice([-7, 7])
        self.v.y = randint(3, 7) 

    def update(self, dt):
        self.rect.x += self.v.x
        if self.rect.x < 0 or self.rect.x > 800 - self.w:
            self.ping.play()
            self.v.x *= -1

        self.rect.y += self.v.y
        if self.rect.y <0:
            self.ping.play()
            self.v.y *= -1

        if self.rect.y > 600 - self.h:
            self.speed = (0, 0)
            self.lost_point.play()

    def collide_direction(self, r):
        Vr = self.v - r.v

        direccion = pg.math.Vector2(Vr.x/abs(Vr.x) if Vr.x != 0 else 0, Vr.y/abs(Vr.y) if Vr.y != 0 else 0)

        dy = r.rect.center[1] - self.rect.center[1]
        penetracion_y = (r.rect.h+self.rect.h) / 2 - dy
        dx = r.rect.center[0] - self.rect.center[0]
        penetracion_x = (r.rect.w+self.rect.w) / 2 - dx

        penetracion = penetracion_x / penetracion_y

        '''
        posRelAnt = Punto(self.rect.center[0] - Vr.x, self.rect.center[1] - Vr.y)
        dyAnt = r.rect.center[1] - posRelAnt.y
        dxAnt = r.rect.center[0] - posRelAnt.x

        while abs(dyAnt) < (r.h + self.h)/2 and abs(dxAnt) < (r.w + self.w)/2:
            posRelAnt.x -= Vr.x
            posRelAnt.y -= Vr.y
            dyAnt = r.rect.center[1] - posRelAnt.y
            dxAnt = r.rect.center[0] - posRelAnt.x


        if abs(dyAnt) < (r.h + self.h)/2:
            direccion.y = 0
        
        if abs(dxAnt) < (r.w + self.w)/2:
            direccion.x = 0
        '''

        copendienteV = Vr.x/Vr.y

        if copendienteV > penetracion:
            direccion.y = 0
        elif copendienteV < penetracion:
            direccion.x = 0
        
        return direccion.x, direccion.y


    def test_collisions(self, group, borra=False):
        candidates = pg.sprite.spritecollide(self, group, borra)
        nC = len(candidates)
        if nC > 0:
            self.ping.play()
            dx, dy = self.collide_direction(candidates[0])
            if dx !=0:
                self.v.x *= -1
            elif dy !=0:
                self.v.y *= -1
            
            self.nC += 1
            if self.nC == 5:
                length = self.v.length()
                self.v.scale_to_length(length * 1.1)
                print(self.v.length())
                self.nC = 0

        return nC

    @property
    def speed(self):
        return self.v
    
    @speed.setter
    def speed(self, v):
        self.v.x = v[0]
        self.v.y = v[1]



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

        self.v = pg.math.Vector2(0, 0)

    @property
    def speed(self):
        return self.v
    
    @speed.setter
    def speed(self, v):
        self.v.x = v[0]
        self.v.y = v[1]
