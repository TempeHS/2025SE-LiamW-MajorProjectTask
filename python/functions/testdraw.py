import pygame



def testdraw(self, zoom_scale,offset, internal_offset,screen):
    try:
        for character in self.character:
            cell_size = 32 * zoom_scale
            display_size = pygame.display.get_surface().get_size()
            internal_surf_size = screen.get_size()
            scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
            offset_x = (display_size[0] - scaled_size[0]) // 2
            offset_y = (display_size[1] - scaled_size[1]) // 2
            x = (character.pos.x + offset.x - internal_offset.x) * zoom_scale + offset_x - (internal_offset.x + 16)* zoom_scale + cell_size / 2
            y = (character.pos.y + offset.y - internal_offset.y) * zoom_scale + offset_y - (internal_offset.y + 16)* zoom_scale + cell_size / 2
            return x,y
    except AttributeError:
        cell_size = 32 * zoom_scale
        display_size = pygame.display.get_surface().get_size()
        internal_surf_size = screen.get_size()
        scaled_size = (internal_surf_size[0] * zoom_scale, internal_surf_size[1] * zoom_scale)
        offset_x = (display_size[0] - scaled_size[0]) // 2
        offset_y = (display_size[1] - scaled_size[1]) // 2
        x = (self.pos.x + offset.x - internal_offset.x) * zoom_scale + offset_x - (internal_offset.x + 16)* zoom_scale + cell_size / 2
        y = (self.pos.y + offset.y - internal_offset.y) * zoom_scale + offset_y - (internal_offset.y + 16)* zoom_scale + cell_size / 2
        return x,y