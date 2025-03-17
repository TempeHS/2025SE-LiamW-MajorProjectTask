import pygame
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Unit(pygame.sprite.Sprite):
    def __init__(self,Owner,HP,Energy,Range,Speed,empty_path):
        super().__init__()
        self.image = pygame.image.load('assets/playerstandin.png').convert_alpha()
        self.rect =  self.image.get_rect(center = (60,60))
        self.pos = self.rect.center
        self.Owner = Owner
        self.HP = HP
        self.Energy = Energy
        self.Range = Range
        self.Speed = Speed #you need to set it 
        self.path=[]
        self.collision_rects=[]
        self.direction = pygame.math.Vector2(0,0)
        self.empty_path = empty_path
    
    @classmethod
    def spawn(self,screen,location):
        pygame.draw.circle(screen, "red", location, 30)
    
    def get_coord(self):
        col = math.floor(self.rect.centerx / 32)
        row = math.floor(self.rect.centery / 32)
        return (col,row)
    
    def set_path(self,path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x=(point.x * 32) + 16
                y=(point.y * 32) + 16
                rect = pygame.Rect((x-2,y-2),(4,4)) # change this later this based on each grid size so try center it later
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            print(self.direction)
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []

    def check_collisions(self): 
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path()

    def update(self):
        self.pos += self.direction * self.Speed
        self.check_collisions()
        self.rect.center = self.pos

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
        self.character = pygame.sprite.GroupSingle(Unit("me",10,10,10,0.6,self.empty_path))

    def empty_path(self):
        self.path = []

    def gridIntoInt(self,point):
        x = point.x
        y = point.y
        point = [x,y]
        return point


    def draw_active_cell(self,screen):
        notin = True
        mouse_pos = pygame.mouse.get_pos()
        row = math.floor(mouse_pos[1] / 32)
        col = math.floor(mouse_pos[0] / 32)
        while notin is True:
            try:
                current_cell_value = self.Map[row][col]
                notin = False
            except IndexError:
                #make this better later
                if row < 0:
                    row = 0
                if col < 0:
                    col = 0
                if col > 32:
                    col = 32
                if row > 32:
                    row = 32

        if current_cell_value == 1:
            rect = pygame.Rect((col * 32, row * 32),(32,32))
            screen.blit(self.select_surf, rect)

    def create_path(self):
        startx,starty = self.character.sprite.get_coord()
        start = self.grid.node(startx,starty)
        mouse_pos = pygame.mouse.get_pos()  # gets mouse x,y coordinates
        endx,endy = math.floor(mouse_pos[0] / 32), math.floor(mouse_pos[1] / 32)
        end = self.grid.node(endx,endy)

        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start,end,self.grid)
        self.grid.cleanup()
        self.character.sprite.set_path(self.path)

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
        self.character.update()
        self.character.draw(screen)