import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import classes as Class
import mouseStuff as mouse


class UI():
    def __init__(self):
        UIbotBackground = pygame.image.load("assets/UI/Game Overlay Bottom Background.png").convert_alpha()
        self.UIbotBackground = pygame.transform.scale(UIbotBackground, (1920, 1080))
        CommandUIborder = pygame.image.load("assets/UI/Command UI border icon.png").convert_alpha()
        self.CommandUIborder = pygame.transform.scale(CommandUIborder, (80,80))


    def UIdraw(self,screen):
        screen.blit(self.UIbotBackground, (0, 0))
        screen.blit(self.CommandUIborder, (1465, 775))
