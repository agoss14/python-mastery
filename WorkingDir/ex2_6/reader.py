# reader.py

import csv

from pprint import pprint

from collections.abc import Sequence

import tracemalloc

from sys import intern

from abc import ABC, abstractmethod


# Define a utility function read_csv_as_columns() that reads a file of CSV data into lists
# of values, where each list represents a column of the CSV

class DataCollection(Sequence):

    # types is a list of column types
    def __init__(self, headings, types):

        for head in headings:
            setattr(self, head, [])

        self.headings = list(headings) #shallow copy
        self.types = list(types) #shallow copy

    def __len__(self):

        #All lists assumed to have the same length
        #Get first attribute without knowing its name
        first_attr_name, _ = next(iter(self.__dict__.items()))
        return len(getattr(self, first_attr_name))

    def __getitem__(self, index):

        # return a dictionary dinamically extracting each column value from the attribute (list)
        # with attr_name==columm
        return {column:getattr(self, column)[index] for column in self.headings}

    def append(self, row):

        """
        Foreach triple (value, column_name, type) in row, the function
        append to the list with the name equals to 'column_name' the 
        value casted with the function equivalent to the type (es. str)
        """
        for value, column_name, func in zip(row, self.headings, self.types):
            getattr(self, column_name).append(func(value))


def read_csv_as_columns(filename, types):

    """
    filename = name of the source file
    list_of_types = a list of types of columns, where the order matters
    """

    with open(filename) as f:

        rows = csv.reader(f)
        headings = next(rows)     # Skip headers

        print(f'Headers: {headings}')
        print(f'List of column types: {types}')

        records = DataCollection(headings, types)

        for row in rows:
            records.append(row)

    return records

#############################################################################

# Example of Template design pattern using an abstract class
class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)
    
# Define a utility function read_csv_as_dicts() that reads a file of CSV data into a list
# of dictionaries where the user specifies the type conversions for each column.
def read_csv_as_dicts(filename, list_of_types):

    """
    filename = name of the source file
    list_of_types = a list of types of columns, where the order matters
    """
    parser = DictCSVParser(list_of_types)
    return parser.parse(filename)

# Utility function that read a csv file and foreach each record create an instance of a class
def read_csv_as_instances(filename, cls):

    parser = InstanceCSVParser(cls)
    return parser.parse(filename)

#############################################################################

def main():

    print('Welcome to the reader tool!')

    #result = read_csv_as_dicts('Data/portfolio.csv', [str,int,float])
    #pprint(result)

    tracemalloc.start()

    result = read_csv_as_columns('Data/ctabus.csv', [intern, intern, intern, int])

    current, peak = tracemalloc.get_traced_memory()

    print('Memory Use: Current %d, Peak %d' % (current,peak))

    print('Length of result:', len(result))

    print(f'Example of record: {result[0]}')

    tracemalloc.stop()


if __name__=='__main__':
    main()