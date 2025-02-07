# manually_create_class

"""
Manually create this class:

class Stock:
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares*self.price
    def sell(self,nshares):
        self.shares -= nshares

"""

def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
        
def cost(self):
        return self.shares*self.price

def sell(self,nshares):
        self.shares -= nshares

# Make a method table
methods = {
        '__init__': __init__,
        'cost': cost,
        'sell':sell 
        }

# Make a new type (Stock)
Stock = type('Stock', (object,), methods)