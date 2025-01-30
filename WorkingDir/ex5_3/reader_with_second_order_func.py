# reader_with_second_order_func.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')

import stock

import csv

def convert_csv(lines, line_converter_function, *, headers=None):
    """
    Second order function: accepts a function (line_converter_function) as an input
    """
    records = []

    # Deal with headers == None
    if headers is None:
        headers = next(lines).split(',')

    rows = csv.reader(lines)

    # map() maps a function on an iterable, and returns an iterable (convertible to list)
    # the first parameter is the function that applies on each element of second parameter
    result = list(map(lambda row: line_converter_function(headers, row), rows))

    return result

###########################################################################################

def csv_as_dicts(lines, types, headers=None):
    '''
    Read lines from an iterable object into a list of dictionaries 
    with optional header if it's not the first row
    '''

    # Call the higher order function
    records = convert_csv(lines, 
                         lambda headers, row: { name: func(val) for name, func, val in zip(headers, types, row)},
                         headers=headers
                         )

    return records

def csv_as_instances(lines, cls, headers=None):
    '''
    Read lines from an iterable object into a list of dictionaries 
    with optional header if it's not the first row
    '''

    # Deal with headers == None
    if headers is None:
        headers = next(lines).split(',')

    # Call the higher order function
    records = convert_csv(lines, 
                          lambda headers, row: cls.from_row(row),
                          headers=headers)

    return records

###########################################################################################

# with the asterisk, all optional parameters can be provided only with parameter=value, not directly value
def read_csv_as_dicts(filename, types, *, headers=None):
    '''
    Call csv_as_dicts on a file
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types, headers=headers)
    

def read_csv_as_instances(filename: str, cls, *, headers=None):
    '''
    Call csv_as_instances on a file
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls, headers=headers)
    
###########################################################################################


def main():

    port = read_csv_as_instances('Data/portfolio.csv', stock.Stock)
    print(port)



if __name__=='__main__':
    main()