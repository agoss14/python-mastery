# generators.py

# Function generator (not reusable, you have to redefine f=frange(...))
def frange(start,stop,step):
    while start < stop:
        yield start #emits a value
        start += step #next iteration

f = frange(0, 2, 0.25)

for x in f:
    print(x, end=' ')


##########################

# Class generator (you can reuse it without creating a new object)

class FRange:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step
    def __iter__(self):
        n = self.start
        while n < self.stop:
            yield n
            n += self.step

f = FRange(0, 2, 0.25)
print('\nFirst iteration')
for x in f:
    print(x, end=' ')

print('\nSecond iteration')
for x in f:
    print(x, end=' ')