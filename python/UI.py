import pygame
from pygame.locals import *
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import python.classes as Class
import python.mouseStuff as mouse
import python.functions.unitTypeClassIndex as translator


class UI():
    def __init__(self):
        UIbotBackground = pygame.image.load("assets/UI/Game Overlay Bottom Background.png").convert_alpha()
        self.UIbotBackground = pygame.transform.scale(UIbotBackground, (1920, 1080))
        CommandUIborder = pygame.image.load("assets/UI/Command UI border icon.png").convert_alpha()
        self.CommandUIborder = pygame.transform.scale(CommandUIborder, (80,80))
        MapSprite = pygame.image.load("assets/Map Small.png").convert_alpha()
        self.MapSprite = pygame.transform.scale(MapSprite,(768,384)).convert_alpha()
        self.number = []
        self.resource = 0
        digits = pygame.image.load("assets/UI/Digits.png").convert_alpha()
        self.resourcesprite = pygame.image.load("assets/resourcestandin.png").convert_alpha()
        self.unitsprite = pygame.image.load("assets/playerstandin.png").convert_alpha()
        for i in range(10):
            number = pygame.transform.scale(digits.subsurface((0 +80 * i , 0, 80, 80)), (50, 50))
            self.number.append(number)

        self.totaltime = 0
        self.totalunits = 0

    def UIdraw(self,screen,colliders,dt):
        unitselect = False
        #basic setup
        map_rect = pygame.Rect(0, 730, 400, 400)
        pygame.draw.rect(screen,"#3684eb",map_rect)
        screen.blit(self.MapSprite,(-232,716))
        screen.blit(self.UIbotBackground, (0, 0)) #if you need to optimise don't draw this every frame and have it in the main line
        grouplist = self.number[1:10]
        for number in grouplist:
            number2 = pygame.transform.scale(number, (25, 25))
            screen.blit(number2, (450 + (self.number.index(number)-1)* 103, 795))
        
        #clock
        self.totaltime += dt
        digit1 = int(self.totaltime) % 10
        digit2 = int(self.totaltime / 10) % 6
        digit3 = int(self.totaltime / 60) % 10
        digit4 = int(self.totaltime / 600) % 10

        number = pygame.transform.scale(self.number[digit4], (25, 25))
        number2 = pygame.transform.scale(self.number[digit3], (25, 25))
        number3 = pygame.transform.scale(self.number[digit2], (25, 25))
        number4 = pygame.transform.scale(self.number[digit1], (25, 25))
        screen.blit(number, (290, 695))
        screen.blit(number2, (305, 695))
        screen.blit(number3, (325, 695))
        screen.blit(number4, (340, 695))

        #resource counter
        resourcecount = 0
        resource = pygame.transform.scale(self.resourcesprite, (50, 50))
        screen.blit(resource, (1500, 10))
        for structure in colliders[0]:
            if isinstance(structure, Class.Base):
                if structure.Owner == "Me":
                    resourcecount += structure.resource
        resource_number = str(resourcecount)
        for i, digit in enumerate(resource_number):
            if digit.isdigit():
                digit_index = int(digit)
                number = pygame.transform.scale(self.number[digit_index], (25, 25))
                screen.blit(number, (1560 + i * 10, 20))
        self.resource = resourcecount


        #unit counter
        unitcount = 0
        unit = pygame.transform.scale(self.unitsprite, (50, 50))
        screen.blit (unit,(1700,10))
        for collidergroup in colliders:
            for unit in collidergroup:
                if isinstance(unit, Class.Unit):
                    if unit.Owner == "Me":
                        unitcount += 1
                elif isinstance(unit, Class.Worker):
                    if unit.Owner == "Me":
                        unitcount += 1
        
        unitcount = str(unitcount)
        for i, digit in enumerate(unitcount):
            if digit.isdigit():
                digit_index = int(digit)
                number = pygame.transform.scale(self.number[digit_index], (25, 25))
                screen.blit(number, (1760 + i * 10, 20))
        
        self.totalunits = unitcount


        # selection interaction
        i = 0
        selectlist = []
        for collidergroup in colliders:
            for collider in collidergroup:
                if collider.selected:
                    if collider.Owner == "Me":
                        selectlist.append(collider)
        
        priority = {'Worker': 1, 'Unit': 0, 'Structure': 3, 'Base': 2}
        selectlist = sorted(selectlist, key=lambda obj: priority.get(obj.__class__.__name__, 99))
        for collider in selectlist:
            for character in collider.character:
                UI_image = pygame.transform.scale(character.image, (40,40))
                UI_border = pygame.transform.scale(self.CommandUIborder, (50,50))
                screen.blit(UI_image, (500 + i,875))
                screen.blit(UI_border, (495 + i, 870))
                i += 50
                unitselect = True
        
        if selectlist:
            for character in selectlist[0].character:
                UIunit = pygame.transform.scale(character.image, (100,100))
                text = selectlist[0].name
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render(text, True, (84, 97, 110))
                textRect = text.get_rect(center=(1160 +UIunit.get_width()/2, 865))
                screen.blit(text, textRect)
                screen.blit(UIunit, (1160, 890))

                unitType = None
                unitClass = None
                if hasattr(selectlist[0],'unitType') and hasattr(selectlist[0],'unitType'):
                    unitType, unitClass = translator.unitTypeClassIndex(selectlist[0].unitType,selectlist[0].unitClass)
                
                if unitType is not None and unitClass is not None:
                    font = pygame.font.Font('freesansbold.ttf', 16)
                    textType = unitType
                    text = font.render(textType, True, (84, 97, 110))
                    textRect = text.get_rect(center=(1160 +UIunit.get_width()/2 - 40, 1030))
                    screen.blit(text, textRect)

                    textClass = unitClass
                    text = font.render(textClass, True, (84, 97, 110))
                    textRect = text.get_rect(center=(1160 +UIunit.get_width()/2 + 40, 1030))
                    screen.blit(text, textRect)

        if unitselect:
            screen.blit(self.number[1], (420, 850))
            UIborder = pygame.transform.scale(self.CommandUIborder, (50, 50))
            screen.blit(UIborder, (420, 850))
            font = pygame.font.Font('freesansbold.ttf', 16)
            for i in range(2):
                screen.blit(self.CommandUIborder, (1465 + i* 100, 775))
                if isinstance(selectlist[0],Class.Unit):
                    if i == 0:
                        text = font.render("Move", True, (84, 97, 110))
                    elif isinstance(selectlist[0],Class.Worker):
                        text = font.render("Gather", True, (84, 97, 110))
                    else:
                        
                        text = font.render("Attack", True, (84, 97, 110))
                if isinstance(selectlist[0],Class.Structure):
                    if i == 0:
                        text = font.render("Path", True, (84, 97, 110))
                    else:
                        text = font.render("Build", True, (84, 97, 110))
                textRect = text.get_rect(center=(1465 + i* 100 + self.CommandUIborder.get_width()/2, 775 + self.CommandUIborder.get_height()/2))
                screen.blit(text, textRect)

