# reader_with_error_checking.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')
import stock

import csv

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

###########################################################################################

def convert_csv(lines, line_converter_function, *, headers=None):
    """
    Second order function: accepts a function (line_converter_function) as an input
    """
    records = []

    rows = csv.reader(lines)

    # Deal with headers == None
    if headers is None:
        headers = next(rows)

    # read records with the line_converter_function
    for index, row in enumerate(rows):
        
        # try to read the row, if not possible catch the exception and continue to next row
        try:
            records.append(line_converter_function(headers,row))
        except ValueError as e:
            log.warning(f'Row {index+1}: Bad row:{row}')
            log.debug(f'Row {index+1}: Reason: {e}')
            continue

    return records

###########################################################################################

def csv_as_dicts(lines, types, headers):
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

def csv_as_instances(lines, cls, headers):
    '''
    Read lines from an iterable object into a list of dictionaries 
    with optional header if it's not the first row
    '''

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

    port = read_csv_as_dicts(
        'Data/missing.csv', 
        [str, int, float], 
        #headers=['name', 'shares', 'price']
        )
    print(port)



if __name__=='__main__':
    main()