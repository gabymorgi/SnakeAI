from settings import *
import random
from snake import Snake
from food import Food
from utils import BoardElement, Direction
from event_emitter import EventEmitter
from typing import List
import math

def distribute_players(num_players):
    division = num_players // 4
    rest = num_players % 4
    result = [division] * 4

    for i in range(rest):
        result[i] += 1

    return result

def initialize_snakes(num_players, width, height):
    radio = math.ceil(num_players / 4)
    center = (width // 2, height // 2)
    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    players_per_side = distribute_players(num_players)
    players_positions = []
    for i in range(4):
        initial_x = center[0] + radio * (directions[i][0] + directions[(i - 1) % 4][0]) + directions[(i + 1) % 4][0]
        initial_y = center[1] + radio * (directions[i][1] + directions[(i - 1) % 4][1]) + directions[(i + 1) % 4][1]
        for j in range(players_per_side[i]):
            # snake length is 3
            x = initial_x
            y = initial_y
            actual_player_positions = []
            for k in range(3):
                actual_player_positions.insert(0, (x, y))
                x += directions[i][0]
                y += directions[i][1]
            players_positions.append({
                "positions": actual_player_positions,
                "direction": directions[i],
            })
            initial_x += directions[(i + 1) % 4][0] * 2
            initial_y += directions[(i + 1) % 4][1] * 2

    return players_positions

class Game:
    def __init__(self, data, size=(10, 10)):
        self.events = EventEmitter()
        # create board
        self.board = [[BoardElement.EMPTY for _ in range(size[1])] for _ in range(size[0])]
        # set wall boundaries
        for i in range(size[0]):
            self.board[i][0] = BoardElement.WALL
            self.board[i][size[1]-1] = BoardElement.WALL
        for i in range(size[1]):
            self.board[0][i] = BoardElement.WALL
            self.board[size[0]-1][i] = BoardElement.WALL

        players = data["players"]
        players_data = initialize_snakes(len(players), size[0], size[1])
        self.snakes: List[Snake] = []
        for i, player in enumerate(players):
            snake = Snake(self.board, player, {
                "positions": players_data[i]["positions"],
                "direction": players_data[i]["direction"],
                "id": i,
            })
            snake.events.on('hit', self.handle_snake_hit)
            snake.events.on('eat', self.handle_food_eatten)
            snake.events.on('no energy', self.handle_snake_hit)
            for pos in snake.positions:
                self.board[pos[0]][pos[1]] = BoardElement.SNAKE
            self.snakes.append(snake)

        # food_position = (random.randint(1, size[0]-2), random.randint(1, size[1]-2))
        self.foods = [Food(self.board) for _ in range(len(players))]

    def update(self):
        # make a random array from 0 to len(snakes) - 1
        random_order = list(range(len(self.snakes)))
        random.shuffle(random_order)
        snakes_turn = []
        for i in random_order:
            snakes_turn.append(self.snakes[i])
        food_positions = [food.position for food in self.foods]
        for snake in snakes_turn:
            snake.move(self.board, food_positions)

    def handle_snake_hit(self, id):
        # convert snake into food
        snake = [snake for snake in self.snakes if snake.id == id][0]
        for pos in snake.positions:
            self.board[pos[0]][pos[1]] = BoardElement.FOOD
            self.foods.append(Food(self.board, pos))
        # remove snake from list, check by id
        self.snakes = [snake for snake in self.snakes if snake.id != id]

        if len(self.snakes) == 0:
            self.game_over()

    def game_over(self):
        self.events.emit('game_over')

    def handle_food_eatten(self, position):
        # remove food from list, check by position
        self.foods = [food for food in self.foods if food.position != position]
        if len(self.foods) < len(self.snakes):
            self.foods.append(Food(self.board))

    def get_draw_info(self):
        draw_info = []
        
        draw_info.append({'type': 'game', 'board': self.board})
        food_positions = [food.position for food in self.foods]
        for snake in self.snakes:
            draw_info.extend(snake.get_draw_info(self.board, food_positions))
        for food in self.foods:
            draw_info.extend(food.get_draw_info())

        return draw_info

if __name__ == '__main__':
    game = Game()
    game.run()
