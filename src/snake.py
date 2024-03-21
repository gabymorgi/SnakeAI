import numpy as np
from settings import *
from utils import Direction, BoardElement, Rotation
from event_emitter import EventEmitter

class Snake:
    def __init__(self, board, player, data = {}):
        self.id = data.get('id', 0)
        self.events = EventEmitter()
        self.positions = data.get("positions", [(5, 5), (5, 6), (5, 7)])
        for pos in self.positions:
            board[pos[0]][pos[1]] = BoardElement.SNAKE
        self.direction = data.get("direction", Direction.UP)
        self.player = player
        self.energy = data.get('energy', 100)

    def move(self, board, foods):
        rotation = self.player.act({
            'board': board,
            'foods': foods,
            'positions': self.positions,
            'direction': self.direction,
            'energy': self.energy,
        })
        # print(id, rotation)
        self.direction = Direction.rotate(self.direction, rotation)
        new_head_pos = (self.positions[0][0] + self.direction[0],
                        self.positions[0][1] + self.direction[1])
        
        if (board[new_head_pos[0]][new_head_pos[1]] == BoardElement.WALL or
            board[new_head_pos[0]][new_head_pos[1]] == BoardElement.SNAKE):
                print('Hit', self.id)
                self.events.emit('hit', self.id)
        elif board[new_head_pos[0]][new_head_pos[1]] == BoardElement.FOOD:
            self.positions.insert(0, new_head_pos)
            board[new_head_pos[0]][new_head_pos[1]] = BoardElement.SNAKE
            self.energy += 10
            # print('Eat')
            self.events.emit('eat', new_head_pos)
        else:
            self.positions.insert(0, new_head_pos)
            board[new_head_pos[0]][new_head_pos[1]] = BoardElement.SNAKE
            tail = self.positions.pop()
            board[tail[0]][tail[1]] = BoardElement.EMPTY
        
        self.energy -= 1
        if self.energy <= 0:
            self.events.emit('no energy')
            print('No energy')

    def get_draw_info(self, board, foods):
        self.player.act({
            'board': board,
            'foods': foods,
            'positions': self.positions,
            'direction': self.direction,
            'energy': self.energy,
        })
        player_info = self.player.get_draw_info()
        return [{
            'id': self.id,
            'type': 'snake',
            'positions': self.positions,
            'direction': self.direction,
            'energy': self.energy,
            **player_info
        }]