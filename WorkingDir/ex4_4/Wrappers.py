# attribute_access_example.py

class Stock:

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    #example of __setattr__ usage: an alternative to __slots__
    def __setattr__(self, name, value):
        if name not in { 'name', 'shares', 'price' }:
            raise AttributeError('No attribute %s' % name)
        super().__setattr__(name, value) #super() invokes object.__setattr__ method

#########################################################################################

# an example of Proxy --> readonly object
class Readonly:
    def __init__(self, obj):
        self.__dict__['_obj'] = obj #we cannot use self._obj = obj cause it invokes the __setattr__ below
    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute") #we cannot set any attribute with object.<attr_name> method
    def __getattr__(self, name):
        return getattr(self._obj, name)
    
#########################################################################################

# an example of Delegation --> alternative to Inheritance
class Spam:
    def a(self):
        print('Spam.a')
    def b(self):
        print('Spam.b')

class MySpam:
    def __init__(self):
        self._spam = Spam()
    def a(self):
        print('MySpam.a')
        self._spam.a()
    def c(self):
        print('MySpam.c')
    #is not __getattribute__! This method is useful in case of attributes not present here (ex. b, see Spam)
    def __getattr__(self, name): 
        return getattr(self._spam, name)