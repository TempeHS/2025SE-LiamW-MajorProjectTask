import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import unitsetup as setup
import production as pro
import testdraw as test

class Object(pygame.sprite.Sprite):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,empty_path,x,y):
        super().__init__()
        self.name = name
        self.Owner = Owner
        self.HP = HP
        self.Energy = Energy
        self.Range = Range
        self.Speed = Speed #you need to set it 
        self.pos = pygame.math.Vector2(x, y)
        self.path=[]
        self.collision_rects=[]
        self.direction = pygame.math.Vector2(0,0)
        self.empty_path = empty_path
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.selected = False
    
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
            delta = end - start
            if delta.length() > 0:
                self.direction = delta.normalize()
            else:
                self.direction = pygame.math.Vector2(0, 0)
                # Optionally remove this collision rect and try the next
                del self.collision_rects[0]
                self.get_direction()
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

class CameraGroup(pygame.sprite.Group):
    def __init__(self,Map):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = pygame.image.load('assets/backgroundstandin.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
        self.Map = Map
        #camera offset
        self.offset = pygame.math.Vector2()
        
        #for centered camera
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.keyboard_speed = 5
        self.mouse_speed = 5

        #camera zoom
        self.zoom_scale = 1.0 
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, flags=pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_width, self.half_height))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2(0, 0)
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_height

        self.camera_borders = {'left': 50, 'right': 50, 'top': 50, 'bottom': 50}
        l = self.camera_borders["left"]
        t = self.camera_borders["top"]
        w = self.display_surface.get_size()[0] - (self.camera_borders["left"] + self.camera_borders["right"])
        h = self.display_surface.get_size()[1] - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(l,t,w,h)
    
    def center_target_camera(self, target): 
        self.offset.x = -(target.rect.centerx - self.half_width)
        self.offset.y = -(target.rect.centery - self.half_height)

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = -(self.camera_rect.left - self.camera_borders["left"])
        self.offset.y = -(self.camera_rect.top - self.camera_borders["top"])

    def keyboard_camera(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.camera_rect.x -= 5
        if keys[pygame.K_RIGHT]: self.camera_rect.x += 5
        if keys[pygame.K_UP]: self.camera_rect.y -= 5  
        if keys[pygame.K_DOWN]: self.camera_rect.y += 5
        self.offset.x = -(self.camera_rect.left - self.camera_borders["left"])
        self.offset.y = -(self.camera_rect.top - self.camera_borders["top"])

    def mouse_camera(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2(0, 0)
        left_border = self.camera_borders["left"]
        right_border = self.display_surface.get_size()[0] - self.camera_borders["right"]
        top_border = self.camera_borders["top"]
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders["bottom"]

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos(left_border, mouse.y)
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos(right_border, mouse.y)
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos(left_border, top_border)
            elif mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos(right_border, top_border)
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos(left_border, bottom_border)
            elif mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos(right_border, bottom_border)

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos(mouse.x, top_border)
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos(mouse.x, bottom_border)
        
        self.offset += -mouse_offset_vector * self.mouse_speed

    def zoom_camera(self):
        ##if keys[pygame.MOUSEWHEEL]: 
            #self.zoom_scale += 0.1
        #if keys[pygame.MOUSEWHEEL]: 
            #self.zoom_scale -= 0.1
        pass

    def draw_grid(self, surface, ground_offset):
        # Draw grid lines or cells
        for row in range(len(self.Map)):
            for col in range(len(self.Map[0])):
                cell_x = ground_offset.x + col * 32
                cell_y = ground_offset.y + row * 32
                rect = pygame.Rect(cell_x, cell_y, 32, 32)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)  # Draw grid cell outline

    def custom_draw(self,player):
        # dead zone camera
        #self.box_target_camera(player)
        
        #self.keyboard_camera()
        self.mouse_camera()
        self.internal_surf.fill(("#408ff7"))  # Fill the internal surface with a color

        #self.internal_surf.blit(self.ground_surf, (0, 600))
        #for centred around player camera will be used for control groups
            #self.center_target_camera(player)

        ground_offset = self.ground_rect.topleft + self.offset - self.internal_offset
        self.internal_surf.blit(self.ground_surf, ground_offset)
        self.draw_grid(self.internal_surf, ground_offset)
        # Collect all characters from all sprites
        all_characters = []
        for sprites in self.sprites():
            for character in sprites.character:
                all_characters.append(character)
        # Sort by y (centery)
        all_characters.sort(key=lambda c: c.rect.centery)
        # Draw in order
        for character in all_characters:
            offset_pos = character.rect.topleft + self.offset - self.internal_offset
            pygame.draw.rect(self.internal_surf, (255, 0, 0), character.rect.move(self.offset - self.internal_offset), 2)
            self.internal_surf.blit(character.image, offset_pos)
        
        #add if statement to limit size
        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_width, self.half_height))
        self.display_surface.blit(scaled_surf, scaled_rect)
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.camera_rect, 5)

class Pathfinder(Object):
    def __init__ (self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,zoom_scale):
        super().__init__(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y)
        self.Map = Map
        self.grid = Grid(matrix = Map)
        self.select_surf = pygame.transform.scale(pygame.image.load('assets/mouse_cursor.png').convert_alpha(),(1280/(32*zoom_scale),1280/(32*zoom_scale)))
        self.select_point = pygame.transform.scale(pygame.image.load('assets/path_point.png').convert_alpha(),(1280/(32*zoom_scale),1280/(32*zoom_scale)))
        self.screen = screen
        self.path = []
        self.flag = False
        self.collision_frames = 0
        self.last_collision_pos = None
        self.last_collision_pos2 = None
        self.character = pygame.sprite.GroupSingle(Object(name,Owner,HP,Energy,Range,Speed,self.empty_path,x,y))

    def empty_path(self):
        self.path = []

    def gridIntoInt(self,point):
        x = point.x
        y = point.y
        point = [x,y]
        return point

    def screen_to_internal(self,mouse_pos, internal_surf_size, display_size, zoom_scale):
        # Find the top-left of the scaled internal_surf on the display
        scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
        offset_x = (display_size[0] - scaled_size[0]) // 2
        offset_y = (display_size[1] - scaled_size[1]) // 2
        # Convert mouse position to internal_surf coordinates
        internal_x = (mouse_pos[0] - offset_x) / zoom_scale
        internal_y = (mouse_pos[1] - offset_y) / zoom_scale
        return internal_x, internal_y

    def draw_active_cell(self, screen, offset, internal_offset, zoom_scale):
        mouse_pos = pygame.mouse.get_pos()
        display_size = pygame.display.get_surface().get_size()
        internal_surf_size = screen.get_size()
        scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
        offset_x = (display_size[0] - scaled_size[0]) // 2
        offset_y = (display_size[1] - scaled_size[1]) // 2

        # Convert mouse to internal surface coordinates
        internal_x = (mouse_pos[0] - offset_x) / zoom_scale
        internal_y = (mouse_pos[1] - offset_y) / zoom_scale

        # Convert to world coordinates
        world_x = internal_x + offset.x - internal_offset.x
        world_y = internal_y + offset.y - internal_offset.y

        # Get grid cell
        col = int(world_x // 32)
        row = int(world_y // 32)

        # Clamp to valid range
        row = max(0, min(row, len(self.Map) - 1))
        col = max(0, min(col, len(self.Map[0]) - 1))

        current_cell_value = self.Map[row][col]
        #print(f"row={row}, col={col}, value={current_cell_value}")

        if current_cell_value == 1:
            cell_size = 32 * zoom_scale
            # Use the same math as draw_grid for the top-left of the cell
            cell_world_x = col * 32
            cell_world_y = row * 32
            cell_internal_x = cell_world_x - offset.x + internal_offset.x
            cell_internal_y = cell_world_y - offset.y + internal_offset.y
            cell_screen_x = cell_internal_x * zoom_scale + offset_x
            cell_screen_y = cell_internal_y * zoom_scale + offset_y
            rect = pygame.Rect((cell_screen_x, cell_screen_y), (cell_size, cell_size))
            screen.blit(pygame.transform.scale(self.select_surf, (int(cell_size), int(cell_size))), rect)

    def create_path(self, offset, internal_offset, zoom_scale):
        mouse_pos = pygame.mouse.get_pos()
        # Calculate scaled cell size
        cell_size = 32 * zoom_scale

        # Use the same math as draw_active_cell for mouse-to-grid
        display_size = pygame.display.get_surface().get_size()
        internal_surf_size = self.screen.get_size()
        scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
        offset_x = (display_size[0] - scaled_size[0]) // 2
        offset_y = (display_size[1] - scaled_size[1]) // 2
        internal_x = (mouse_pos[0] - offset_x) / zoom_scale
        internal_y = (mouse_pos[1] - offset_y) / zoom_scale
        world_x = internal_x - offset.x + internal_offset.x + (internal_offset.x)
        world_y = internal_y - offset.y + internal_offset.y + (internal_offset.y)

        endx = math.floor((world_x) / 32)
        endy = math.floor((world_y) / 32)

        startx, starty = self.character.sprite.get_coord()
        start = self.grid.node(startx, starty)
        end = self.grid.node(endx, endy)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.character.sprite.set_path(self.path)

    def draw_path(self, screen, offset, internal_offset, zoom_scale):
        if self.path:
            cell_size = 32 * zoom_scale
            display_size = pygame.display.get_surface().get_size()
            internal_surf_size = screen.get_size()
            scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
            offset_x = (display_size[0] - scaled_size[0]) // 2
            offset_y = (display_size[1] - scaled_size[1]) // 2

            points = []
            for point in self.path:
                point = self.gridIntoInt(point)
                x = (point[0] * 32 + offset.x - internal_offset.x) * zoom_scale + offset_x + cell_size - (internal_offset.x + 16)* zoom_scale
                y = (point[1] * 32 + offset.y - internal_offset.y) * zoom_scale + offset_y + cell_size - (internal_offset.y + 16)* zoom_scale
                points.append((x, y))
                pygame.draw.circle(screen, '#4a4a4a', (int(x), int(y)), max(2, int(2 * zoom_scale)))
            if len(points) > 1:
                pygame.draw.lines(screen, '#4a4a4a', False, points, max(1, int(5 * zoom_scale)))
                tempx, tempy = points[-1]
                scaled_point = pygame.transform.scale(self.select_point, (int(cell_size), int(cell_size)))
                screen.blit(scaled_point, (tempx - cell_size / 2, tempy - cell_size / 2))

    def collision(self, cameralist, colliders):
        for character in self.character:
            collided = False
            grid_size = 32
            for cam in cameralist:
                if character.name is not cam.name:
                    for character2 in cam.character:
                        if character.rect.colliderect(character2.rect):
                            collided = True
                            # Convert character.pos to Vector2 if it's not already
                            character.pos = pygame.math.Vector2(character.pos)
                            #print(f"character: {character}, character.pos: {character.pos}, type: {type(character.pos)}")
                            #print(f"cam: {cam}, cam.pos: {getattr(cam, 'pos', None)}, type: {type(getattr(cam, 'pos', None))}")
                            # Calculate the overlap rectangle
                            overlap = character.rect.clip(character2.rect)
                            """
                            if overlap.width < overlap.height:
                                # Move in x direction
                                if character.rect.centerx < cam.rect.centerx:
                                    character.pos.x -= overlap.width * self.Speed
                                else:
                                    character.pos.x += overlap.width * self.Speed
                            else:
                                # Move in y direction
                                if character.rect.centery < cam.rect.centery:
                                    character.pos.y -= overlap.height * self.Speed
                                else:
                                    character.pos.y += overlap.height * self.Speed
                            character.rect.center = character.pos
                            """
                            
                            # this is the get unstuck code for special cases if you want it to be every second time an object collides with the same object then you gotta change it lol
                            
                            collision_point = (int(character.pos.x // grid_size), int(character.pos.y // grid_size))
                            print(f"Collision at {collision_point} for {character.name}")
                            if self.last_collision_pos == collision_point:
                                self.collision_frames += 1
                            elif self.last_collision_pos2 == collision_point:   
                                self.collision_frames += 1
                            else:
                                if self.last_collision_pos is not None:
                                    self.last_collision_pos2 = collision_point
                                else:
                                    self.collision_frames = 1
                                    self.last_collision_pos = collision_point
                                

                            if self.collision_frames > 10:  # Threshold (10 frames)
                                character.path = []
                                character.collision_rects = []
                                character.get_direction()
                                self.collision_frames = 0
                                self.last_collision_pos = None
                            else:
                                #if self.flag == True:
                                if self.Speed > 0:
                                    self.repositionGridCenter(colliders)
                                    """
                                    self.flag = False
                                else:
                                    self.flag = True
                                """
                            break
                    if collided:
                        break

            if not collided:
                if self.last_collision_pos is not None:
                    current_grid = (int(character.pos.x // grid_size), int(character.pos.y // grid_size))
                    if current_grid != self.last_collision_pos:
                        self.collision_frames = 0
                        self.last_collision_pos = None

    def repositionGridCenter(self, colliders, grid_size=32, search_radius=1):
        """
        Move the sprite's character to the nearest grid center (within search_radius) that does not collide with any collider,
        but do NOT clear the path—allow the unit to continue following its path.
        """
        for character in self.character:
            current_grid_x = int(character.pos.x // grid_size)
            current_grid_y = int(character.pos.y // grid_size)
            candidate_centers = []

            # Generate candidate grid centers within the search radius
            for dx in range(-search_radius, search_radius + 1):
                for dy in range(-search_radius, search_radius + 1):
                    grid_x = current_grid_x + dx
                    grid_y = current_grid_y + dy
                    center = pygame.math.Vector2(grid_x * grid_size + grid_size // 2, grid_y * grid_size + grid_size // 2)
                    dist = (center - character.pos).length()
                    candidate_centers.append((dist, center))

            # Sort by distance to current position
            candidate_centers.sort(key=lambda tup: tup[0])

            # Try each candidate
            for dist, center in candidate_centers:
                test_rect = character.rect.copy()
                test_rect.center = center
                collision = False
                for collidergroup in colliders:
                    for collider in collidergroup:
                        if collider is self:
                            continue
                        for other in collider.character:
                            if test_rect.colliderect(other.rect):
                                collision = True
                                break
                        if collision:
                            break
                if not collision:
                    # Move to this grid center, but do NOT clear the path
                    character.pos = center
                    character.rect.center = character.pos
                    # Recalculate direction to next path point
                    character.get_direction()
                    return True  # Successfully repositioned

        # If no free grid found, do nothing
        return False

    def attack(self, zoom_scale, colliders,offset, internal_offset,screen):
        for character2 in self.character:
            current_grid_x = int(character2.pos.x)
            current_grid_y = int(character2.pos.y)
            scale_factor = 32 * zoom_scale
            candidate_centers = []

            # change this to find nearest enemy in range centre  
            for collidergroup in colliders:
                for collide in collidergroup:
                    for character3 in collide.character:
                        center = character3.pos
                        dist = (center - character2.pos).length()
                        search_radius = collide.Range * scale_factor
                        if dist < search_radius: #make sure to scale to zoom factor
                            if collide.Owner != self.Owner: #need to do this for other functions that are similar
                                candidate_centers.append(character3)

            # Sort by distance to current position
            candidate_centers.sort(reverse=True,key=lambda c: (c.pos - character2.pos).length())


            if candidate_centers:
                #put in a way to stop the unit when they are attacking
                if candidate_centers[0] != character2:
                    candidate_centers[0].HP -= 5
                    print(f"{candidate_centers[0].name} is down to {candidate_centers[0].HP} HP")

    def update(self,screen,offset,internal_offset,zoom_scale,cameralist, colliders):
        self.draw_active_cell(screen,offset,internal_offset,zoom_scale)
        self.draw_path(screen,offset,internal_offset,zoom_scale)
        self.collision(cameralist,colliders)
        self.character.update(screen)

        #self.character.draw(screen)

class Structure(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Map,screen,x,y,unitlist, zoom_scale):
        super().__init__(name,Owner,HP,Energy,Range,0,Map,screen,x,y,zoom_scale)
        setup.spriteSet(self, 'assets/structurestandin.png', x, y)
        self.ulist = unitlist
        self.queue = [0,0,0,0,0]
        self.proflag = [0,0,0,0,0]
    
    def production(self,time):
        productionflag = self.proflag
        setup.spriteSetUpdate(self, 'assets/structurestandinactive.png')
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
    def createunit(self,Map,screen,zoom_scale):
        #placeholder build timer
        for character in self.character:
            unitTime = 8
            if pro.produce(self,unitTime):
                Man = Unit("man",self.Owner,100,100,0,2,Map,screen,character.pos.x + 50,character.pos.y + 50,zoom_scale)
                setup.spriteSetUpdate(self, 'assets/structurestandin.png')
                self.ulist.add(Man)


    def update(self,screen,time,Map,offset,internal_offset,zoom_scale,cameralist,colliders):
        self.draw_active_cell(screen,offset,internal_offset,zoom_scale)
        self.draw_path(screen,offset,internal_offset,zoom_scale)
        self.collision(cameralist,colliders)
        self.character.update(screen)
        #self.character.draw(screen)
        productionflag = self.proflag
        if 1 in productionflag:
            self.production(time)
        self.createunit(Map,screen, zoom_scale)

class Unit(Pathfinder):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,zoom_scale):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,zoom_scale)
        setup.spriteSet(self, 'assets/playerstandin.png', x, y)
        self.Type = 0

class Worker(Unit):
    def __init__(self,name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,zoom_scale):
        super().__init__(name,Owner,HP,Energy,Range,Speed,Map,screen,x,y,zoom_scale)
        setup.spriteSet(self, 'assets/workerstandin.png', x, y)
        self.Speed = 1.5  # Workers are slower than units
        self.mining_progress = 0
        self.has_mined = False
    
    def resourcecollectcol(self,resourcelist,cameralist,colliders):
        Rcollision = False
        if not self.has_mined:
            for resource in resourcelist:
                #print(f"Worker rect: {self.rect}, Resource rect: {resource.rect}")
                for rcharacter in resource.character:
                    for character in self.character:
                        if character.rect.colliderect(rcharacter.rect):
                            Rcollision = True
                            print("Collision with resource!")
                            #need to rework logic for later to be if the user clicks on the resource then they stop at the resource which will stop locking the worker class to the resource
                            character.direction = pygame.math.Vector2(0,0)
                            self.mining()
                            break
                    else:
                        self.mining_progress = 0

        if not Rcollision:
            self.collision(cameralist,colliders)

    def baseputcol(self,structurelist,cameralist,colliders):
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
        
        #else:
            #self.collision(cameralist,colliders)
    
    def putting(self):
        # Handle resource collection here
        print("Resource deposited!")
        for character in self.character:
            pygame.math.Vector2(-character.direction)
            setup.spriteSetUpdate(self, 'assets/workerstandin.png')
        self.has_mined = False

    def mining(self):
        self.mining_progress += 1
        if self.mining_progress == 600:
            # Handle resource collection here
            print("Resource collected!")
            self.mining_progress = 0
            setup.spriteSetUpdate(self, 'assets/workerwithRstandin.png')
            self.has_mined = True
            # You can also remove the resource from the game or update its state

    def update(self,screen,resourcelist,structurelist,cameralist,offset,internal_offset,zoom_scale,colliders):
        self.draw_active_cell(screen,offset,internal_offset,zoom_scale)
        self.draw_path(screen,offset,internal_offset,zoom_scale)
        self.baseputcol(structurelist,cameralist,colliders)
        self.resourcecollectcol(resourcelist,cameralist,colliders)
        self.character.update(screen)

        #self.character.draw(screen)
        #print(f"Updated rect: {self.rect.center}, Position: {self.pos}")

class Resource(Pathfinder):
    def __init__(self,name,Owner,Map,screen,x,y,resources,zoom_scale):
        super().__init__(name,Owner,0,0,0,0,Map,screen,x,y,zoom_scale)
        setup.spriteSet(self, 'assets/resourcestandin.png', x, y)
        self.resources = resources

class Base(Structure):
    def __init__(self,name,Owner,HP,Energy,Range,Map,screen,x,y,workerlist,zoom_scale):
        super().__init__(name,Owner,HP,Energy,Range,Map,screen,x,y,0,zoom_scale)
        setup.spriteSet(self, 'assets/structurestandin.png',x,y)
        self.wlist = workerlist
        self.resource = 0
        self.queue = [0,0,0,0,0]
        self.proflag = [0,0,0,0,0]

    def createunit(self,Map,screen,zoom_scale):
        #placeholder build timer
        unitTime = 5
        for character in self.character:
            if pro.produce(self,unitTime):
                Man = Worker("man1",self.Owner,100,100,0,2,Map,screen,character.pos.x + 50,character.pos.y + 50,zoom_scale)
                setup.spriteSetUpdate(self, 'assets/structurestandin.png')
                self.wlist.add(Man)
