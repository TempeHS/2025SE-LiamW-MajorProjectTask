# Agile Artifacts

## Sprint Backlog List Achievable

3. create structure class 
4. worker, child class from unit class 
5. resource class 

## Increment

- have a new structure class that is child class or independent from unit class. 
- Have a structure can produce a unit (make an instance of a unit). 
- Have a worker class on unit to decide if they can gather resource or not. 
- have a resource class and have a worker gather resources from that object created

## Sprint Review

This sprite was a very large underestimate with the inclusion of lots of unforseen issues that took very long to fix. All the increments are delivered. The structure class can produce a fully working unit that follows its own path and updates the same as the original unit. The worker class can collect resources from the resource class. This required a collision system that I fundamentally didn't understand until I did visual debugging by showing the rects of each instance. After realising character is updating not the actual object allowed me to quickly implement the rest of the resource collection system. There is still no sprite for once the worker has collected the resource and not where for the unit to deposit the resource. 