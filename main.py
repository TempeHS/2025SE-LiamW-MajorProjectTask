import pygame
from pygame.locals import *
from sys import exit

import classes as Class

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
clicking = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    for event in pygame.event.get():
        mx, my = pygame.mouse.get_pos()  # gets mouse x,y coordinates
        location = [mx, my]
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  
                clicking = True
                unit.mousemovement(player_pos,location,dt)
                unit.spawn(screen,player_pos)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    
    #add all your main line stuff here
    unit = Class.Unit("me",10,100,1,1)
    unit.spawn(screen,player_pos)
    unit.movement(player_pos,dt)

    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()