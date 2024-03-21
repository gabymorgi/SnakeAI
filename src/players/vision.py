import math
from collections import deque
from utils import Direction, BoardElement

def is_safe(next_pos, board):
    x, y = next_pos
    if 0 <= x < len(board) and 0 <= y < len(board[0]):
        return board[x][y] in [BoardElement.EMPTY, BoardElement.FOOD]
    return False

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_direction_to_food(head, food):
    if food[0] < head[0]:
        return Direction.LEFT
    elif food[0] > head[0]:
        return Direction.RIGHT
    elif food[1] < head[1]:
        return Direction.UP
    else:
        return Direction.DOWN

def are_free_space(start_pos, board, snake_length):
    visited = set()
    queue = deque([start_pos])
    visited.add(start_pos)
    free_space = 0

    while queue and free_space < snake_length:
        current_pos = queue.popleft()
        free_space += 1

        for direction in [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]:
            next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            if next_pos not in visited and is_safe(next_pos, board):
                queue.append(next_pos)
                visited.add(next_pos)

    return free_space >= snake_length

def ray_cast(board, start_point, angle):
    radians = math.radians(angle)
    
    # ray direction
    dx = math.cos(radians)
    dy = math.sin(radians)
    
    distance = 1

    x_actual = start_point[0] + 0.5 + dx * distance
    y_actual = start_point[1] + 0.5 + dy * distance
    
    distance_step = 0.1
    
    while (0 <= int(x_actual) < len(board[0])) and (0 <= int(y_actual) < len(board)):
        if board[int(x_actual)][int(y_actual)] != 0:
            return (angle, board[int(x_actual)][int(y_actual)], distance)
        
        x_actual += dx * distance_step
        y_actual += dy * distance_step
        distance += distance_step
    
    # no object found
    return (angle, None, distance)