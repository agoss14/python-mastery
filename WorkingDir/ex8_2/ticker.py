# ticker.py

"""
PULL data from a producer (follow.py) using generators
The last consumer is generator that lastly consume data 
Here is the code inside the last loop in print_table()
NOTE: in print_table() the print of headers is outsite the loop, 
so it's printed only one time! 
"""

import sys

sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex8_1')
from structure import Structure

class Ticker(Structure):
    name = String()
    price = Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()

def main():

    from follow import follow
    import csv
    import os
    sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_2')
    from tableformat import create_formatter, print_table

    # Formatter for data
    formatter = create_formatter('text')

    # Absolute path for the input file
    file_path = os.path.abspath('Data/stocklog.csv')
    print('Absolute path of the file: ',file_path)

    # PRODUCER
    lines = follow(file_path)

    # PROCESSING
    rows = csv.reader(lines)
    records = (Ticker.from_row(row) for row in rows) #another generator

    # CONSUMER
    negative = (rec for rec in records if rec.change < 0) #another generator

    # FINAL CONSUMER
    #NOTE: print_table contains a for ... in ... (generator) in which there is the final consumer
    print_table(negative, ['name','price','change'], formatter) 


if __name__ == '__main__':
    main()