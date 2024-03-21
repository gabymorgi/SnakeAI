from utils import Direction, Rotation, BoardElement
from players.vision import *
    
class Basic_Player:
    def __init__(self):
        super().__init__() 
        self.name = "Basic"

    def act(self, data):
        board = data['board']
        positions = data['positions']
        direction = data['direction']
        foods = data['foods']

        # Encontrar la comida más cercana
        head = positions[0]
        closest_food = min(foods, key=lambda food: distance(head, food))

        # Dirección deseada hacia la comida más cercana
        desired_direction = get_direction_to_food(head, closest_food)

        cycle = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

        # Encontrar la rotación necesaria para llegar a la dirección deseada
        rotation = Direction.min_rotation(direction, desired_direction)
        direction_index = cycle.index(direction)
        # chequear si la dirección en la rotación es segura
        new_pos = (head[0] + cycle[(direction_index + rotation) % 4][0],
                   head[1] + cycle[(direction_index + rotation) % 4][1])
        if is_safe(new_pos, board) and are_free_space(new_pos, board, len(positions)):
            return rotation
        else:
            # Si no es segura, buscar una dirección segura en sentido horario
            for i in range(-1, 2):
                new_pos = (head[0] + cycle[(direction_index + i) % 4][0],
                           head[1] + cycle[(direction_index + i) % 4][1])
                if is_safe(new_pos, board) and are_free_space(new_pos, board, len(positions)):
                    return i
        return rotation

    def get_draw_info(self):
        return {'name': self.name}