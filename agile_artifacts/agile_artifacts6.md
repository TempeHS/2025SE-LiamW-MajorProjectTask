# Agile Artifacts

## Sprint Backlog List Achievable

14. create map sprite + mini map
15. change hitboxes to be inside sprites

17. command UI

## Increment

- have a new map sprite that has a matching matrix grid using Tiled
- have a minimap in the bottom left corner in the UI which is based off the new map sprite
- command UI in the bottom right

## Sprint Review

I implemented a map image using tiled as a tile engine. I designed all of the tiles in Adobe Photoshop with a 32x32 pixel canvas and then placed them into an isometric of 32x16. Inital implementation of indivdiually rendering each tiles was too intentive and reduced game performance (even more than current) and was swapped for just a static image. I went over the image in tiled again on a orthogonal grid and painted it over with an invisible tile that I would use for the pathfinding matrix for my classes which worked by taking the layer 2D array values from the tmx file and using that as the 2D array the project used to pass in. The mini-map is also a static image that uses the same one as the map rendered on screen. The UI command is hard coded and displays the actions of all the different unit and structure types in the game when they are the first priority in selection.