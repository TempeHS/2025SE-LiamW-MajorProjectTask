import pygame
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

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
        self.path = []

    def gridIntoInt(self,point):
        x = point.x
        y = point.y
        point = [x,y]
        return point


    def draw_active_cell(self,screen):
        mouse_pos = pygame.mouse.get_pos()
        row = math.floor(mouse_pos[1] / 32)
        col = math.floor(mouse_pos[0] / 32)
        current_cell_value = self.Map[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col * 32, row * 32),(32,32))
            screen.blit(self.select_surf, rect)

    def create_path(self):
        startx,starty = [1,1]
        start = self.grid.node(startx,starty)
        mouse_pos = pygame.mouse.get_pos()  # gets mouse x,y coordinates
        endx,endy = math.floor(mouse_pos[0] / 32), math.floor(mouse_pos[1] / 32)
        end = self.grid.node(endx,endy)

        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start,end,self.grid)
        self.grid.cleanup()

    def draw_path(self,screen):
        if self.path:
            points = []
            for point in self.path:
                point = self.gridIntoInt(point)
                x = (point[0] *32) + 16
                y = (point[1] *32) + 16
                points.append((x, y))
                pygame.draw.circle(screen,'#4a4a4a',(x,y),2)
            pygame.draw.lines(screen, '#4a4a4a',False, points, 5)

    def update(self,screen):
        self.draw_active_cell(screen)
        self.draw_path(screen)