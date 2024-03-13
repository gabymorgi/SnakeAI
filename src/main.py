# Example file showing a circle moving on screen
import pygame
import sys
from pygame.locals import *
from game import Game
from settings import CELL_SIZE
from renderer import Renderer
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
# pygame setup
pygame.init()
game_size = 9
display_size = CELL_SIZE * (game_size - 1)
screen = pygame.display.set_mode((display_size, display_size))
clock = pygame.time.Clock()
dt = 0

# pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,
#                           K_LEFT, K_RIGHT, K_UP, K_DOWN,
#                           K_w, K_a, K_s, K_d])


class main():
    running = True
    
    def on_game_over(self):
        print('Game Over!')
        self.running = False

    def run(self):
        renderer = Renderer()
        game = Game(size=(game_size, game_size))
        game.events.on('game_over', self.on_game_over)
        entities = game.get_draw_info()
        renderer.draw_entities(entities, screen)
        pygame.display.flip()

        clock.tick(1)

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            game.update()
            entities = game.get_draw_info()
            renderer.draw_entities(entities, screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(2) / 1000

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main().run()
