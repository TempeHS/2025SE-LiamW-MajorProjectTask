import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Mouse:
    def __init__(self):
        self.mouse_pos_start = (0, 0)
        self.clicking = False
        self.selection_rect = None
        self.flag = True

    def selection(self, screen):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if self.flag:
                self.mouse_pos_start = mouse_pos
                self.flag = False
            pygame.draw.rect(screen, (255, 0, 0), (self.mouse_pos_start[0], self.mouse_pos_start[1], mouse_pos[0]- self.mouse_pos_start[0]  , mouse_pos[1]- self.mouse_pos_start[1]), 2)
        else:
            self.flag = True