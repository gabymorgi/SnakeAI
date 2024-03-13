import pygame
from utils import BoardElement
from settings import *

class Renderer:
    def draw_entities(self, entities_info, surface):
        for entity_info in entities_info:
            if entity_info['type'] == 'game':
                self.draw_game(entity_info, surface)
            elif entity_info['type'] == 'snake':
                self.draw_snake(entity_info, surface)
            elif entity_info['type'] == 'food':
                self.draw_food(entity_info, surface)
            else:
                print('Unknown entity type:', entity_info['type'])

    def draw_game(_, game, surface):
        surface.fill(BLACK)
        # Dibujar el tablero
        for y in range(len(game['board'])):
            for x in range(len(game['board'][y])):
                if game['board'][y][x] == BoardElement.WALL:
                    rect = pygame.Rect(x*20 - HALF_CELL_SIZE, y*20 - HALF_CELL_SIZE, 20, 20)
                    pygame.draw.rect(surface, WHITE, rect)
                else:
                    rect = pygame.Rect(x*20 - HALF_CELL_SIZE, y*20 - HALF_CELL_SIZE, 20, 20)
                    pygame.draw.rect(surface, WHITE, rect, 1)

    def draw_snake(_, snake, surface):
        # Dibujar un rectángulo para cada par de posiciones adyacentes
        for i in range(len(snake['positions']) - 1):
            pygame.draw.circle(surface, SNAKE_COLOR, (
                snake['positions'][i][0] * CELL_SIZE, snake['positions'][i][1] * CELL_SIZE
                ), HALF_CELL_SIZE)
            
            # Dibujar un rectángulo desde el centro de una celda al centro de la siguiente
            x1, y1 = snake['positions'][i]
            x2, y2 = snake['positions'][i + 1]
            # Convertir las coordenadas de la celda a coordenadas de píxeles
            x1_px, y1_px = (x1 * CELL_SIZE), (y1 * CELL_SIZE)
            x2_px, y2_px = (x2 * CELL_SIZE), (y2 * CELL_SIZE)
            # Calcular la posición del rectángulo
            rect_x = x1_px - HALF_CELL_SIZE if x1 == x2 else min(x1_px, x2_px)
            rect_y = y1_px - HALF_CELL_SIZE if y1 == y2 else min(y1_px, y2_px)
            pygame.draw.rect(surface, SNAKE_COLOR, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
        # Dibujar la cola de la serpiente como un círculo
        pygame.draw.circle(
            surface,
            SNAKE_COLOR,
            (snake['positions'][-1][0] * CELL_SIZE, snake['positions'][-1][1] * CELL_SIZE),
            HALF_CELL_SIZE)
        
    def draw_food(_, food, surface):
        # Dibujar un círculo
        x, y = food['position']
        x = x * CELL_SIZE
        y = y * CELL_SIZE
        pygame.draw.circle(surface, FOOD_COLOR, (x, y), HALF_CELL_SIZE)