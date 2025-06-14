import pygame



def spriteSet(self,Image,x,y):
    for character in self.character:
        if self.Owner == 'Neutral':
            pass
        elif self.Owner != "Me":
            before, after = Image.split(".")
            Image = f"{before}E.{after}"
        image = pygame.image.load(Image).convert_alpha()
        bounding_rect = image.get_bounding_rect()
        cropped_image = image.subsurface(bounding_rect).copy()
        character.image = cropped_image
        character.rect = cropped_image.get_rect(center=(x, y))
        character.pos = character.rect.center

def spriteSetUpdate(self,Image):
    for character in self.character:
        if self.Owner != "Me":
            before, after = Image.split(".")
            Image = f"{before}E.{after}"
        image = pygame.image.load(Image).convert_alpha()
        bounding_rect = image.get_bounding_rect()
        cropped_image = image.subsurface(bounding_rect).copy()
        character.image = cropped_image

def spriteInheritpath(self, product):
    product.path = self.path[:]  # Copy the path

    # Get the structure's collision rect(s)
    structure_rects = [character.rect for character in self.character]

    # Filter out path points that would collide with the structure
    filtered_path = []
    for point in product.path:
        # Convert path point to pixel position (center of grid cell)
        x = point.x * 32 + 16
        y = point.y * 32 + 16
        point_rect = pygame.Rect(x - 2, y - 2, 4, 4)  # Same as your collision_rects

        # Check collision with any structure rect
        if not any(point_rect.colliderect(srect) for srect in structure_rects): #not sure how this code works need to research it
            filtered_path.append(point)

    # Optionally remove the first element if you want to skip the starting cell
    if filtered_path:
        filtered_path = filtered_path[1:]

    product.path = filtered_path

    # Set the filtered path for the internal Object
    for character in product.character:
        character.set_path(product.path)

def spriteResourcepath(self, resourcelist):
    # Collect all resource rects from all resources in the list
    resource_rects = []
    for resource in resourcelist:
        for character in resource.character:
            resource_rects.append(character.rect)

    # Filter out path points that would collide with any resource rect
    filtered_path = []
    for point in self.path:
        x = point.x * 32 + 16
        y = point.y * 32 + 16
        point_rect = pygame.Rect(x - 2, y - 2, 4, 4)
        if not any(point_rect.colliderect(srect) for srect in resource_rects):
            filtered_path.append(point)

    if filtered_path:
        filtered_path = filtered_path[1:]

    self.path = filtered_path

    for character in self.character:
        character.set_path(self.path)