import numpy as np
from settings import *
from utils import Direction, BoardElement, Rotation
from event_emitter import EventEmitter

class Snake:
    def __init__(self, board, player, data = None):
        self.events = EventEmitter()
        if data["positions"]:
            self.positions = data["positions"]  # Lista de posiciones de la serpiente
        else:
            self.positions = [(5, 5), (5, 6), (5, 7)]  # Posiciones iniciales
        for pos in self.positions:
            board[pos[0]][pos[1]] = BoardElement.SNAKE
        self.direction = Direction.UP  # Dirección inicial
        self.player = player  # Jugador al que pertenece la serpiente
    
    def get_draw_info(self):
        return [{'type': 'snake', 'positions': self.positions}]
    
    def rotate_direction(self, rotation):
        # Convertir la dirección actual en un vector numpy
        current_vector = np.array(self.direction)
        
        # Definir la matriz de rotación según la dirección de la rotación
        if rotation == Rotation.RIGHT:
            rotation_matrix = np.array([[0, -1], [1, 0]])  # Rotación en sentido horario
        elif rotation == Rotation.LEFT:
            rotation_matrix = np.array([[0, 1], [-1, 0]])  # Rotación en sentido antihorario
        else:
            return
        
        # Aplicar la rotación multiplicando el vector por la matriz de rotación
        new_vector = np.dot(rotation_matrix, current_vector)
        
        # Convertir el nuevo vector de vuelta a una tupla de dirección
        new_direction = tuple(new_vector.astype(int))
        
        # Actualizar la dirección de la serpiente
        self.direction = new_direction

    def move(self, board):
        rotation = self.player.act()
        self.rotate_direction(rotation)
        new_head_pos = (self.positions[0][0] + self.direction[0],
                        self.positions[0][1] + self.direction[1])
        
        if (board[new_head_pos[0]][new_head_pos[1]] == BoardElement.WALL or
            board[new_head_pos[0]][new_head_pos[1]] == BoardElement.SNAKE):
                print('Hit')
                self.events.emit('hit')
                return False
        elif board[new_head_pos[0]][new_head_pos[1]] == BoardElement.FOOD:
            self.positions.insert(0, new_head_pos)
            board[new_head_pos[0]][new_head_pos[1]] = BoardElement.SNAKE
            print('Eat')
            self.events.emit('eat', new_head_pos)
            return True
        else:
            self.positions.insert(0, new_head_pos)
            board[new_head_pos[0]][new_head_pos[1]] = BoardElement.SNAKE
            tail = self.positions.pop()
            board[tail[0]][tail[1]] = BoardElement.EMPTY
            # print('Move to', new_head_pos)
            return True
