from utils import Direction, Rotation, BoardElement
from players.vision import *
    
class FP_Player:
    def __init__(self):
        super().__init__() 
        self.ray_casts = []
        self.name = "First Person"

    def act(self, data):
        board = data['board']
        positions = data['positions']
        direction = data['direction']
        foods = data['foods']

        angle_half_range = 145
        cycle_dir = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        cycle_angle = [-90, 0, 90, 180]
        angle_from = cycle_angle[cycle_dir.index(direction)] - angle_half_range
        angle_to = cycle_angle[cycle_dir.index(direction)] + angle_half_range
        angle_step = 10
        self.ray_casts = []
        for angle in range(angle_from, angle_to, angle_step):
            cast = ray_cast(board, positions[0], angle % 360)
            self.ray_casts.append(cast)


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
        return {'ray_casts': self.ray_casts, 'name': self.name}