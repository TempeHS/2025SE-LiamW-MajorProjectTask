import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


def spriteSet(self,Image,x,y):
    for character in self.character:
        if self.Owner != "Me":
            before, after = Image.split(".")
            Image = f"{before}E.{after}"
        image = pygame.image.load(Image).convert_alpha()
        bounding_rect = image.get_bounding_rect()
        cropped_image = image.subsurface(bounding_rect).copy()
        character.image = cropped_image
        character.rect = cropped_image.get_rect(center=(x, y))
        character.pos = character.rect.center

def spriteSetUpdate(self,Image):
    for character in self.character:
        if self.Owner != "Me":
            before, after = Image.split(".")
            Image = f"{before}E.{after}"
        image = pygame.image.load(Image).convert_alpha()
        bounding_rect = image.get_bounding_rect()
        cropped_image = image.subsurface(bounding_rect).copy()
        character.image = cropped_image

def spriteInheritpath(self, product):
    product.path = self.path[:]  # Copy the path
    for character in product.character:
        character.set_path(product.path)  # Set path for internal Object