import pygame

def draw_gauge(screen, score, max_gauge=100):
    gauge_width = 400
    gauge_height = 30
    x = (1200 - gauge_width) // 2
    y = 700 - 50

    pygame.draw.rect(screen, (100, 100, 100), (x, y, gauge_width, gauge_height), 3)
    filled_width = int(min(score, max_gauge) / max_gauge * gauge_width)
    pygame.draw.rect(screen, (0, 200, 255), (x, y, filled_width, gauge_height))
