# scopes.py

import sys

def _init():
    locs = sys._getframe(1).f_locals   # Get callers local variables
    self = locs.pop('self')
    for name, val in locs.items():
        setattr(self, name, val)

class Stock:
    def __init__(self, name, shares, price):
        _init()