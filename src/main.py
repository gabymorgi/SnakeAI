# Example file showing a circle moving on screen
import pygame
import sys
from pygame.locals import *
from game import Game
from settings import *
from renderer.renderer import Renderer
from players.keyboard_player import Player
from players.basic_player import Basic_Player
from players.first_person_player import FP_Player
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "1000,0"

set_game_size(10)
set_players_amount(4)
is_hooman_player = False
FPS = 6
speed = 3
frames_per_update = FPS // speed

# pygame setup
pygame.init()
display_width = 1900
display_height = 1000
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
dt = 0

class main():
    def __init__(self):
        self.running = True
        self.frames_since_last_update = 0
    
    def on_game_over(self):
        print('Game Over!')
        self.running = False

    def run(self):
        renderer = Renderer(screen, get_players_amount())
        # set players taking player_amount from settings
        players = [FP_Player() for _ in range(get_players_amount())]
        if is_hooman_player:
            players[0] = Player()
        game_data = {"players": players}
        game = Game(size=(get_game_size(), get_game_size()), data=game_data)
        game.events.on('game_over', self.on_game_over)
        entities = game.get_draw_info()
        renderer.draw_entities(entities)
        clock.tick(1)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if is_hooman_player:
                players[0].on_tick()

            # Incrementa el contador de frames desde la última actualización
            self.frames_since_last_update += 1

            # Actualiza el juego si es tiempo según la velocidad definida
            if self.frames_since_last_update >= frames_per_update:
                self.frames_since_last_update = 0  # Resetea el contador de frames
                game.update()
                # Dibuja en pantalla
                entities = game.get_draw_info()
                renderer.draw_entities(entities)
                # pygame.display.flip()


            # Controla la velocidad de los frames
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main().run()
