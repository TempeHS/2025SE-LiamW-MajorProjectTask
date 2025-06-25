import pygame
from pytmx.util_pygame import load_pygame

class Map(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.pos = pos
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)