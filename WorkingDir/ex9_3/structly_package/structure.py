# structure.py

"""
Define a structure to simplify the definition of a Class
""" 

__all__ = [
    'Structure',
    'typed_structure',
]

from .validation.validate import Validator, validated #import from a file in the same folder of this file
import inspect
from collections import ChainMap

# Metaclass useful for eliminate imports of validators in stock.py
class StructureMeta(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({}, Validator.validators)
        
    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)

# abstract class
class Structure(metaclass=StructureMeta):
    """
    With this abstract class, you can simplify the __init__ function of the classes that inherit from it
    """
    _fields = () #useful for __setattr__()
    _types = () #useful for from_row() method

    # set attributes that are contained into _fields()
    def __setattr__(self, name, value):
        if name.startswith('_') or name in self._fields:
            super().__setattr__(name, value)
        else:
            raise AttributeError('No attribute %s' % name)

    @classmethod
    def create_init(cls):
        """
        Function that sets the __init__ method using exec() and "cls._fields" class attribute
        """
        argstr = ','.join(cls._fields)

        code = f'def __init__(self, {argstr}):\n'

        for name in cls._fields:
            code += f'    self.{name} = {name}\n'

        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__'] #take __init___ method from locals of exec

    #Useful for using validate_attributes decorator without explicity set it to the child class
    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    #Alternative constructor for a class
    @classmethod
    def from_row(cls, row):
        #extracts fields from a row (ex: from a CSV) for make an cls object
        rowdata = [ func(val) for func, val in zip(cls._types, row) ]
        return cls(*rowdata)
    
    # Use with repr()
    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
              ','.join(f'{repr(getattr(self, field))}' for field in self._fields) + \
              ')'
    
    # Makes possible to iterate over attributes of an object using for attr in obj:...
    def __iter__(self):
        for name in self._fields:
            yield getattr(self, name)

    # Comparison operator
    def __eq__(self, other):
        """
        You can use tuple(self) because you defined the __iter__ method before!
        """
        return isinstance(other, type(self)) and tuple(self) == tuple(other)


#################################################################
#Create a class from Structure and validators

def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators) #Manually create a Class
    return cls

#################################################################

# Class decorator (usable with @validate_attributes on a class definition like Stock)
def validate_attributes(cls):
    """
    This decorator takes the class variables of a class and checks:
    if the attribute is an istance of a descriptor (Validator), it fills dynamically
    the _fields class attribute with the descriptor instance name.
    Lastly, it invoke create_init() for create the __init__ function of the class
    """
    validators = []

    # foreach attribute (variable, method) in the class...
    for name_attribute, val_attribute in vars(cls).items():

        if isinstance(val_attribute, Validator): # a descriptor

            #append to a list useful for create _fields
            validators.append(val_attribute)

        #apply a decorator foreach method in the class with annotations in the argument
        elif inspect.isfunction(val_attribute) and val_attribute.__annotations__: # a function
            setattr(cls, name_attribute, validated(val_attribute))

    #populating _fields class attribute
    cls._fields = [val.name for val in validators]

    #Append the expected_type to _types attribute of the class (see Structure
    #NOTE: if no expected_type (ex for NonEmpty() descriptor), the identity lambda function
    #implies that func(val) into from_row() method simply sets the value without a cast
    cls._types = tuple(getattr(val, 'expected_type', lambda x:x) for val in validators)

    #create the __init__ dinamically using exec() and _fields, see Structure
    if cls._fields:
        cls.create_init()

    return cls