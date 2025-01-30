# typedproperty.py

def typedproperty(expected_type):

    # Closure to capture the field name
    def wrapper(name):
        private_name = '_' + name

        @property #property is a builtin descrptor that has already the __set_name__ function defined
        def value(self):
            return getattr(self, private_name)

        @value.setter
        def value(self, val):
            if not isinstance(val, expected_type):
                raise TypeError(f'Expected {expected_type}')
            setattr(self, private_name, val)

        return value

    return wrapper

# Type shortcuts
# NOTE: name is passed to wrapper(name) because @property is a builtin descriptor that already implements __set_name__

String = lambda: typedproperty(str)  # Calls typedproperty(str) and passes 'name' dynamically
Integer = lambda: typedproperty(int)
Float = lambda: typedproperty(float)

######################################################################

class Stock:
    name = String()     # No need to specify 'name' explicitly, cause it's implicity passed to the result of typedproperty(str)
    shares = Integer()  # No need to specify 'shares' explicitly
    price = Float()     # No need to specify 'price' explicitly

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __str__(self):
        return f'Stock: name={self.name}, shares={self.shares}, price={self.price}'

######################################################################

def main():
    s = Stock('PIPPO', 53, 34.56)
    print(s)

    # Testing type enforcement
    try:
        s.shares = "not an int"  # Should raise TypeError
    except TypeError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()