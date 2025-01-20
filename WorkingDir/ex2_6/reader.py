# reader.py

import csv

from pprint import pprint

from collections.abc import Sequence

import tracemalloc

from sys import intern


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


# Define a utility function read_csv_as_dicts() that reads a file of CSV data into a list
# of dictionaries where the user specifies the type conversions for each column.

def read_csv_as_dicts(filename, list_of_types):

    """
    filename = name of the source file
    list_of_types = a list of types of columns, where the order matters
    """

    records = []

    with open(filename) as f:

        file_csv = csv.reader(f)
        headers = next(file_csv)

        print(f'Headers: {headers}')
        print(f'List of column types: {list_of_types}')

        for row in file_csv:
            records.append({header:func(value) for header, func, value in zip(headers,list_of_types,row)})

    return records


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