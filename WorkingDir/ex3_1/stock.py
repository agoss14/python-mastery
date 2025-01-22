# stock.py

import csv

from decimal import Decimal

class Stock:

    types = (str, int, float)  # class variable: useful for defining a variable that applies to all the istances

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod # class method: useful for defining an alternative inizializer
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls.types, row)]
        return cls(*values)
        
    def cost(self):
        return self.shares * self.price
    
    def sell(self, shares):
        self.shares -= shares

    def __str__(self):
        return "Stock: name=" + str(self.name) + " shares=" + str(self.shares) + " price=" + str(self.price)

class DStock(Stock):
    types = (str, int, Decimal)

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
        

def main():

    headers, portfolio = read_portfolio('Data/portfolio.csv')

    print_portfolio(headers, portfolio)

if __name__=='__main__':
    main()