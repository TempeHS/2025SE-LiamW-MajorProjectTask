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
                
            """
            print(location)
            print(distanceX)
            print(distanceY)
            print(unitVectorX)
            print(unitVectorY)
            newlocationY = location.y + unitVectorY
            newlocationX = location.x + unitVectorX
            print(newlocationX)
            print(newlocationY)
            location.y = newlocationY 
            location.x = newlocationX """
    #@property uncomment when you have properties later
