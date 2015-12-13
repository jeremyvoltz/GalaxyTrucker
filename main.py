from ship import *
import random
import operator
import pyglet
from pyglet.window import key
import pickle


centers = ["tile_61.jpg", "tile_62.jpg", 
    "tile_63.jpg", "tile_64.jpg"]

tiles = [CrewTile([1,2,0,2], "tile_07.jpg"),
    CrewTile([2,1,2,2], "tile_08.jpg"),
    CrewTile([0,0,1,3], "tile_09.jpg"),
    CrewTile([0,1,0,3], "tile_10.jpg"),
    CargoTile([0,0,0,3], 2, "tile_28.jpg"),
    CargoTile([0,1,0,3], 2, "tile_30.jpg"),
    Tile([1,3,0,3], "tile_31.jpg"),
    Tile([1,3,1,3], "tile_32.jpg"),
    Tile([1,3,2,3], "tile_33.jpg"),
    Tile([2,3,0,3], "tile_34.jpg"),
    Tile([3,1,2,3], "tile_35.jpg"),
    CargoTile([0,1,0,2], 3, "tile_52.jpg"),
    EngineTile([0,3,0,0], "tile_58.jpg"),
    EngineTile([1,0,0,0], "tile_60.jpg"),
    EngineTile([1,1,0,0], "tile_67.jpg"),
    EngineTile([2,0,0,0], "tile_68.jpg"),
    EngineTile([2,0,0,0], "tile_69.jpg"),
    EngineTile([2,3,0,0], "tile_70.jpg"),
    EngineTile([3,2,0,0], "tile_71.jpg"),
    EngineTile([0,3,0,1], "tile_72.jpg"),
    EngineTile([3,0,0,1], "tile_73.jpg"),
    EngineTile([1,2,0,2], "tile_74.jpg"),
    EngineTile([2,0,0,2], "tile_75.jpg"),
    EngineTile([3,1,0,2], "tile_76.jpg"),
    LaserTile([0,0,1,0], "tile_100.jpg"),
    LaserTile([0,0,1,0], "tile_101.jpg"),
    LaserTile([0,0,2,0], "tile_102.jpg"),
    LaserTile([0,0,2,3], "tile_103.jpg"),
    LaserTile([0,1,0,3], "tile_104.jpg"),
    LaserTile([0,1,2,0], "tile_110.jpg"),
    LaserTile([0,3,0,0], "tile_113.jpg")]

# The probability of a tile mutation on each ship in a generation.
MUTATION_RATE = 1


def breed(ship1,ship2):
    """Given two ships, this method returns a child ship by 
    selecting tiles randomly between the two ships at each location.
    The returned ship should be legal, as the prune method is called 
    before return."""
    ship = Ship()
    ship.tiles[(0,0)] = CrewTile([3,3,3,3], centers[0])
    assert(set(ship1.tiles.keys()) == set(ship2.tiles.keys()))
    for s in list(set(ship1.tiles.keys())-set([(0,0)])):
        ship.tiles[s] = None
        tile = random.choice([ship1.tiles[s], ship2.tiles[s]])
        if tile:
            if ship.check_placement(s, tile):
                ship.tiles[s] = tile

    ship.prune()
    return ship


def fitness(ships):
    """Returns a list of the input ships ranked by their fitness.  
    This will eventually be decided by their ranking at the end 
    of a game, but for now, fitness is simply determined by speed.
    """
    speed = {}
    for ship in ships:
        speed[ship] = 0
        for s in ship.tiles:
            if type(ship.tiles[s]) is EngineTile:
                speed[ship] += 1
    # return list of tuples of (ship, speed) sorted by maximum speed
    ranking = list(reversed(sorted(speed.items(), key=operator.itemgetter(1))))
    return [ship for ship, speed in ranking]


def mutate(ships):
    """ Given a list of ships, for each ship it selects 
    a random location and replaces the tile with a 
    random legal alternative with probability MUTATION_RATE.  
    It is selecting from all tile spaces available, which 
    could be far from the center and thus no tile will suffice.
    """
    used = []
    for ship in ships:
        used + ship.tiles.values()
    for ship in ships:
        s = random.choice(list(set(ship.tiles.keys())-set([(0,0)])))
        if random.random() < MUTATION_RATE:
            legals = []
            for t in tiles:
                if t not in used:
                    for r in range(3):
                        t.rotate(r)
                        if ship.check_placement(s,t):
                            legals.append((t,r))
                        t.rotate(-r)
            if legals:
                t,r = random.choice(legals)
                t.rotate(r)
                ship.tiles[s] = t
                used.append(t)
    for ship in ships:
        ship.prune()
    return ships


# method which takes a list of ships and builds them according to their dna.
def build(ships, points):
    """Takes a list of ships and a collection of points
     and gives each a random, legal assortment of tiles."""
    used = []
    for ship in ships:
        ship.tiles[(0,0)] = CrewTile([3,3,3,3], centers[0])
        for s in list(set(points) - set([(0,0)])):
            legals = []
            for t in tiles: # find legal pieces at s
                if t not in used:
                    for r in range(3):
                        t.rotate(r)
                        if ship.check_placement(s,t):
                            legals.append((t,r))
                        t.rotate(-r)
            if legals:
                t,r = random.choice(legals) # choose when using weights given by dna
                t.rotate(r)
                ship.tiles[s] = t
                used.append(t) # mark the tile used
            else:
                ship.tiles[s] = None
    return ships


def draw(ship):
    """This program draws the inputted ship onto a pyglet window object,
    which is stored in memory.  To see any such windows, one must call 
    pyglet.app.run() afterwards for the window objects to be displayed.
    Given a displayed window, pressing 'P' runs ship.prune(), though this 
    should be unecessary, as ship.prune() is run after mutation and breeding.
    """
    # create a window object with pyglet,
    # a python GUI module
    window = pyglet.window.Window()
    
    # add the images to pyglet as resources, then as sprites.
    # we batch the sprites together so that they can be drawn together.
    # images are approx 50px square (51x48), and the center 
    # of the window is (300, 250), measured from the bottom left.
    # here we normalize the sprites to be 50px by 50px, and set the 
    # rotation anchor in the center.  Then we rotate the sprite accordingly.
    images = {}
    tile_sprites = {}
    batch = pyglet.graphics.Batch()
    for (x,y) in ship.tiles.keys():
        if ship.tiles[(x,y)]:
            img = pyglet.resource.image("images/"+str(ship.tiles[(x,y)].art))
            sprite = pyglet.sprite.Sprite(img, 300+50*x, 250+50*y, batch=batch)

            sprite.image.height = 50 # normalize 
            sprite.image.width = 50
            sprite.image.anchor_x = 25
            sprite.image.anchor_y = 25
            sprite.rotation = 90*ship.tiles[(x,y)].rotation

            tile_sprites[(x,y)] = sprite
            
    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    # when "P" is pressed on the keyboard, ship.prune is called.
    # The window is then redrawn with whatever tiles remain.
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.P:
            ship.prune()
            for (x,y) in tile_sprites.keys():
                if not ship.tiles[(x,y)]:
                    tile_sprites[(x,y)].visible = False
            on_draw()


def weight(ships):
    """Given a list of ships, this returns a list of those ships,
    but with multiple occurences, weighted by their order upon input,
    so that 'random.choice()' will given weighted choices."""
    n = len(ships)
    weight = []
    for i in range(n):
        weight += i*[ships[n-(i+1)]]
    return weight


def game(gens, points, num_of_ships = 4):
    """Simulates games with 'num_of_ships' ships, runs fitness test, 
    then breeds the resulting ranked ships into pairs using the weight 
    method, with possible mutation each generation.  It returns the 
    final list of ships after 'gens' generations.
    """
    used = []
    ships = [Ship() for i in range(num_of_ships)]
    build(ships, points)

    for i in range(gens):
        ranking = fitness(ships)
        weighted = weight(ranking)
        ships = [breed(random.choice(weighted), random.choice(weighted)) for _ in range(num_of_ships)]
        mutate(ships)
    return ships


# save the ship for debugging purposes
def pickle(ship):
    output = open('ship.pkl', 'wb')
    pickle.dump(ship,output)
    output.close()


if __name__ == '__main__':

    # Run a simulation using the methods above.

    # Points are created and sorted by distance from the origin.
    points = []
    for i in range(-3,4):
        for j in range(-3,4):
            points.append((i,j))
    points = sorted(points, key = lambda x: dist((0,0),x))

    # Run the simulation.
    ships = game(50,points,100)

    # Display the five most fit ships at the end of the simulation.
    for ship in ships[:5]:
        draw(ship)
    pyglet.app.run()


