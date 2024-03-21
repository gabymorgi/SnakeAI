import math
import pygame
from settings import *

def get_more_distinct_color(selected_hues):
    if not selected_hues or len(selected_hues) == 0:
        return 30
    if len(selected_hues) == 1:
        return 330
    
    sorted_hues = sorted(selected_hues)
    
    max_gap = 0
    hue_before_gap = 0
    for i in range(len(sorted_hues) - 1):
        gap = sorted_hues[i + 1] - sorted_hues[i]
        if gap > max_gap:
            max_gap = gap
            hue_before_gap = sorted_hues[i]
    
    most_distinct_hue = (hue_before_gap + max_gap // 2)
    
    return most_distinct_hue

def hue_to_rgb(hue):
    # Convertir hue a la región del círculo de color HSL
    c = 1  # Saturación al 100% implica que C (chroma) es máximo
    x = (1 - abs((hue / 60) % 2 - 1))  # Intermedio para el segundo color RGB más prominente
    m = 0.5 - c / 2  # Ajuste de luminosidad al 50%

    c = c + m
    x = x + m

    if hue < 60:
        r, g, b = c, x, m
    elif hue < 120:
        r, g, b = x, c, m
    elif hue < 180:
        r, g, b = m, c, x
    elif hue < 240:
        r, g, b = m, x, c
    elif hue < 300:
        r, g, b = x, m, c
    else:
        r, g, b = c, m, x

    # Convertir de 0-1 a 0-255
    return int(r * 255), int(g * 255), int(b * 255)

def draw_wedge(surface, center, angle_from, angle_to, radius_from, radius_to, color):
    # Lista para almacenar puntos de la cuña
    points = []

    for angle in range(angle_from, angle_to + 1):
        rad = math.radians(angle)
        x = center[0] + radius_from * math.cos(rad)
        y = center[1] + radius_from * math.sin(rad)
        points.append((x, y))

    # Agregar puntos desde el radio exterior
    for angle in range(angle_to, angle_from - 1, -1):
        rad = math.radians(angle)
        x = center[0] + radius_to * math.cos(rad)
        y = center[1] + radius_to * math.sin(rad)
        points.append((x, y))

    # Dibujar polígono
    pygame.draw.polygon(surface, color, points)

def draw_text(surface, position, text, color=(255, 255, 255)):
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(text, True, color)
    surface.blit(text, position)

