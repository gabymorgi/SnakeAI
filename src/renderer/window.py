import pygame
from utils import BoardElement
from settings import *
from renderer.common import *
import numpy as np


class Window:
    def __init__(self, available_space, cell_size=50):
        self.window_width = available_space[0]
        self.window_height = available_space[1]
        self.cell_size = cell_size
        self.grid_width = self.window_width // cell_size
        self.grid_height = self.window_height // cell_size
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=bool)  # False = libre, True = ocupado
        self.assigned_surfaces = {}
        self.surface_id_counter = 0

    def find_free_space(self, width, height):
        required_cells_x = math.ceil(width / self.cell_size)
        required_cells_y = math.ceil(height / self.cell_size)

        for y in range(self.grid_height - required_cells_y + 1):
            for x in range(self.grid_width - required_cells_x + 1):
                area = self.grid[y:y+required_cells_y, x:x+required_cells_x]
                if not area.any():  # Si todo el área está libre (False)
                    self.mark_grid_as_occupied(x, y, required_cells_x, required_cells_y)
                    return x, y  # Devuelve la posición
        return None  # No se encontró espacio

    def get_empty_surface(self, width, height):
        position = self.find_free_space(width, height)
        if position is None:
            print("No hay espacio disponible")
            return (0, 0)
        
        new_surface_id = self.surface_id_counter
        self.surface_id_counter += 1

        pixel_pos = (position[0] * self.cell_size, position[1] * self.cell_size)
        self.assigned_surfaces[new_surface_id] = pixel_pos
        print("New surface at", position, pixel_pos)
        return pixel_pos

    def mark_grid_as_occupied(self, grid_x, grid_y, cells_x, cells_y):
        self.grid[grid_y:grid_y+cells_y, grid_x:grid_x+cells_x] = True

        