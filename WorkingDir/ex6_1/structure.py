# structure.py

"""
Define a structure to simplify the definition of a Class
"""

import sys
from abc import ABC
import inspect

# abstract class
class Structure(ABC):

    """
    With this abstract class, you can simplify the __init__ function of the classes that inherit from it
    """

    ##################################
    @classmethod
    def create_init(cls):
        """
        Function that sets the __init__ method using exec() (see stock.py under ex6_4)
        """
        argstr = ','.join(cls._fields)

        code = f'def __init__(self, {argstr}):\n'

        for name in cls._fields:
            code += f'    self.{name} = {name}\n'

        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__']

    ##################################


    @classmethod
    def set_fields(cls):
        """
        Function that sets the _fields variable of child classes using the signature of their constructor
        NOTE: cls is the class of the child that inherits from Structure class
        """
        sig = inspect.signature(cls) #signature on a class returns parameters of __init__ method
        cls._fields = list(sig.parameters)
        

    def __setattr__(self, name, value):
        """
        Restricts the allowed set of attributes to those listed in the _fields variable. 
        However, it should still allow any "private" attribute (name starting with _).
        """
        if (name[0] != '_') and (not name in self._fields) :
            raise AttributeError('No attribute %s' % name)
                
        return super().__setattr__(name, value)

    @staticmethod
    def _init():
        """
        Dinamically set values to attributes where (name=value) are locals of the caller function
        NOTE: self is the first local variable, so don't need to pass it explicity
        """
        locs = sys._getframe(1).f_locals # get local variables from the caller
        self = locs.pop('self') # the first element is the self, the others are parameters of caller function
        for name, val in locs.items():
            setattr(self, name, val)

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
              ','.join(f'{repr(getattr(self, field))}' for field in self._fields) + \
              ')'

#################################################################