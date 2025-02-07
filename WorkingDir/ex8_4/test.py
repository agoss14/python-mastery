# test.py

from follow import follow

# Experiment: Garbage collection of a running generator
f = follow('Data/stocklog.csv')
next(f)

del f

# Experiment: Closing a generator
f = follow('Data/stocklog.csv')
for line in f:
        print(line,end='')
        if 'IBM' in line:
            #NOTE: if you use break instead of f.close(), you will able to resume the generator
            f.close() 


# Experiment: no output from the generator
for line in f:
        print(line, end='')    # No output: generator is done

###################################################

from cofollow import printer

p = printer()

p.send('hello')

p.send(42)

# raise an exception inside the coroutine
p.throw(ValueError('It failed'))

