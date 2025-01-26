# object_dicts.py

class SimpleStock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price
        def cost(self):
            return self.shares * self.price
        
goog = SimpleStock('GOOG',100,490.10)
ibm  = SimpleStock('IBM',50, 91.23)