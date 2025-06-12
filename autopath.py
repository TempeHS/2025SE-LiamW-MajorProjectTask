from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import classes as Class
import unitsetup as setup


def ResourcePath(self, structurelist,zoom_scale,resourcelist): #resource to base
    candidate_centers = []
    scale_factor = 32 * zoom_scale
    for character2 in self.character:
        for structure in structurelist:
            for character3 in structure.character:
                center = character3.pos
                dist = (center - character2.pos).length()
                if isinstance(structure, Class.Base):
                    candidate_centers.append(structure)

    # Sort by distance to current position
    candidate_centers.sort(reverse=True,key=lambda c: (c.pos - character2.pos).length())
    
    #create_path but with structure location
    for character in candidate_centers[0].character:

        endx = int(character.pos.x // 32)
        endy = int(character.pos.y // 32)

        startx, starty = self.character.sprite.get_coord()
        start = self.grid.node(startx, starty)
        end = self.grid.node(endx, endy)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        setup.spriteResourcepath(self,resourcelist)

def ResourcePath2(self, structurelist,zoom_scale,resourcelist): #base to resource
    if not hasattr(self, "mined_from") or self.mined_from is None:
        print("No mined_from resource set for this worker.")
        return

    endx = int(self.mined_from.pos.x // 32)
    endy = int(self.mined_from.pos.y // 32)

    startx, starty = self.character.sprite.get_coord()
    start = self.grid.node(startx, starty)
    end = self.grid.node(endx, endy)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    self.path, _ = finder.find_path(start, end, self.grid)
    self.grid.cleanup()
    setup.spriteResourcepath(self,structurelist)