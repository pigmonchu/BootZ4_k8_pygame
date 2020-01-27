import pygame as pg
from pygame.locals import *
import sys

from entities import *

FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

level1 = ['',
          '-XXXXXXXXXXXXXX-',
          '-X------------X-',
          '-X------------ X-',
          '-XXXXXXXXXXXXXX-']


class Game:
    clock = pg.time.Clock()
    score = 0

    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption('Mi Arcanoid')

        self.background_img = pg.image.load('resources/background.png').convert()

        self.fontGran = pg.font.Font('resources/fonts/font.ttf', 40)
        self.font = pg.font.Font('resources/fonts/font.ttf', 28)
        self.marcador = self.font.render('0', True, WHITE)
        self.livescounter = self.font.render('0', True, WHITE)
        self.text_game_over = self.fontGran.render('GAME OVER', True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Insert coin', True, WHITE)

        self.player = Racket()
        self.ball = Ball()
        self.tileGroup = None

        self.playerGroup = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()
        self.playerGroup.add(self.player)

        self.start_partida()

    def create_tiles(self):
        self.tileGroup.empty()
        self.allSprites.add(self.tileGroup)


    def start_partida(self):
        self.player.lives = 3
        self.ball.start()
        self.allSprites.empty()
        self.allSprites.add(self.player)
        self.allSprites.add(self.ball)
        self.tileGroup = Map(level1, Tile).group
        self.allSprites.add(self.tileGroup)
        self.score = 0

    def quitGame(self):
        pg.quit()
        sys.exit()

    def handleEvents_GO(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitGame()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.start_partida()


    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitGame()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.player.v.x = -10
                
                if event.key == K_RIGHT:
                    self.player.v.x = 10

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.player.v.x = -10
        elif keys_pressed[K_RIGHT]:
            self.player.v.x = 10
        else:
            self.player.v.x = 0

    def mainloop(self):
        while True:
            dt = self.clock.tick(FPS)

            if self.player.lives > 0:
                self.bucle_partida(dt)
            else: 
                self.gameOver()

            pg.display.flip()

    def bucle_partida(self, dt):
        self.handleEvents()

        self.ball.test_collisions(self.playerGroup)
        self.score += self.ball.test_collisions(self.tileGroup, True)

        if self.ball.speed.length() == 0: #se ha producido colision
            self.player.lives -= 1
            self.ball.start()

        if self.player.lives == 0:
            self.gameOver()

        self.livescounter = self.font.render(str(self.player.lives), True, WHITE)
        self.marcador = self.font.render(str(self.score), True, WHITE)

        self.screen.blit(self.background_img, (0, 0))

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen)

        self.screen.blit(self.marcador, (750, 10))
        self.screen.blit(self.livescounter, (50, 10))

    def gameOver(self):
        self.handleEvents_GO()

        rect = self.text_game_over.get_rect()
        self.screen.blit(self.text_game_over, ((800 - rect.w)//2, 300))
        rect = self.text_insert_coin.get_rect()
        self.screen.blit(self.text_insert_coin, ((800 - rect.w)//2, 380))





if __name__ == '__main__':
    pg.init()
    game = Game()
    game.mainloop()

