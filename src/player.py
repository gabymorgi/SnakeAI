import pygame
from pygame.locals import *
from utils import Rotation

BLUE  = (0, 0, 255)
SCREEN_WIDTH = 400

class Player:
    def __init__(self):
        super().__init__() 

    def act(self):
        pressed_keys = pygame.key.get_pressed()
        rotation = Rotation.NONE
        if pressed_keys[K_LEFT]:
            rotation = Rotation.LEFT
        elif pressed_keys[K_RIGHT]:
            rotation = Rotation.RIGHT
        return rotation
