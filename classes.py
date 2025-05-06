import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Object(pygame.sprite.Sprite):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,empty_path,x,y,Type):
        super().__init__()
        #need to get rid of this and put it in individual classes
        if Type == 0:
            self.image = pygame.image.load('assets/playerstandin.png').convert_alpha()
            self.rect =  self.image.get_rect(center = (x,y))
            self.pos = self.rect.center
        elif Type == 1:
            self.image = pygame.image.load('assets/structurestandin.png').convert_alpha()
            self.rect =  self.image.get_rect(center = (x,y))
            self.pos = self.rect.center
        elif Type == 2:
            self.image = pygame.image.load('assets/structurestandinactive.png').convert_alpha()
            self.rect =  self.image.get_rect(center = (x,y))
            self.pos = self.rect.center
        elif Type == 3:
            self.image = pygame.image.load('assets/workerstandin.png').convert_alpha()
            self.rect =  self.image.get_rect(center = (x,y))
            self.pos = self.rect.center
        elif Type == 4:
            self.image = pygame.image.load('assets/resourcestandin.png').convert_alpha()
            self.rect =  self.image.get_rect(center = (x,y))
            self.pos = self.rect.center
        self.name = name
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
    def spawn(self,screen,location): #this is not used
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

class Pathfinder(Object):
    def __init__ (self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,Type):
        super().__init__(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y,Type)
        self.Map = Map
        self.grid = Grid(matrix = Map)
        self.select_surf = pygame.transform.scale(pygame.image.load('assets/mouse_cursor.png').convert_alpha(),(1280/32,1280/32))
        self.select_point = pygame.transform.scale(pygame.image.load('assets/path_point.png').convert_alpha(),(1280/32,1280/32))
        self.screen = screen
        self.path = []
        self.character = pygame.sprite.GroupSingle(Object(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y,Type))

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
            if not len(points) == 1:
                pygame.draw.lines(screen, '#4a4a4a',False, points, 5)
                tempx,tempy = points[len(points)-1]
                screen.blit(self.select_point,(tempx - 16,tempy-16))

    def update(self,screen):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.character.update()
        self.character.draw(screen)

class Structure(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Map,screen,x,y):
        super().__init__(name,Owner,HP,Energy,Range,0,Map,screen,x,y,1)
        self.queue = [0,0,0,0,0]
    
    def production(self,time,productionflag):
        n = 0
        for slot in productionflag:
            if slot == 1:
                self.queue[n] += time
                print(self.queue)
            n += 1
    
    def startqueue(self,proflag):
        for slot in proflag:
            if slot == 0:
                print(proflag.index(slot))
                proflag[proflag.index(slot)] = 1
                break
    def stopqueue(self,proflag):
        n = 4
        for slot in reversed(proflag):
            if slot == 1:
                self.queue[n] = 0
                proflag[n]  = 0
                break
            n -= 1
    def createunit(self,proflag,Map,screen):
        #placeholder build timer
        unitTime = 8
        if self.queue[0] >= unitTime:
            Queue = self.queue
            newqueue = [0,0,0,0,0]
            newflag = [0,0,0,0,0]
            for slot in Queue:
                num = Queue.index(slot) + 1
                newqueue[Queue.index(slot)] = Queue[num]
            Queue = newqueue
            for slot in proflag:
                num = proflag.index(slot) + 1
                newflag[proflag.index(slot)] = proflag[num]
            proflag = newflag
            Queue[4] = 0
            self.queue = newqueue
            Man = Unit("man","Me",100,100,0,2,Map,screen,300,300)
            return (Man, proflag)


    def update(self,screen,time,productionflag,Map):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.character.update()
        self.character.draw(screen)
        if 1 in productionflag:
            self.production(time,productionflag)
        Man = self.createunit(productionflag,Map,screen)
        if Man is not None:
            return Man[0], Man[1]

class Unit(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,Type):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,Type)
        self.Type = 0

class Worker(Unit):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,3)
        self.Speed = 1.5  # Workers are slower than units
    
    def draw_active_cell(self, screen):
        return super().draw_active_cell(screen)

class Resource(Pathfinder):
    def __init__(self,name,Owner,Map,screen,x,y,resources):
        super().__init__(name,Owner,0,0,0,0,Map,screen,x,y,4)
        self.resources = resources
