# Agile Artifacts

## Sprint Backlog List Achievable

6. main base child class from structure class
7. standin sprite for worker with resource
8. camera system

## Increment

- have a base class that produces worker class instances 
- have a sprite for when the worker has gathered the resource
- have a method that allows the worker class with resources to deposit into the base class
- have a fully functioning camera system that can be moved by pushing against the corners/edges of the screen to explore the map

## Sprint Review

This sprint was predicted to be long but still ended up being an underestimate. The first three increments were done in first days of the sprint being launched but the camera system took lots of implementing to do. There are now several camera options that can be further implemented later in the project the main methods of using the mouse and the keyboard to adjust the camera are implemented. The zooming issues took a long time to fix but it came down to using the offset vectors to line up the sprites, matrix and pathfinder systems. There is a minor bug where the mouse cursor selector isn't quite lining up with the grid and disappearing depending on mouse movements which is likely just improper vector application. All the non-game parts of the project are done now and the project will be centred around the core aspects that will make this project a game rather than just a pathfinder simulator.