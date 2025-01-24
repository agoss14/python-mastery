# tableformat.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex2_6')

from reader import read_csv_as_instances
from stock import Stock

from abc import ABC, abstractmethod


# Table Formatter is an example of Handler design pattern.
# Here it's implemented as an Abstract Class
class TableFormatter(ABC):

    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass
    
class TextTableFormatter(TableFormatter):

    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVTableFormatter(TableFormatter):

    def headings(self, headers):
        print(','.join('%s' % h for h in headers))
    
    def row(self, rowdata):
        print(','.join('%s' % d for d in rowdata))

class HTMLTableFormatter(TableFormatter):

    def headings(self, headers):

        print('<tr>', end=' ')
        print(' '.join('<th>%s</th>' % field for field in headers), end=' ')
        print('</tr>')
    
    def row(self, rowdata):
        print('<tr>', end=' ')
        print(' '.join('<td>%s</td>' % cell for cell in rowdata), end=' ')
        print('</tr>')

# Some mixin classes to add format functionality to other classes
class ColumnFormatMixin:
    formats = [] #a class attribute
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])

# Utility function that enable to create an instance of a formatter specifing its name
# Returs a TableFormatter's child instance
def create_formatter(nameFormatter, column_formats=[], upper_headers=False):

    mapper_name_formatter = {
        'text': TextTableFormatter,
        'csv': CSVTableFormatter,
        'html': HTMLTableFormatter
    }

    if(nameFormatter not in mapper_name_formatter):
        raise RuntimeError('Unknown format %s' % nameFormatter)
    
    inheritance_tuple = (mapper_name_formatter[nameFormatter],)

    if upper_headers:
        inheritance_tuple = (UpperHeadersMixin,) + inheritance_tuple

    if column_formats:
        inheritance_tuple = (ColumnFormatMixin,) + inheritance_tuple

    formatter_cls = type('FormatterDynamicClass', inheritance_tuple, {'formats':column_formats})
    
    return formatter_cls()


def print_table(objects, attr_names, formatter):

    if(not isinstance(formatter, TableFormatter)):
        raise TypeError('Invalid Formatter!') 

    formatter.headings(attr_names)

    #check on attributes using the first object in the list objects
    check_attribute = [hasattr(objects[0], attribute) for attribute in attr_names]
    if(False in check_attribute):
        print('Invalid attribute list for objects in the container!')
        return

    for object in objects:
        rowdata = [getattr(object, attribute) for attribute in attr_names]
        formatter.row(rowdata)


def main():

    portfolio = read_csv_as_instances('Data/portfolio.csv', Stock)

    formatter = create_formatter('text', upper_headers=True, column_formats=['"%s"','%d','%0.2f'])
    print_table(portfolio, ['name', 'shares', 'price'], formatter)

if __name__=='__main__':
    main()