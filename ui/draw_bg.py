import pygame

def draw_bg(screen, bg, scroll, y):
    x = -scroll % bg.get_width()
    screen.blit(bg, (x - bg.get_width(), y))
    screen.blit(bg, (x, y))