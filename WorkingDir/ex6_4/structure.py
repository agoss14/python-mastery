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
        cls.__init__ = locs['__init__']
    

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
              ','.join(f'{repr(getattr(self, field))}' for field in self._fields) + \
              ')'

#################################################################