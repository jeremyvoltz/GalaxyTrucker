
class Tile(object):
    """A tile from the game. it occupies a space.  
    It can belong to a ship.  It takes a list of length 4 to 
    represent connections.  Connections should be given as
    [north, south, east, west], with values ranging from 0-4,
    which represent the different possible connections (0 being none)."""
    def __init__(self, connectors, image = None):
        self.connectors = connectors
        self.ship = None
        self.image = image  #Should we include this in the tile class?

    # rotate clockwise
    def rotate_connectors(self, n):
        self.connectors = self.connectors[-n%4:]+self.connectors[:-n%4]
        return self

    def rotate(self,n):
        self.rotate_connectors(n)
        return self


class ShieldTile(Tile):
    """A tile with a shield in the middle.  
    The shield can have one of four possible orientations:
    'NE', 'ES', 'SW', 'WN', indicating cardinal directions of coverage."""
    def __init__(self, connectors, orientation):
        super(ShieldTile, self).__init__(connectors)
        self.orientation = orientation
        
    def rotate(self, n):
        self.rotate_connectors(n)
        directions = "NESWN"
        ind = directions.find(self.orientation)
        self.orientation = directions[ind+(n%4):ind+(n%4)+2]
        return self


class CrewTile(Tile):
    """A tile with a crew pod in the middle.
    Orientation does not matter."""
    def __init__(self, connectors):
        super(CrewTile, self).__init__(connectors)
        self.connectors = connectors
        self.crew = 2


class Ship(object):
    """A ship, which consists of a dictionary of {space:tile}, 
    and its genetic code, which consists of tile probabilities."""
    def __init__(self, spaces, dna = None):
        self.tiles = spaces
        self.tiles[(0,0)] = CrewTile([3,3,3,3])
        self.dna = dna

    # removes pieces which are not legally connected to ship center
    def prune(self):
        checked = []
        connected = [(0,0)] 
        next = [(0,0)]
        while next:
            v = next[0]
            for p in self.tiles.keys():
                if all([dist(v,p)==1,
                    self.tiles[v],
                    self.tiles[p], 
                    p not in checked, 
                    p not in connected]):
                    if legal_connection(v,self.tiles[v],p,self.tiles[p]):
                        connected.append(p)
                        next.append(p)
            next.remove(v)


        for p in self.tiles.keys():
            if p not in connected:
                self.tiles[p] = None


def diff((a,b),(c,d)):
    return (a - c, b - d)

def dist((a,b), (c,d)):
    return abs(a-c)+abs(b-d)

# checks whether the connection between two tiles at two points p1, and p2 is legal.
# Returns None if the points are not neighbors of each other.
def legal_connection(p1, tile1, p2, tile2):
    if not dist(p1,p2)==1:
        return None
    difference = diff(p2, p1)
    # The lookup represents the indices of 'NESW' in the tile connectors
    tile1_lookup = {(0,1):0, (1,0): 1, (0,-1):2, (-1,0):3}
    tile1_side = tile1_lookup[difference]
    tile2_side = (tile1_side+2)%4
    tile1_connector = tile1.connectors[tile1_side]
    tile2_connector = tile2.connectors[tile2_side]
    if tile1_connector == 0 or tile2_connector == 0:
        return False
    if tile1_connector == 3 or tile2_connector == 3:
        return True
    return tile1_connector == tile2_connector



if __name__ == '__main__':

    # example to instantiate a ship with some tiles, then prune the ship
    points = [(0,0),(0,1),(1,0),(0,-1),(-1,0)]
    spaces = dict([(p,None) for p in points])
    
    ship = Ship(spaces)

    ship.tiles[(0,0)].image = "images/tile_61.jpg"
    tile1 = Tile([0,2,0,2], "images/tile_54.jpg")
    tile2 = Tile([2,1,0,3], "images/tile_47.jpg")
    tile3 = Tile([1,0,0,2], "images/tile_26.jpg")
    tile4 = Tile([0,0,0,3], "images/tile_137.jpg")
    
    ship.tiles[(0,1)] = tile1
    ship.tiles[(0,-1)] = tile2
    ship.tiles[(-1,0)] = tile3
    ship.tiles[(1,0)] = tile4
    # ship.prune()
    print ship.tiles


    #example to draw a ship with the above tiles, then prune it for the tiles to disappear

    import pyglet
    from pyglet.window import key

    window = pyglet.window.Window()
    # image0 = pyglet.resource.image("images/tile_61.jpg")
    # image1 = pyglet.resource.image("images/tile_54.jpg")
    # image2 = pyglet.resource.image("images/tile_47.jpg")
    # image3 = pyglet.resource.image("images/tile_26.jpg")
    # image4 = pyglet.resource.image("images/tile_137.jpg")
    images = {}
    for (x,y) in ship.tiles.keys():
        if ship.tiles[(x,y)]:
            images[(x,y)] = pyglet.resource.image(ship.tiles[(x,y)].image)


    @window.event
    def on_draw():
        window.clear()
        # image0.blit(300, 250)
        # image1.blit(300, 300)
        # image2.blit(300,200)
        # image3.blit(250,250)
        # image4.blit(350,250)
        for (x,y) in ship.tiles.keys():
            if ship.tiles[(x,y)]:
                images[(x,y)].blit(300+50*x,250+50*y)


    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.P:
            ship.prune()
            on_draw()

    pyglet.app.run()
