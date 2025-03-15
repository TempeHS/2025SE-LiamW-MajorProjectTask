import pygame
import math
from pathfinding.core.grid import Grid 

class Unit:
    def __init__(self,Owner,HP,Energy,Range,Speed):
        self.Owner = Owner
        self.HP = HP
        self.Energy = Energy
        self.Range = Range
        self.Speed = Speed
    
    @classmethod
    def spawn(self,screen,location):
        pygame.draw.circle(screen, "red", location, 30)
    def movement(self,location,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            location.y -= 300 * dt
        if keys[pygame.K_s]:
            location.y += 300 * dt
        if keys[pygame.K_a]:
            location.x -= 300 * dt
        if keys[pygame.K_d]:
            location.x += 300 * dt
    def mousemovement(self,location,mouselocation,dt):
        if mouselocation == location:
            pass 
        else:
            print(mouselocation)
            distanceY = mouselocation[1] - location.y
            distanceX = mouselocation[0] - location.x
            #unitVectorY = distanceY / abs(distanceY)
            #unitVectorX = distanceX / abs(distanceX)
            gradient = distanceY/distanceX
            if distanceX > 0:
                location.x += 300 * dt
            else:
                location.x -= 300 * dt
            if location.y == mouselocation[1]:
                pass
            else:
                location.y = gradient * location.x
            print(location)
            print(gradient)
    #@property uncomment when you have properties later

class Pathfinder:
    def __init__ (self,Map,screen):
        self.Map = Map
        self.grid = Grid(matrix = Map)
        self.select_surf = pygame.transform.scale(pygame.image.load('assets/mouse_cursor.png').convert_alpha(),(1280/32,1280/32))
        self.screen = screen
    def draw_active_cell(self,screen):
        mouse_pos = pygame.mouse.get_pos()  # gets mouse x,y coordinates
        row = math.floor(mouse_pos[1] / 32)
        col = math.floor(mouse_pos[0] / 32)
        print(f"{row},{col}")
        #current_cell_value
        rect = pygame.Rect((col * 32, row * 32),(32,32))
        screen.blit(self.select_surf, rect)
    def update(self,screen):
        self.draw_active_cell(screen)