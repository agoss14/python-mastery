# tableformat.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex2_6')

from reader import read_csv_as_instances

from stock import Stock, DStock, read_portfolio

def print_table(objects=[], attr_names=[]):

    header = ' '.join('%10s' % attribute for attribute in attr_names)
    dashes = ' '.join('----------' for attribute in attr_names)

    #check on attributes
    check_attribute = [hasattr(objects[0], attribute) for attribute in attr_names]
    if(False in check_attribute):
        print('Invalid attribute list for objects in the container!')
        return

    print(header)
    print(dashes)

    for object in objects:

        row_printed = ' '.join('%10s' % str(getattr(object, attribute)) for attribute in attr_names)

        print(row_printed)


def main():

    _, portfolio = read_portfolio('Data/portfolio.csv')

    print_table(portfolio, ['shares', 'name'])

    #read with the generic reader from csv into instances of a class from 'reader' module
    portfolio = read_csv_as_instances('Data/portfolio.csv', Stock)

    #an example of records in portfolio (is an instance of class Stock!)
    print(portfolio[0])

if __name__=='__main__':
    main()