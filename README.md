# GalaxyTrucker
Galaxy Trucker is a board game where players build a space ship, and then race that space ship, encountering various challenges and boons along the way.  This is code that will (eventually) implement genetic algorithms to evolve fitter and fitter ships.

##Project overview as it stands

### Tiles:

 A Tile object has a 4-tuple of connectors (corresponding to the cardinal directions), which are encoded by the numbers 0,1,2,3 (0 means no connector on that side, 1 is the single connector, 2 the double, 3 the universal).  

The idea being that you can make subclasses that inherit from Tile, but are more specific.  So I made a ShieldTile class, which is a Tile object (it has connectors), but it also has a shield orientation.  And a CrewTile class, which has some number of crew.

A Tile object also has a method called rotate, which rotates its connectors (and its shield, if it’s a ShieldTile.  Cannons and engines will do the same thing, but I haven’t written those yet).

I also made a method which, given two tiles and their positions, determines if their connection is legal.  

###Ship:

I then made a Ship class, which has a list of spaces (x,y) (the centre is (0,0)), and on each of those spaces a tile can be placed.  I wrote a method called prune, which removes any pieces that are not connected to the centre legally.

###Example implementation:

I instantiated four tiles, put them around the centre of the ship, then called prune to make sure it works.  It seemed to be working, but with only text readout, it was extremely hard to tell if it was pruning correctly.  So I found a picture of all the game tiles pre-punched, sliced them up in photoshop, gave the Tile class an “image” attribute, assigned the four tiles I had instantiated their appropriate images, and then I was able to have the program draw the ship in a window with pyglet, so I could see if it was pruning it correctly.  And it all seems to be working.  The images are poor quality, as they're taken from a picture someone took on a desk, and I wasn’t careful about cutting them up perfectly.  They are simply for debugging purposes, and will not be used in the final form of this program.

###To Do:

1.  Implement the rest of the tile types (cannon, engines, batteries, aliens, and goods). 
2.  Instantiate all tiles in the game, and tie the tiles to their images.
3.  The hard part… game mechanics!  Flying the ships, resolving encounter cards, scoring, etc....  That’s the part I’m most worried about.
4.  Implement evolution.  That part shouldn’t be too hard, and the fun lies in deciding how best to tune that, how to mix the chromosomes, how to mutate, etc…  
