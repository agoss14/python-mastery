# stock.py

import csv

from decimal import Decimal

class Stock:

    __slots__ = ['name', '_shares', '_price']

    _types = (str, int, float)  # class variable: useful for defining a variable that applies to all the istances

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    # Getter and setter for validation rules without change the way you use the class instances
    @property #modify the behaviour of self.shares
    def shares(self):
        return self._shares
    
    @property
    def price(self):
        return self._price
    
    @shares.setter #modify the behaviour of self.shares = something
    def shares(self,value):
        if isinstance(value, self._types[1]):
            if value >= 0:
                self._shares = value
                return
        raise TypeError(f'Expected a positive {self._types[1]}!')
    
    @price.setter
    def price(self,value):
        if isinstance(value, self._types[2]):
            if value >= 0:
                self._price = value
                return
        raise TypeError(f'Expected a positive {self._types[2]}!')


    @classmethod # class method: useful for defining an alternative inizializer
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)
        
    @property #this annotation let you call the method without double parenthesis, for ex: s.cost
    def cost(self):
        return self.shares * self.price
    
    def sell(self, shares):
        self.shares -= shares

    def __str__(self):
        return 'Stock: name=' + str(self.name) + ' shares=' + str(self.shares) + ' price=' + str(self.price)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.shares},{self.price})'
    
    def __eq__(self, other_stock):
        if type(other_stock) == type(self) and \
                    self.name == other_stock.name and \
                    self.shares == other_stock.shares and \
                    self.price == other_stock.price:
            return True
        return False
        
######################################################################

class DStock(Stock):
    _types = (str, int, Decimal)

def read_portfolio(filename, cls=Stock):

    with open(filename) as f:

        records = csv.reader(f)
        headers = next(records) #headers
        list_stocks = [cls.from_row(record) for record in records]

        return headers, list_stocks

    return

def print_portfolio(headers, portfolio):

    print('%10s %10s %10s' % (headers[0], headers[1], headers[2]))
    print('%10s %10s %10s' % ('----------', '----------', '----------'))
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
        
######################################################################

def main():

    headers, portfolio = read_portfolio('Data/portfolio.csv')

    print_portfolio(headers, portfolio)

    print(portfolio[0])

    ex_stock = Stock('AA', 100, 32.2)

    print(portfolio[0] == ex_stock)

    

if __name__=='__main__':
    main()