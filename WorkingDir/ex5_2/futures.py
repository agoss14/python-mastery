# futures.py

import time
import threading
from concurrent.futures import Future


def worker(x, y):
    print('About to work')
    time.sleep(20)
    print('Done')
    return x + y

# Wrapper around the function to use a future
def do_work(x, y, fut):
    fut.set_result(worker(x,y))

fut = Future()

t = threading.Thread(target=do_work, args=(2, 3, fut))

t.start()

print('This print is from the main thread, not the secondary!')

# sincronization with the secondary thread
result = fut.result()

print('Result is: ',result)

