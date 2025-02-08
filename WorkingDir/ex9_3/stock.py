# stock.py

"""
Stock class redefined
NOTE: the import of String, PositiveInteger and PositiveFloat are missing because
of the usage of a metaclass into Structure that makes this import
"""
from structly_package import *

class Stock(Structure):
    """
    Stock inherits from Structure, that has a method for implicity set the decorator
    @validate_attributes to Stock without explicity use @validate_attributes on this
    class (it is based on inheritance)
    In this way, it dinamically set the _fields class attribute, and invoke create_init()
    """

    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares: PositiveInteger):
        self.shares -= nshares

if __name__ == '__main__':
    
    portfolio = read_csv_as_instances('Data/portfolio.csv', Stock)
    #portfolio = read_csv_as_dicts('Data/portfolio.csv', [str, int, float])

    formatter = create_formatter('text')
    print_table(portfolio, ['name','shares','price'], formatter)