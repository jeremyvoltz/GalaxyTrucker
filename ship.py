
class Tile(object):
    """A tile from the game. it occupies a space.  
    It can belong to a ship.  It takes a list of length 4 to 
    represent connections.  Connections should be given as
    [north, east, south, west], with values ranging from 0-3,
    which represent the different possible connections (0 being none)."""
    def __init__(self, connectors, art = None):
        self.connectors = connectors
        self.ship = None
        self.rotation = 0 # Keeps track of rotation for graphical sprite rotation
        self.art = art

    # rotate clockwise
    def rotate_connectors(self, n):
        self.connectors = self.connectors[-n%4:]+self.connectors[:-n%4]
        return self

    def rotate(self,n=1):
        self.rotate_connectors(n)
        self.rotation+=n
        return self

class ShieldTile(Tile):
    """A tile with a shield in the middle.  
    The shield can have one of four possible orientations:
    'NE', 'ES', 'SW', 'WN', indicating cardinal directions of coverage."""
    def __init__(self, connectors, orientation, art = None):
        super(ShieldTile, self).__init__(connectors, art)
        self.orientation = orientation
        
    def rotate(self, n=1):
        super(ShieldTile, self).rotate(n)
        directions = "NESWN"
        ind = directions.find(self.orientation)
        self.orientation = directions[(ind+(n%4))%4:(ind+(n%4))%4+2]
        return self


class CrewTile(Tile):
    """A tile with a crew pod in the middle.
    Orientation does not matter."""
    def __init__(self, connectors, art = None):
        super(CrewTile, self).__init__(connectors, art)
        self.connectors = connectors
        self.crew = 2


class CargoTile(Tile):
    """A tile with 2 or 3 cargo holds for goods."""
    def __init__(self, connectors, holds, art = None):
        super(CargoTile, self).__init__(connectors, art)
        self.holds = holds


class EngineTile(Tile):
       """A tile with an engine.  Engines always face south."""
       def __init__(self, connectors, art = None):
           super(EngineTile, self).__init__(connectors, art)     
              

class LaserTile(Tile):
    """A tile with a laser.  Lasers always point north."""
    def __init__(self, connectors, art = None):
           super(LaserTile, self).__init__(connectors, art)
           self.orientation = "N"
        
    def rotate(self, n=1):
        super(LaserTile, self).rotate(n)
        directions = "NESW"
        ind = directions.find(self.orientation)
        self.orientation = directions[(ind+(n%4))%4]
        return self

class Ship(object):
    """A ship, which consists of a dictionary of {space:tile}, 
    and its genetic code, which consists of tile probabilities."""
    def __init__(self, dna = None):
        self.tiles = {}
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
                    p not in connected]):
                    status = legal_connection(v,self.tiles[v],p,self.tiles[p])
                    if status:
                        connected.append(p)
                        next.append(p)
                    if status is False: 
                        self.tiles[p] = None
            next.remove(v)
        for p in self.tiles.keys():
            if p not in connected:
                self.tiles[p] = None

    # Checks if it's legally possible to place tile at (x,y)
    def check_placement(self, (x,y), tile):
        # engines can't be rotated, nor have anything behind them
        if type(tile) is EngineTile:
            if tile.rotation != 0:
                return False
            if (x,y-1) in self.tiles:
                if  self.tiles[(x,y-1)]:
                    return False

        # Can't place a tile infront of a laser
        if type(tile) is LaserTile:
            if (x,y+1) in self.tiles:
                if tile.orientation == "N" and self.tiles[(x,y+1)]:
                    return False
            if (x+1, y) in self.tiles:
                if tile.orientation == "E" and self.tiles[(x+1,y)]:
                    return False
            if (x,y-1) in self.tiles:
                if tile.orientation == "S" and self.tiles[(x,y-1)]:
                    return False
            if (x-1,y) in self.tiles:
                if tile.orientation == "W" and self.tiles[(x-1,y)]:
                    return False

        # Can't place a tile below an engine
        if (x,y+1) in self.tiles:
            if type(self.tiles[(x,y+1)]) is EngineTile:
                return False


        if (x,y-1) in self.tiles:
            if type(self.tiles[(x,y-1)]) is LaserTile:
                if self.tiles[(x,y-1)].orientation == "N":
                    return False
        if (x,y+1) in self.tiles:
            if type(self.tiles[(x,y+1)]) is LaserTile:
                if self.tiles[(x,y+1)].orientation == "S":
                    return False    
        if (x-1,y) in self.tiles:
            if type(self.tiles[(x-1,y)]) is LaserTile:
                if self.tiles[(x-1,y)].orientation == "E":
                    return False
        if (x+1,y) in self.tiles:
            if type(self.tiles[(x+1,y)]) is LaserTile:
                if self.tiles[(x+1,y)].orientation == "W":
                    return False

        connected = False
        for (i,j) in [(-1,0),(0,-1),(1,0),(0,1)]:
            if (x+i,y+j) in self.tiles:
                if self.tiles[(x+i,y+j)]:
                    status = legal_connection((x,y), tile, 
                        (x+i,y+j), self.tiles[(x+i,y+j)])
                    if status is False:
                        return False
                    if status is True:
                        connected = True
        return connected


# The following methods are useful utilities independent of the classes above.
def diff((a,b),(c,d)):
    return (a - c, b - d)

def dist((a,b), (c,d)):
    return abs(a-c)+abs(b-d)

# checks whether the connection between two tiles at two points p1, and p2 is legal.
# Returns None if the points are not neighbors of each other, or not connected.
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
    if tile1_connector == 0 and tile2_connector == 0:
        return None
    if tile1_connector == 0 or tile2_connector == 0:
        return False
    if tile1_connector == 3 or tile2_connector == 3:
        return True
    return tile1_connector == tile2_connector

