# Agile Artifacts

## Sprint Backlog List Achievable

11. enemy interaction (attacking)
12. Autopathing (workers and structures)
13. UI overlay

## Increment

- owner units and enemy units can interact with eachother by attacking commands and projectiles (so you'll need to make a moveset now)
- add a indicator that shows that a unit is selected
- when a worker unit is mining resources it will automatically path to it
- when a unit/worker is made from a structure it will inherit the path the structure has
- have UI overlay that is described in storyboards

## Sprint Review

This sprint was estimated well. The attack command is now implemented where a selected ally unit can attack an enemy unit by right click + A. I have also added a change in selection hitbox colour to show what units are selected + UI which displays all the units selected in a group. Autopathing for resource collection and unit production have also been implemented with some difficulty of path inheritance leading to more python files being made. The UI as described in the storyboards has been drawn into the engine with an in-game timer, HUD and unit selection interactions. I have also added a bonus of HP UI