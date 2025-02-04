# validate.py

###########################################################

import inspect
from functools import wraps

# VALIDATE CLASSES AND METHODS

# Implemented as CUSTOM DESCRIPTOR
class Validator:

    def __init__(self, name=None):
        self.name = name

    # Called when the descriptor is placed in a class definition
    # useful method for inizializing a Validator object (example: String), without specifing two times the name
    # Without __set_name__ method: name = String('name')
    # With    __set_name__ method: name = String() --> the name of the descriptor is setted with the name of the object
    # cls is not used but it's important for the order of the parameters automatically provided to function
    def __set_name__(self, cls, name):
        #print('Set_name called, name:', name)
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

###########################################################

# DECORATOR: validated() is a wrapper, that enables the usage of decorator @validate
def validated(func):
    """
    This is a wrapper usable as decorator in order to add validation functionalities to functions
    """

    # Annotations of the function (dict() for making a copy)
    annotations = dict(func.__annotations__)
    #print(annotations)

    # Get the return annotation (if any)
    retcheck = annotations.pop('return', None)

    # Get the signature of the func
    bind_signature = inspect.signature(func)

    @wraps(func) #useful for preserving original informations in help(func)
    def wrapper(*args, **kwargs):

        errors = []

        #print('Calling', func)

        # Get arguments provided to func by its caller (no need to create a copy of the dict)
        bind_dict = bind_signature.bind(*args, **kwargs).arguments

        #foreach argument, check if it is of the annotated type (function typehints)
        for argument, validator in annotations.items():
            try:
                #try the validation method 'validator' (ex: String.check(value)) on the value provided by the Caller
                validator.check(bind_dict[argument])
            except Exception as e: 
                #catch the exception raised from check()
                errors.append(f'    {argument}: {e}') #append to the list error

        # If there is almost one error, it raises an Exception
        if errors:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))
            
        # Call the func and save result for check the type of the result (if specified)
        result = func(*args,**kwargs)
        
        # Enforce return check (if any)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f'Bad return: {e}') from None
            
        # Return the result of the funct
        return result
    
    return wrapper

# PARAMETRIC DECORATOR: enforce is a wrapper callable with a parametric decorator, similar to validated
def enforce(**annotations):

    # Get the return annotation (if any)
    retcheck = annotations.pop('return_', None)

    def decorate(func):

        # Get the signature of the func
        bind_signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):

            errors = []

            # Get arguments provided to func by its caller (no need to create a copy of the dict)
            bind_dict = bind_signature.bind(*args, **kwargs).arguments

            #foreach argument, check if it is of the annotated type (function typehints)
            for argument, validator in annotations.items():
                try:
                    #try the validation method 'validator' (ex: String.check(value)) on the value provided by the Caller
                    validator.check(bind_dict[argument])
                except Exception as e: 
                    #catch the exception raised from check()
                    errors.append(f'    {argument}: {e}') #append to the list error

            # If there is almost one error, it raises an Exception
            if errors:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))
            
            # Call the func and save result for check the type of the result (if specified)
            result = func(*args,**kwargs)
        
            # Enforce return check (if any)
            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f'Bad return: {e}') from None
            
            return result

        return wrapper
        
    return decorate


@validated
def add(x: Integer, y: Integer):
    return x + y

@enforce(x=Integer, y=Integer, return_=Integer)
def mul(x, y):
    return x * y

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

    # s = Stock('PIPPO', 12, 45.21)
    # print(s)

    print(add(1,3))

    print(mul(2,3))

if __name__=='__main__':
    main()