# sample.py

from logcall import logged, logformat

@logged
def add(x,y):
    return x+y

@logged
def sub(x,y):
    return x-y

@logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x,y):
    return x*y


class Spam:
    
    @logged
    def instance_method(self):
        pass

    @classmethod
    @logged
    def class_method(cls):
        pass

    @staticmethod
    @logged
    def static_method():
        pass

    @property
    @logged
    def property_method(self):
        pass

s = Spam()


s.instance_method()
s.class_method()
s.static_method()
s.property_method
