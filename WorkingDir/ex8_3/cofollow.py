# cofollow.py

"""
Data flow with COROUTINE
NOTE: 
The only difference between pipelines with generators and pipeline
with coroutines is that with a coroutine, you PUSH data into different
processing elements as OPPOSED TO PULLING data out with a for-loop.
"""

import os
import time

# Data source
def follow(filename,target):
    """
    In this function we have to provide
    filename but also target, because it
    is pushing data, not pulling (like in generators)
    """
    with open(filename,'r') as f:
        f.seek(0,os.SEEK_END)
        while True:
            line = f.readline()
            if line != '':
                target.send(line) #send the line to target
            else:
                time.sleep(0.1)

# Decorator for coroutine functions
from functools import wraps

# Define a wrapper for consumer functions useful for coroutine priming
def consumer(func):
    @wraps(func)                # with this, wrapped functions retains original metadata (like __name__)
    def start(*args,**kwargs):
        f = func(*args,**kwargs)
        f.send(None)
        return f
    return start

################################################################

# Sample coroutine that uses consumer decorator for coroutine priming (send(none))
@consumer
def printer():
    while True:
        item = yield     # Receive an item sent to me
        print(item)

# Example use
if __name__ == '__main__':
    follow('Data/stocklog.csv',printer())