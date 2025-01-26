# validate.py

###########################################################

# VALIDATE CLASSES AND METHODS

# Implemented as Descriptor
class Validator:

    def __init__(self, name=None):
        self.name = name

    # useful method for inizializing a Validator object (ex: String), without specifing two times the name
    # Without __set_name__ method: name = String('name')
    # With    __set_name__ method: name = String() --> the name of the descriptor is setted with the name of the object
    # cls is not used but it's important for the order of the parameters automatically provided to function
    def __set_name__(self, cls, name):
        print('Set_name called, name:', name)
        self.name = name
    
    @classmethod #allows us to avoid the extra step of creating instances which we don't really need
    def check(cls, value):
        return value

    # example of descriptor method --> necessary if you want to use descriptors also for set method
    # after the first initialization of the object
    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class Typed(Validator):
    expected_type = object
    @classmethod #allows us to avoid the extra step of creating instances which we don't really need
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

def add(x, y):
    Integer.check(x)
    Integer.check(y)
    return x + y

###########################################################
# A class for some examples

class Stock:

    # descriptors usage (NOTE: the base class aka descriptor is 'Validator'!!!):
    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
       
    def __str__(self): #print()
        return 'Stock: name=' + str(self.name) + ' shares=' + str(self.shares) + ' price=' + str(self.price)

###########################################################

def main():

    #this is the order of super() evaluation
    # print('Check example:', Integer.check(10))
    # print('Add example:', add(5,9))
    # print('Positive integer example:', PositiveInteger.check(10))
    # print('PositiveInteger.__mro__: ',PositiveInteger.__mro__)

    s = Stock('PIPPO', 12, 45.21)
    print(s)

if __name__=='__main__':
    main()