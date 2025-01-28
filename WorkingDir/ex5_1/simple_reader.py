# simple_reader.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')

import csv

from typing import List, Iterator, Type, Optional

def csv_as_dicts(lines: Iterator, types: List, headers : Optional[List[str]] = None) -> List :
    '''
    Read lines from an iterable object into a list of dictionaries with optional type conversion
    '''

    records = []

    rows = csv.reader(lines)

    # Deal with headers == None
    if headers is None:
        headers = next(lines).split(',')

    for row in rows:
        record = { name: func(val) 
                   for name, func, val in zip(headers, types, row) }
        records.append(record)

    return records

def csv_as_instances(lines: Iterator, cls: Type, headers : Optional[List[str]] = None) -> List:
    '''
    Read lines from an iterable object into a list of dictionaries with optional type conversion
    '''

    records = []

    rows = csv.reader(lines)

    # Deal with headers == None
    if headers is None:
        headers = next(lines).split(',')

    for row in rows:
        record = cls.from_row(row)
        records.append(record)

    return records

# with the asterisk, all optional parameters can be provided only with parameter=value, not directly value
def read_csv_as_dicts(filename: str, types: List, *, headers : Optional[List[str]] = None):
    '''
    Call csv_as_dicts on a file
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types, headers=headers)
    

def read_csv_as_instances(filename: str, cls: Type, *, headers : Optional[List[str]] = None):
    '''
    Call csv_as_instances on a file
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls, headers=headers)


def main():

    port = read_csv_as_dicts('Data/portfolio.csv', [str, int, float])
    print(port)



if __name__=='__main__':
    main()