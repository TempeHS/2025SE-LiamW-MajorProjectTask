import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import classes as Class
import mouseStuff as mouse


def createpathHandler(offset,internal_offset,zoom_scale,structurelist, unitlist, resourcelist, workerlist):
    for units in unitlist:
        if units.selected:
            if units.Owner == "Me":
                units.create_path(offset,internal_offset,zoom_scale)
    for structures in structurelist:
        if structures.selected:
            if structures.Owner == "Me":
                structures.create_path(offset,internal_offset,zoom_scale)
    for worker in workerlist:
        if worker.selected:
            if worker.Owner == "Me":
                worker.create_path(offset,internal_offset,zoom_scale)


def attackHandler(zoom_scale, structurelist, unitlist, resourcelist, workerlist,offset,internal_offset,screen):
    for units in unitlist:
        if units.selected:
            if units.Owner == "Me":
                units.attack(zoom_scale,[structurelist, unitlist, resourcelist, workerlist],offset, internal_offset, screen)
    for structures in structurelist:
        if structures.selected:
            if structures.Owner == "Me":
                structures.attack(zoom_scale,[structurelist, unitlist, resourcelist, workerlist],offset, internal_offset, screen)
    for worker in workerlist:
        if worker.selected:
            if worker.Owner == "Me":
                worker.attack(zoom_scale,[structurelist, unitlist, resourcelist, workerlist],offset, internal_offset, screen)