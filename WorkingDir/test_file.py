# test_file.py

class Singleton:
    _instance = None  # Class-level variable to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:  # If the instance doesn't exist yet
            cls._instance = super().__new__(cls)  # Create and store the instance
        return cls._instance  # Return the same instance every time
    

a = Singleton()
b = Singleton()

print('a:', a)
print('b:', b)
print('a._instance', a._instance)
print('b._instance', b._instance)
