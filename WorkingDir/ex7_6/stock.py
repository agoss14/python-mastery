# stock.py

"""
Stock class redefined
NOTE: the import of String, PositiveInteger and PositiveFloat are missing because
of the usage of a metaclass into Structure that makes this import
"""
from structure import Structure

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