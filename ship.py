class Space(object):
    """A space for a tile, a collection of which makes a ship.
    Locations are indexed by integers from the center piece."""
    def __init__(self, x, y):
        self.location = (x,y)
        # Should a space know what ship it belongs to?


class Tile(object):
    """A tile from the game, it occupies a space.  
    It takes a list of length 4 to represent connections.  
    Connections should be given as [north, south, east, west]."""
    def __init__(self, connectors):
        self.connectors = connectors
        self.space = None

    def rotate_connectors(self, n):
        self.connectors = self.connectors[n%4:]+self.connectors[:n%4]
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
    """A ship, which consists of spaces, and one crew tile in the center."""
    def __init__(self):
        self.center = Space(0, 0)
        self.center_crew_tile = CrewTile([3,3,3,3])
        self.spaces = [self.center]

        
if __name__ == '__main__':
   pass
