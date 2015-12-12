from ship import *
import random
import operator

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


def random_gene(spaces, tiles):
    gene = {}
    for s in spaces:
        v = []
        for t in tiles:
            for r in range(4):
                v.append([(t,r),random.random()])
        gene[s] = v
    return gene


def weighted_choice(choices):
    if len(choices) == 0:
        return None
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
       if upto + w >= r:
          return c
       upto += w
    assert False, "Shouldn't get here"

# A method to breed two genes into a child gene.
def breed(gene1, gene2):
    assert(set(gene1.keys()) == set(gene2.keys()))
    child = {}
    for s in gene1.keys():
        r = random.randint(0,len(gene1[s]))
        child[s] = gene1[s][:r] + gene2[s][r:]
    return child

# method to test which ship is the fittest, in this simple case, speed is the test.
def fitness(ships):
    speed = {}
    for ship in ships:
        speed[ship] = 0
        for s in ship.tiles:
            if type(ship.tiles[s]) is EngineTile:
                speed[ship] += 1
    # return ship with maximum speed
    return  list(reversed(sorted(speed.items(), key=operator.itemgetter(1))))

# method which takes a list of ships and builds them according to their dna.
def build(ships, points):
    used = [] 
    for ship in ships:
        ship.tiles[(0,0)] = CrewTile([3,3,3,3], centers[0])
        for s in points:
            legals = []
            for (t,r),w in ship.dna[s]: # find legal pieces at s
                if t not in used:
                    t.rotate(r)
                    if ship.check_placement(s,t):
                        legals.append([(t,r),w])
                    t.rotate(-r)
            if legals:
                t,r = weighted_choice(legals) # choose when using weights given by dna
                t.rotate(r)
                ship.tiles[s] = t
                used.append(t) # mark the tile used
    return ships

# method to simulate games with four ships, fitness test, then breeding
def game(n):
    points = [(0,1),(1,0),(0,-1),(-1,0), (-1,-1),(1,1),(1,-1),(-1,1)]
    ships = [Ship() for j in range(4)]
    for ship in ships:
        ship.dna = random_gene(points, tiles)
    evolved_dna = {}

    for i in range(n):
        build(ships, points)
        ranking = fitness(ships)
        evolved_dna = breed(ranking[0][0].dna, ranking[1][0].dna)
        random_gene1 = random_gene(points, tiles)
        random_gene2 = random_gene(points, tiles)
        random_gene3 = random_gene(points, tiles)
        ships = [Ship(evolved_dna),
            Ship(evolved_dna),
            Ship(random_gene1),
            Ship(random_gene2)]
    
    return evolved_dna


if __name__ == '__main__':

    dna = game(100)
    ship = Ship(dna)
    points = [(0,1),(1,0),(0,-1),(-1,0), (-1,-1),(1,1),(1,-1),(-1,1)]
    build([ship], points)
    back = dna[(0,-1)]
    for (t,r),w in back:
        if type(t) is EngineTile:
            print t.art,r,w

    # # example to instantiate a ship and build it using a random gene.

    # # The order of points matters, as the ship must build from the center out.
    # points = [(0,1),(1,0),(0,-1),(-1,0), (-1,-1),(1,1),(1,-1),(-1,1)]
    
    # ship = Ship()
    # ship.dna = random_gene(points, tiles)

    # # can't allow reusing tiles, because calling rotate on a tile
    # # that's already been placed breaks the ship.  Hence the list used.
    # used = [] 
    # ship.tiles[(0,0)] = CrewTile([3,3,3,3], centers[0])
    # for s in points:
    #     legals = []
    #     for (t,r),w in ship.dna[s]: # find legal pieces at s
    #         if t not in used:
    #             t.rotate(r)
    #             if ship.check_placement(s,t):
    #                 legals.append([(t,r),w])
    #             t.rotate(-r)
    #     if legals:
    #         t,r = weighted_choice(legals) # choose when using weights given by dna
    #         t.rotate(r)
    #         ship.tiles[s] = t
    #         used.append(t) # mark the tile used
    
    
    # save the ship for debugging purposes
    import pickle
    output = open('ship.pkl', 'wb')
    pickle.dump(ship,output)
    output.close()



    # what follows is an example to draw a ship 
    # with the above tiles, then by pressing 'P' 
    # prune it for the unconnected tiles to disappear.

    import pyglet
    from pyglet.window import key

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


    pyglet.app.run()




