# coticker.py

"""
Consume data that is PUSHED from the producer (cofollow.py)
"""
import sys

sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex8_1')
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_2')

from structure import Structure
from cofollow import consumer, follow
from tableformat import create_formatter, print_table
import csv
from io import StringIO

# A class for creating objects from received data
class Ticker(Structure):
    name = String()
    price =Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()


#FIRST CONSUMER
@consumer
def to_csv(target):
    """
    Consumer that process sent data from the PRODUCER to create csv lines
    Parameter is the target consumer
    Each data must be a file line
    """
    while True:
        line = yield #receive data from producer

        # Use StringIO to treat the line like a file object (expected from csv.reader())
        csv_file_like = StringIO(line)

        # Create a CSV reader object
        csv_reader = csv.reader(csv_file_like)

        # Read the line as a list of fields
        row = next(csv_reader)

        target.send(row) #send data to next consumer

#INTERMEDIATE
@consumer
def create_ticker(target):
    """
    Consumer that process sent data in order to create Ticker insances
    Parameter is the target (the next consumer)
    Each data must be a row (ex. extracted with csv)
    """
    while True:
        row = yield
        target.send(Ticker.from_row(row)) #send data to next consumer

# INTERMEDIATE
@consumer
def negchange(target):
    """
    Consumer that process sent data in order to filter negative records
    Parameter is the target (the next consumer)
    Each data must be an object (instance of Ticker in this case)
    """
    while True:
        record = yield
        if record.change < 0:
            target.send(record) #send data to next consumer


# LAST CONSUMER
@consumer
def ticker(fmt, fields):
    """
    Consumer that process sent data in order to create a row.
    Parameters are the format (string) and fields (a list)
    Each data must be an object (instance of Ticker in this case)
    """
    formatter = create_formatter(fmt)

    # Here we cannot use print_table like in pipeline with generators
    # cause we cannot transmit a generator (all the rows) to the function
    # Instead, we have to process each message (an object) separately!
    # See ticker.py for other details why it supports print_table()

    formatter.headings(fields) #one time because outside the loop     
    while True:
        rec = yield
        row = [getattr(rec, name) for name in fields] #foreach row
        formatter.row(row)


"""
Main program that hooks all of these components together 
to generate the same stock ticker as in the previous exercise.
"""
def main():
    
    #pipeline
    follow('Data/stocklog.csv', 
           to_csv(
               create_ticker(
                   negchange(
                       ticker(
                           'text',
                           ['name','price','change']
                       )
                   )
               )
           ))



if __name__=='__main__':
    main()