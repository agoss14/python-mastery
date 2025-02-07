# stock.py

"""
Stock class created from a function
"""
from structure import typed_structure
from validate import String, PositiveInteger, PositiveFloat

Stock = typed_structure(
    'Stock', #class name
    name=String(), #Validators (fields to create as attributes)
    shares=PositiveInteger(), 
    price=PositiveFloat())