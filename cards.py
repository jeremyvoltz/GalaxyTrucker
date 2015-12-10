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
