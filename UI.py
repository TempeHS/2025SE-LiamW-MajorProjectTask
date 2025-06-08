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


    def UIdraw(self,screen,colliders):
        screen.blit(self.UIbotBackground, (0, 0))
        i = 0
        for collidergroup in colliders:
            for collider in collidergroup:
                if collider.selected:
                    for character in collider.character:
                        UI_image = pygame.transform.scale(character.image, (40,40))
                        UI_border = pygame.transform.scale(self.CommandUIborder, (50,50))
                        screen.blit(UI_image, (500 + i,875))
                        screen.blit(UI_border, (495 + i, 870))
                        
                        screen.blit(self.CommandUIborder, (1465, 775))
                        i += 50
