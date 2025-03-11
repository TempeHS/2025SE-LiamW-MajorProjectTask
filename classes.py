import pygame

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
    #@property uncomment when you have properties later
