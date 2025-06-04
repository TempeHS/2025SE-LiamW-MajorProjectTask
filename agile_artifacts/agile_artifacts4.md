# Agile Artifacts

## Sprint Backlog List Achievable

9. general collision system
10. ownership system for units (enemy, ally)

## Increment

- implementing hitboxes 
- implement collision stopping (when units hitboxes collide they should stop or similar behaviour)
- structure collisions should effect pathing 
- ownership system where there are now units that can't be controlled by the user
- implement object selector methods (rebinding move commanding onto right mouse button and selection onto left mouse button)
- one of these methods should allow the cursor to draw a box and select all objects (under the user's ownership) within that box

## Sprint Review

Sprint was estimated correctly. I implemented better hitboxes that would actually be used to detect general collisions between the objects. I also implemented a collision system that sends the unit in the other direction slightly stop this collision. I put in a hard limit on recollision from pathing so that 10 consecutive re-collisions would cause the units to lose pathing. This stops instant path stoppin when units collide but don't make them infinitely fight over a stationary point. I used the owner attribute of Object to determine if a unit can be controlled and in unitsetup added a way to change the sprite depending on this attribute.