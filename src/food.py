import random
from settings import *
from utils import BoardElement

class Food:
    def __init__(self, board, pos=None):
        self.position = self.find_empty_position(board) if pos is None else pos
        if self.position:
            board[self.position[0]][self.position[1]] = BoardElement.FOOD

    def find_empty_position(self, board):
        # max_attempts = int((len(board) * len(board[1])) ** 0.5)
        max_attempts = len(board)
        attempt = 0
        while attempt < max_attempts:
            # Generar una posición aleatoria dentro del tablero
            food_position = (random.randint(1, len(board) - 2), random.randint(1, len(board[0]) - 2))
            # Comprobar si la posición está vacía
            if board[food_position[0]][food_position[1]] == BoardElement.EMPTY:
                return food_position  # Devolver la posición si está vacía
            attempt += 1


        # Si después de varios intentos no se encuentra una posición vacía, usar un enfoque más inteligente
        empty_positions = []  # Lista para almacenar las posiciones vacías
        total_empty_spaces = 0

        # Calcular los espacios vacíos totales y almacenar las posiciones vacías
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == BoardElement.EMPTY:
                    total_empty_spaces += 1
                    empty_positions.append((i, j))

        # Si no hay espacios vacíos, retornar None
        if total_empty_spaces == 0:
            return None

        return random.choice(empty_positions)  # Devolver una posición aleatoria de la lista de posiciones vacías

    def get_draw_info(self):
        return [{'type': 'food', 'position': self.position}]

