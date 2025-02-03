# stock.py

"""
Stock class redefined with usage of local spaces and signature of methods (see Structure)
"""

from structure import Structure

class Stock(Structure):

    #_fields is populated dinamycally with Stock.set_fields()

    def __init__(self, name, shares, price):
        self._init()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares

Stock.set_fields() # see Structure father class