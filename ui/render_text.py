import pygame
from config import WHITE
def render_text(screen, font, text, pos,color=WHITE):
    font.render_to(screen, pos, text, color)

def render_text_center(screen, font, text, center_pos,color=WHITE,size=48):
    text_rect = font.get_rect(text, size=size)
    text_rect.center = center_pos
    font.render_to(screen, text_rect.topleft, text, color, size=48)