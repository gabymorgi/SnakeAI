import math

# Dimensiones de la ventana de juego
CELL_SIZE = 20
HALF_CELL_SIZE = CELL_SIZE // 2

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuraciones de la comida
FOOD_COLOR = RED

# Configuraciones de la fuente
FONT_SIZE = 24

# Editable por el usuario
game_size = 20
def set_game_size(size):
    global game_size
    game_size = size
def get_game_size():
    return game_size

players_amount = 4
def set_players_amount(amount):
    global players_amount
    players_amount = amount
    recommended_size = 11 + math.ceil(amount / 2)
    if recommended_size > game_size:
        set_game_size(recommended_size)
def get_players_amount():
    return players_amount