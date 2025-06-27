# 2025SE-LiamW-MajorProjectTask

## Dependencies 
- pip install pygames
- pip install pathfinding 
- pip install pytmx


## Project Overview

This project is a topdown PVE Real Time Strategy game. It has many of the mechnaics that are standard to the genre and contains UI elements that update depending on the situation in the game. There is a placeholder enemy that the users can interact with to try attack mechanics and also resource gathering and unit production processes that are also implemented into the project as the basis for the RTS genre.

## How to run program + Project Showcase + User Documentation

note: once in the game to move in the top left direction to reach the main game area
![console run command](/assets\READMEassets\ConsoleCommand.mkv.gif)

### Camera Movement

By moving your camera to the sides of the screen the camera will be moved around the play area. By moving you mouse into the top left corner you can reach the main map and where the sprites are. By using the scroll wheel you can zoom in and out on the gameplay area.
![camera movement](/assets\READMEassets\Camera%20Movement.mkv.gif)

### Selection UI

By left clicking holding and moving the mouse, you will draw a "selection rectangle". All things that collide with this selection box will be added to selection group displayed in the UI at the bottom of the screen where the first units command will show up in the bottom right panel.
![selection system](/assets\READMEassets\Selection.mkv.gif)

### Moving/Commanding Selected Objects

Selected objects will now respond to user inputs. Right clicking on the land tiles (green tiles) will cause the creation of a path that will be render on the screen. Units (the cirlces) will then move to the point that the indicator shows.
![movement system](/assets\READMEassets\Movement.mkv.gif)

### Resource Collection

When selecting workers (the circle with a spiral in it) and moving it to collide with the resource, it will stop at the collision point and begin to "mine". Once this is complete the sprite will update showing that it has a piece of resource and has taken from the resource. 
![resource collection system](/assets\READMEassets\Resource%20Collection.mkv.gif)

### Resource Deposition 
When a worker is in this "hasResource" state, it now gains the ability to deposit the resource it holds. By moving it to the base class (the left most square sprite), the worker will then lose this state and "deposit" it to the base. The UI in the top right should then update to show the added resource. The worke should also automatically begin pathing back to the resource it just collected from making this an automatic process.
![resource deposition system](/assets\READMEassets\Resource%20Deposition.mkv.gif)

### Collision System

When two sprite hitboxes collide (the red boxes around every sprite), they will begin to rebound off eachother. There is a system in place where if an object is trying to reach a point it will keep try post-collision until a certain amount of time has passed before it stops trying to path to this point. This allows for groups of units pathing to a point to not continue "fighting" over getting to that point.
![collision system](/assets\READMEassets\Collision%20system.mkv.gif)

### Production System

When a structure is selected, the user is now able to command these structures by pressing "B" on the keyboard. The selected structures will then begin to produce a unit which is shown by the updated UI. After a set period of time a new unit will come from the structure and inherit the "rally path" that the structure has. You can create a rally path by doing the same actions while moving units but instead the path will stay on the screen the structure will not move. The unit will then move along this path as if it is a movement command from the user.
![production system](/assets\READMEassets\Unit%20Production.mkv.gif)


### Attack System

If you more down from where all the red sprites are, there is a purple unit. This purple unit is the "enemy" which are the opponents in the game. Selected units can be pathed down to it. By press "A" on the keyboard and right clicking on a valid tile, they will "attack move". If the unit is "in range" (a set area of which an attack will occur) they will "attack" the enemy. The enemy unit will then lose health in their "healthbar" UI and the green bar will decrease. Once this bar is empty, the unit will "die" and disappear from the screen
![attack system](/assets\READMEassets\Attack.mkv.gif)


### Extra User Documentation
- you have to move to the top left to see the area
- if the game runs too slowly you can deload the map its in the custow_draw() function in Classes.CameraGroup "self.internal_surf.blit(ground,ground_offset - (1810,700) + (0,512))" just comment it out

Hotkeys:
- Move: Right Click
- Attack Move: A + Right Click
- Selection: Left Click
- Produce: B
- Cancel: C


## Sprint Summary

### Sprint 1: 

1. set up class for a unit
2. create the movement system (move to mouse click)

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-1
### Sprint 2: 

3. create structure class 
4. worker, child class from unit class 
5. resource class 

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-2
### Sprint 3: 

6. main base child class from structure class
7. standin sprite for worker with resource
8. camera system

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-3
### Sprint 4: 

9. general collision system
10. ownership system for units (enemy, ally)

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-4
### Sprint 5:

11. enemy interaction (attacking)
12. Autopathing (workers and structures)
13. UI overlay

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-5
### Sprint 6:

14. create map sprite + mini map
15. change hitboxes to be inside sprites
17. command UI

- https://github.com/TempeHS/2025SE-LiamW-MajorProjectTask/tree/sprint-6