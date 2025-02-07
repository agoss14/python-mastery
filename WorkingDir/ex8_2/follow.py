# follow.py

"""
The follow(filename) generator yields the last line produced in a file.
It starts from the end of the actual file, and wait for new lines (created
from another process, ex 'Data\stocksim.py') in the end of the file.
"""

import os
import time

# follow() is a PRODUCER useful for constructing a PIPELINE

# Function generator for iterating (useful for realtime reading of data from a file)
def follow(filename):

    f = open(filename)       # Open the file
    f.seek(0, os.SEEK_END)   # Move file pointer 0 bytes from end of file

    # Infine loop
    while True:
        line = f.readline()
        if line == '':
            time.sleep(0.1)   # Sleep briefly and retry
            continue          # Continue with the next iteration of the infinite loop (no yield)
        yield line            # Transmit a line to the caller (for line in follow(...))

#####################################################

# EXAMPLE OF PRODUCER

def main():

    print("Executed from:", os.getcwd()) #useful for debugging relative paths

    # Usage of a (infinite) generator
    for line in follow('Data/stocklog.csv'):
    
        # Print the line
        fields = line.split(',')
        name = fields[0].strip('"')
        price = float(fields[1])
        change = float(fields[4])
        if change < 0:
            print('%10s %10.2f %10.2f' % (name, price, change))

if __name__=='__main__':
    main()