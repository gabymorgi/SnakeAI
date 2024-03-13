# enum para los elementos del tablero
class BoardElement:
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FOOD = 3

# enum para las rotaciones
class Rotation:
    RIGHT = 1
    NONE = 0
    LEFT = -1

# enum para las direcciones
class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)