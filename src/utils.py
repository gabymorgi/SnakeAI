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
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    @classmethod
    def direction_to_index(cls, direction):
        direction_mapping = {
            cls.UP: 0,
            cls.RIGHT: 1,
            cls.DOWN: 2,
            cls.LEFT: 3
        }
        return direction_mapping[direction]
    
    @classmethod
    def min_rotation(cls, from_direction, to_direction):
        from_index = cls.direction_to_index(from_direction)
        to_index = cls.direction_to_index(to_direction)
        
        # Calcula la diferencia en ambos sentidos
        clockwise = (to_index - from_index) % 4
        counterclockwise = (from_index - to_index) % 4
        
        # Determina la rotación óptima limitada entre -1, 0, 1
        if clockwise < counterclockwise:
            return min(clockwise, 1)
        else:
            return max(-1, -counterclockwise)
        
    @classmethod
    def rotate(cls, direction, rotation):
        cycle = [cls.UP, cls.RIGHT, cls.DOWN, cls.LEFT]
        direction_index = cls.direction_to_index(direction)
        return cycle[(direction_index + rotation) % 4]
