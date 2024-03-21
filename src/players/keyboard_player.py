import pygame
from pygame.locals import *
from utils import Rotation

class Player:
    def __init__(self):
        super().__init__() 
        self.buffer = []
        self.name = "Keyboard"

    def act(self, _):
        # ponderar las acciones del buffer de menos a mas
        actions = {}
        weight = 1
        for action in self.buffer:
            if action in actions:
                actions[action] += weight
            else:
                actions[action] = weight
            weight += 1
        self.buffer = []

        # seleccionar la acción con mayor ponderación
        max_weight = 0
        selected_action = Rotation.NONE
        for action, weight in actions.items():
            if weight > max_weight:
                max_weight = weight
                selected_action = action

        return selected_action

    def get_draw_info(self):
        return {'name': self.name}
    
    def on_tick(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.buffer.append(Rotation.LEFT)
        elif pressed_keys[K_RIGHT]:
            self.buffer.append(Rotation.RIGHT)
        else:
            self.buffer.append(Rotation.NONE)
