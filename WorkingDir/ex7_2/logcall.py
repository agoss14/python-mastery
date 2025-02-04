# logcall.py

from functools import wraps

"""
Define a new decorator @logformat(fmt) that accepts a format string as
an argument and uses fmt.format(func=func) to format a supplied 
function into a log message
"""

def logformat(fmt):                              # 1 level --> additionals parameters for decorator arguments

    def log_function(func):                      # 2 level --> dynamic function

        print('Adding logging to', func.__name__)
    
        @wraps(func)
        def wrapper(*args, **kwargs):            # 3 level --> dynamic arguments of function
            print(fmt.format(func=func))
            return func(*args, **kwargs)
        return wrapper
    
    return log_function


logged = logformat('Calling {func.__name__}')    # example of using a decorator with arguments