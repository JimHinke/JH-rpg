import pygame, sys
from level import Level

class Game:
    def __init__(self):

        pygame.init()
        self.WIDTH = 1080
        self.HEIGTH = 640
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGTH))
        pygame.display.set_caption('JH-RPG')
        self.clock = pygame.time.Clock()

        self.level = Level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    game = Game()
    game.run()