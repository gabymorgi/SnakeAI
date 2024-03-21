import pygame
from utils import BoardElement, Direction
from settings import *
from renderer.common import *
from renderer.window import Window

WIN_WIDTH = 150
WIN_HEIGHT = 200

class Renderer:
    def __init__(self, screen, players_amout):
        self.screen = screen
        self.window = Window((screen.get_width(), screen.get_height()))
        size = CELL_SIZE * (get_game_size() - 1)
        self.game_surface = self.window.get_empty_surface(size, size)
        self.snake_data = []
        color_step = 330 / (players_amout + 1)
        for i in range(players_amout):
            self.snake_data.append({
                'color': ((i + 1) * color_step) + 15,
                'win_pos': self.window.get_empty_surface(WIN_WIDTH, WIN_HEIGHT)
                })

    def draw_entities(self, entities_info):
        for entity_info in entities_info:
            if entity_info['type'] == 'game':
                self.draw_game(entity_info)
            elif entity_info['type'] == 'snake':
                self.draw_snake(entity_info)
            elif entity_info['type'] == 'food':
                self.draw_food(entity_info)
            else:
                print('Unknown entity type:', entity_info['type'])

        pygame.display.flip()

    def draw_game(self, game):
        surface = self.screen
        surface.fill(BLACK)
        # Dibujar el tablero
        for y in range(len(game['board'])):
            for x in range(len(game['board'][y])):
                if game['board'][x][y] == BoardElement.WALL:
                    rect = pygame.Rect(x*20 - HALF_CELL_SIZE, y*20 - HALF_CELL_SIZE, 20, 20)
                    pygame.draw.rect(surface, WHITE, rect)
                else:
                    rect = pygame.Rect(x*20 - HALF_CELL_SIZE, y*20 - HALF_CELL_SIZE, 20, 20)
                    pygame.draw.rect(surface, WHITE, rect, 1)

        # colors = [WHITE, BLACK, GREEN, RED]
        # offset = CELL_SIZE * 10
        # for y in range(len(game['board'])):
        #     for x in range(len(game['board'][y])):
        #         rect = pygame.Rect(offset + x*20 - HALF_CELL_SIZE, y*20 - HALF_CELL_SIZE, 20, 20)
        #         pygame.draw.rect(surface, colors[game['board'][x][y]], rect)

    def draw_snake(self, snake):
        surface = self.screen
        # check color

        rgb_color = hue_to_rgb(self.snake_data[snake['id']]['color'])
        text_position = self.snake_data[snake['id']]['win_pos']
        draw_text(surface, text_position,
                  f"{(snake['name'])}: {str(snake['energy'])}",
                  rgb_color)
        
        # if ray_casts:
        if 'ray_casts' in snake:
            self.draw_ray_casts(surface,
                                self.snake_data[snake['id']]['win_pos'],
                                snake['direction'],
                                snake['ray_casts'])

        # Dibujar un rectángulo para cada par de posiciones adyacentes
        for i in range(len(snake['positions']) - 1):
            pygame.draw.circle(surface, rgb_color, (
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
            pygame.draw.rect(surface, rgb_color, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
        # Dibujar la cola de la serpiente como un círculo
        pygame.draw.circle(
            surface,
            rgb_color,
            (snake['positions'][-1][0] * CELL_SIZE, snake['positions'][-1][1] * CELL_SIZE),
            HALF_CELL_SIZE)

        #dibujarle ojitos a la serpiente
        x1, y1 = snake['positions'][0]
        x2, y2 = snake['positions'][1]
        x1_px, y1_px = (x1 * CELL_SIZE), (y1 * CELL_SIZE)
        x2_px, y2_px = (x2 * CELL_SIZE), (y2 * CELL_SIZE)
        if x1 == x2:
            if y1 > y2:
                pygame.draw.circle(surface, BLACK, (x1_px + 3, y1_px + 3), 2)
                pygame.draw.circle(surface, BLACK, (x1_px - 3, y1_px + 3), 2)
            else:
                pygame.draw.circle(surface, BLACK, (x1_px + 3, y1_px - 3), 2)
                pygame.draw.circle(surface, BLACK, (x1_px - 3, y1_px - 3), 2)
        else:
            if x1 > x2:
                pygame.draw.circle(surface, BLACK, (x1_px + 3, y1_px - 3), 2)
                pygame.draw.circle(surface, BLACK, (x1_px + 3, y1_px + 3), 2)
            else:
                pygame.draw.circle(surface, BLACK, (x1_px - 3, y1_px - 3), 2)
                pygame.draw.circle(surface, BLACK, (x1_px - 3, y1_px + 3), 2)
        
    def draw_food(self, food):
        surface = self.screen
        # Dibujar un círculo
        x, y = food['position']
        x = x * CELL_SIZE
        y = y * CELL_SIZE
        pygame.draw.circle(surface, FOOD_COLOR, (x, y), HALF_CELL_SIZE)
    
    def draw_ray_casts(self, surface, win_pos, snake_dir, ray_casts):
        center = (win_pos[0] + WIN_WIDTH // 2, win_pos[1] + WIN_HEIGHT // 2)
        cycle_dir = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        cycle_angle = [0, -90, 180, 90]
        for ray_cast in ray_casts:
            angle, element, distance = ray_cast
            if element == BoardElement.WALL:
                color = WHITE
            elif element == BoardElement.FOOD:
                color = RED
            else:
                color = BLUE
            angle_offset = cycle_angle[cycle_dir.index(snake_dir)]
            angle_from = angle - 2 + angle_offset
            angle_to = angle + 2 + angle_offset
            radius_from = 10
            radius_to = (1 / distance) * 60
            draw_wedge(surface, center, angle_from, angle_to, radius_from, radius_to, color)