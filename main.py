import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pygame.locals import *
from sys import exit
import math
from pytmx.util_pygame import load_pygame

import python.classes as Class
import python.mouseStuff as mouse
import python.event as eventH
import python.functions.testdraw as test
import python.UI as UI


pygame.init()
screen = pygame.display.set_mode((1920,1080)) 
clock = pygame.time.Clock()
pygame.event.set_grab(True)
running = True
dt = 0
clicking = False
attacking = False
confirm = False
testdraw = False
candidates = []
#Map
tmx_data = load_pygame("assets/Map/Map Small.tmx")
layer = tmx_data.get_layer_by_name('Tile Layer 1')
"""
for x,y,surf in layer.tiles():
    print(x)
    print(y)
    print(surf)
"""

#bg_surf = pygame.transform.scale(pygame.image.load('assets/backgroundstandin.png').convert(),(1280,720))

Map = layer.data

#unitsetup
cameralist = Class.CameraGroup(Map)
structurelist = Class.CameraGroup(Map)
unitlist = Class.CameraGroup(Map)
resourcelist = Class.CameraGroup(Map)
workerlist = Class.CameraGroup(Map)
Base = Class.Base("base","Me",1000,100,0,Map,screen,300,300,workerlist,cameralist.zoom_scale)
Structure = Class.Structure("structure","Me",1000,100,0,Map,screen,450,450, unitlist, cameralist.zoom_scale)
Unit = Class.Unit("unit","Me",300,100,5,2,Map,screen,360,360, cameralist.zoom_scale,0,0)
Resource = Class.Resource("resource","Neutral",Map,screen,100,100,10, cameralist.zoom_scale)
Worker = Class.Worker("worker","Me",200,100,5,2,Map,screen,200,200, cameralist.zoom_scale,0,0)
Enemy = Class.Unit("unitE","Enemy",300,100,5,2,Map,screen,600,600, cameralist.zoom_scale,0,0)
structurelist.add(Base,Structure)
unitlist.add(Unit)
resourcelist.add(Resource)
workerlist.add(Worker)
unitlist.add(Enemy)
cameralist.add(structurelist,unitlist,resourcelist,workerlist)
mouse = mouse.Mouse()
UI = UI.UI()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
offset = cameralist.offset
internal_offset = cameralist.internal_offset

# main game loop
while running:
	# poll for events
    for event in pygame.event.get():
        mx, my = pygame.mouse.get_pos()  # gets mouse x,y coordinates
        location = [mx, my]
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEWHEEL:
            cameralist.zoom_scale += event.y * 0.03
        if event.type == pygame.MOUSEBUTTONDOWN:
            #all mouse inputs
            if event.button == 3:
                eventH.createpathHandler(offset,internal_offset,cameralist.zoom_scale,structurelist, unitlist, resourcelist, workerlist)
                if attacking is True:
                    eventH.attackHandler(cameralist.zoom_scale,structurelist, unitlist, resourcelist, workerlist,offset,internal_offset,screen)
                    testdraw = True

                
        if event.type == pygame.KEYDOWN:
            #all keyboard inputs
            if event.key == pygame.K_a:
                attacking = True
            #queue
            if event.key == pygame.K_b:
                for structures in structurelist:
                    if structures.selected:
                        if structures.Owner == "Me":
                            structures.startqueue()
            if event.key == pygame.K_c:
                for structures in structurelist:
                    if structures.selected:
                        if structures.Owner == "Me":
                            structures.stopqueue()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                attacking = False
        

    # fill the screen with a color to wipe away anything from last frame
    #screen.blit(bg_surf,(0,0))
    cameralist.custom_draw(Worker.character.sprite)
    workerlist.update(screen,resourcelist,structurelist,cameralist,offset, internal_offset, cameralist.zoom_scale,[structurelist, unitlist, resourcelist, workerlist])
    unitlist.update(screen,offset, internal_offset, cameralist.zoom_scale, cameralist, [structurelist, unitlist, resourcelist, workerlist])
    resourcelist.update(screen,offset, internal_offset, cameralist.zoom_scale, cameralist,[structurelist, unitlist, resourcelist, workerlist])
    structurelist.update(screen,dt,Map,offset, internal_offset, cameralist.zoom_scale, cameralist,[structurelist, unitlist, resourcelist, workerlist])



    for structure in structurelist:
        try:
            for worker in structure.wlist:
                workerlist.add(worker)
                cameralist.add(worker)

        except AttributeError:
            for unit in structure.ulist:
                unitlist.add(unit)
                cameralist.add(unit)
    
    UI.UIdraw(screen,[structurelist, unitlist, resourcelist, workerlist],dt)
    mouse.selection(screen,[structurelist, unitlist, resourcelist, workerlist],offset, internal_offset, cameralist.zoom_scale,cameralist)
    pygame.display.update()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()