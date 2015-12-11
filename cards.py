class Card(object):
    """An encounter card."""
    def __init__(self, arg):
        self.arg = arg

class EnemyCard(Card):
    """An enemy card, consisting of a combat strength
    that needs to be exceeded, and a penalty if unable."""
    def __init__(self, arg):
        self.arg = arg
        
class PirateCard(EnemyCard):
    """docstring for PirateCard"""
    def __init__(self, arg):
        self.arg = arg
        

def encounter(card, ship):
    pass

# here only for debugging purposes.  Ignore.
if __name__ == '__main__':
    
    from ship import *
    import pickle
    load = open('ship.pkl','rb')
    ship= pickle.load(load)
    load.close()
    # print legal_connection((0,-1),ship.tiles[(0,-1)], (0,0), ship.tiles[(0,0)])
    print ship.check_placement((-1,-1), ship.tiles[(-1,-1)])
    print ship.tiles[(-1,-1)].art
