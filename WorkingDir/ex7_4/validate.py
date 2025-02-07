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

_typed_classes = [
    ('Integer', int),
    ('Float', float),
    ('String', str) ]

globals().update((name, type(name, (Typed,), {'expected_type':ty}))
                 for name, ty in _typed_classes)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

###########################################################

# DECORATOR: validated() is a wrapper, that enables the usage of decorator @validated
def validated(func):
    """
    This is a wrapper usable as decorator in order to add validation functionalities to functions
    Validation: expected types (typehints) equals to provided arguments types (also on return)
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

###########################################################

# some examples of functions with decorators


@validated
def add(x: Integer, y: Integer):
    return x + y

@enforce(x=Integer, y=Integer, return_=Integer)
def mul(x, y):
    return x * y

###########################################################