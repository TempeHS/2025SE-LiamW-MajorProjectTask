import pygame


class Mouse():
    def __init__(self):
        self.mouse_pos_start = (0, 0)
        self.clicking = False
        self.selection_rect = None
        self.flag = True

    def selectioncol(self,selrect, colliders, offset, internal_offset, zoom_scale, screen, cameralist):
        gonelist = list(cameralist)
        cell_size = 32 * zoom_scale
        display_size = pygame.display.get_surface().get_size()
        internal_surf_size = screen.get_size()
        scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
        offset_x = (display_size[0] - scaled_size[0]) // 2
        offset_y = (display_size[1] - scaled_size[1]) // 2
        for collidergroup in colliders:
            for collider in collidergroup:
                if collider is self:
                    continue
                for character in collider.character:
                    # Project character.rect to screen coordinates
                    char_rect = character.rect.copy()
                    char_rect.x = (char_rect.x + offset.x - internal_offset.x) * zoom_scale + offset_x - (internal_offset.x + 16)* zoom_scale + cell_size / 2
                    char_rect.y = (char_rect.y + offset.y - internal_offset.y) * zoom_scale + offset_y - (internal_offset.y + 16)* zoom_scale + cell_size / 2 #potential calibration error later
                    char_rect.width = char_rect.width * zoom_scale
                    char_rect.height = char_rect.height * zoom_scale
                    pygame.draw.rect(screen, (0, 255, 0), char_rect, 2)  # Draw character rect for debugging
                    if selrect.colliderect(char_rect):
                        print(f"Collision with {character.name}")
                        collider.selected = True
                        for character in collider.character:
                            character.selected = True
                        gonelist.remove(collider)

        for goner in gonelist:
            goner.selected = False
            for character in goner.character:
                character.selected = False


    def selection(self, screen,colliders, offset, internal_offset, zoom_scale, cameralist):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if self.flag:
                self.mouse_pos_start = mouse_pos
                self.flag = False
            self.selection_rect = pygame.Rect(self.mouse_pos_start[0], self.mouse_pos_start[1], mouse_pos[0] - self.mouse_pos_start[0], mouse_pos[1] - self.mouse_pos_start[1])
            self.selectioncol(self.selection_rect, colliders, offset, internal_offset, zoom_scale, screen,cameralist)
            pygame.draw.rect(screen, (255, 0, 0), self.selection_rect, 2)

        else:
            self.flag = True


