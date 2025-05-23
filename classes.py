import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Object(pygame.sprite.Sprite):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,empty_path,x,y):
        super().__init__()
        self.name = name
        self.Owner = Owner
        self.HP = HP
        self.Energy = Energy
        self.Range = Range
        self.Speed = Speed #you need to set it 
        self.pos = (100,100)
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
            #print(self.direction)
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

    def update(self,screen):
        self.pos += self.direction * self.Speed
        self.check_collisions()
        self.rect.center = self.pos
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

#fix later currently has no negative effect 
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = pygame.image.load('assets/backgroundstandin.png').convert()
        self.ground_rect = self.ground_surf.get_rect()
        #camera offset
        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        self.display_surface.blit(self.ground_surf, self.ground_rect)
        # Collect all characters from all sprites
        all_characters = []
        for sprites in self.sprites():
            for character in sprites.character:
                all_characters.append(character)
        # Sort by y (centery)
        all_characters.sort(key=lambda c: c.rect.centery)
        # Draw in order
        for character in all_characters:
            self.display_surface.blit(character.image, character.rect)

class Pathfinder(Object):
    def __init__ (self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y):
        super().__init__(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y)
        self.Map = Map
        self.grid = Grid(matrix = Map)
        self.select_surf = pygame.transform.scale(pygame.image.load('assets/mouse_cursor.png').convert_alpha(),(1280/32,1280/32))
        self.select_point = pygame.transform.scale(pygame.image.load('assets/path_point.png').convert_alpha(),(1280/32,1280/32))
        self.screen = screen
        self.path = []
        self.character = pygame.sprite.GroupSingle(Object(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y))

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
        self.character.update(screen)
        #self.character.draw(screen)

class Structure(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Map,screen,x,y,unitlist):
        super().__init__(name,Owner,HP,Energy,Range,0,Map,screen,x,y)
        for character in self.character:
            character.image = pygame.image.load('assets/structurestandin.png').convert_alpha()
            character.rect =  character.image.get_rect(center = (x,y))
            character.pos = character.rect.center
        self.ulist = unitlist
        self.queue = [0,0,0,0,0]
        self.proflag = [0,0,0,0,0]
    
    def production(self,time):
        productionflag = self.proflag
        for character in self.character:
            character.image = pygame.image.load('assets/structurestandinactive.png').convert_alpha()
        n = 0
        for slot in productionflag:
            if slot == 1:
                self.queue[n] += time
                print(self.queue)
            n += 1
    
    def startqueue(self):
        proflag = self.proflag
        for slot in proflag:
            if slot == 0:
                print(proflag.index(slot))
                proflag[proflag.index(slot)] = 1
                break
    def stopqueue(self):
        proflag = self.proflag
        n = 4
        for slot in reversed(proflag):
            if slot == 1:
                self.queue[n] = 0
                proflag[n]  = 0
                break
            n -= 1
    def createunit(self,Map,screen):
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
            for slot in self.proflag:
                num = self.proflag.index(slot) + 1
                newflag[self.proflag.index(slot)] = self.proflag[num]
            self.proflag = newflag
            Queue[4] = 0
            self.queue = newqueue
            Man = Unit("man","Me",100,100,0,2,Map,screen,600,600)
            for character in self.character:
                character.image = pygame.image.load('assets/structurestandin.png').convert_alpha()
            self.ulist.add(Man)


    def update(self,screen,time,Map):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.character.update(screen)
        #self.character.draw(screen)
        productionflag = self.proflag
        if 1 in productionflag:
            self.production(time)
        self.createunit(Map,screen)

class Unit(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y)
        for character in self.character:
            character.image = pygame.image.load('assets/playerstandin.png').convert_alpha()
            character.rect =  character.image.get_rect(center = (x,y))
            character.pos = character.rect.center
        self.Type = 0

class Worker(Unit):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y)
        for character in self.character:
            character.image = pygame.image.load('assets/workerstandin.png').convert_alpha()
            character.rect = character.image.get_rect(center = (x,y))
            character.pos = character.rect.center
        self.Speed = 1.5  # Workers are slower than units
        self.mining_progress = 0
        self.has_mined = False
    
    def draw_active_cell(self, screen):
        return super().draw_active_cell(screen)
    
    def resourcecollectcol(self,resourcelist):
        if not self.has_mined:
            for resource in resourcelist:
                #print(f"Worker rect: {self.rect}, Resource rect: {resource.rect}")
                for rcharacter in resource.character:
                    for character in self.character:
                        if character.rect.colliderect(rcharacter.rect):
                            #print("Collision with resource!")
                            #need to rework logic for later to be if the user clicks on the resource then they stop at the resource which will stop locking the worker class to the resource
                            character.direction = pygame.math.Vector2(0,0)
                            self.mining()
                            break
                    else:
                        self.mining_progress = 0

    def baseputcol(self,structurelist):
        if self.has_mined:
            for structure in structurelist:
                #print(f"Worker rect: {self.rect}, Resource rect: {resource.rect}")
                for rcharacter in structure.character:
                    for character in self.character:
                        if character.rect.colliderect(rcharacter.rect):
                            print("Collision with base!")
                            character.direction = pygame.math.Vector2(0,0)
                            self.putting()
                            structure.resource += 5
                            print(structure.resource)
                            #add updating resource counter in base here

                            break
                    else:
                        self.mining_progress = 0
    
    def putting(self):
        # Handle resource collection here
        print("Resource deposited!")
        for character in self.character:
            pygame.math.Vector2(-character.direction)
            character.image = pygame.image.load('assets/workerstandin.png').convert_alpha()
        self.has_mined = False

    def mining(self):
        self.mining_progress += 1
        if self.mining_progress == 600:
            # Handle resource collection here
            print("Resource collected!")
            self.mining_progress = 0
            for character in self.character:
                pygame.math.Vector2(-character.direction)
                character.image = pygame.image.load('assets/workerwithRstandin.png').convert_alpha()
            self.has_mined = True
            # You can also remove the resource from the game or update its state

    def update(self,screen,resourcelist,structurelist):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.character.update(screen)
        self.resourcecollectcol(resourcelist)
        self.baseputcol(structurelist)
        #self.character.draw(screen)
        #print(f"Updated rect: {self.rect.center}, Position: {self.pos}")

class Resource(Pathfinder):
    def __init__(self,name,Owner,Map,screen,x,y,resources):
        super().__init__(name,Owner,0,0,0,0,Map,screen,x,y)
        for character in self.character:
            character.image = pygame.image.load('assets/resourcestandin.png').convert_alpha()
            character.rect =  character.image.get_rect(center = (x,y))
            character.pos = character.rect.center
        self.resources = resources

class Base(Structure):
    def __init__(self,name,Owner,HP,Energy,Range,Map,screen,x,y,workerlist):
        super().__init__(name,Owner,HP,Energy,Range,Map,screen,x,y,0)
        for character in self.character:
            character.image = pygame.image.load('assets/structurestandin.png').convert_alpha()
            character.rect =  character.image.get_rect(center = (x,y))
            character.pos = character.rect.center
        self.wlist = workerlist
        self.resource = 0
        self.queue = [0,0,0,0,0]
        self.proflag = [0,0,0,0,0]

    def createunit(self,Map,screen):
        #placeholder build timer
        unitTime = 5
        if self.queue[0] >= unitTime:
            Queue = self.queue
            newqueue = [0,0,0,0,0]
            newflag = [0,0,0,0,0]
            for slot in Queue:
                num = Queue.index(slot) + 1
                newqueue[Queue.index(slot)] = Queue[num]
            Queue = newqueue
            for slot in self.proflag:
                num = self.proflag.index(slot) + 1
                newflag[self.proflag.index(slot)] = self.proflag[num]
            self.proflag = newflag
            Queue[4] = 0
            self.queue = newqueue
            Man = Worker("man1","Me",100,100,0,2,Map,screen,300,300)
            for character in self.character:
                character.image = pygame.image.load('assets/structurestandin.png').convert_alpha()
            self.wlist.add(Man)
