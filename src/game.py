from settings import *
from snake import Snake
from food import Food
from utils import BoardElement, Direction
from event_emitter import EventEmitter
from player import Player

class Game:
    foods = []
    def __init__(self, size=(10, 10)):
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

        player = Player()
        self.snake = Snake(self.board, player=player, data={"positions": [(5, 5), (6, 5), (7, 5)]})
        self.snake.events.on('hit', self.game_over)
        self.snake.events.on('eat', self.handle_food_eatten)

        # food_position = (random.randint(1, size[0]-2), random.randint(1, size[1]-2))
        self.foods.append(Food(self.board))

    def update(self):
        self.snake.move(self.board)

    def game_over(self):
        self.events.emit('game_over')

    def handle_food_eatten(self, position):
        # remove food from list, check by position
        self.foods = [food for food in self.foods if food.position != position]
        self.foods.append(Food(self.board))

    def get_draw_info(self):
        draw_info = []
        
        draw_info.append({'type': 'game', 'board': self.board})
        draw_info.extend(self.snake.get_draw_info())
        for food in self.foods:
            draw_info.extend(food.get_draw_info())

        return draw_info

if __name__ == '__main__':
    game = Game()
    game.run()
