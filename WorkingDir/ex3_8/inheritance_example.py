# inheritance_example.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_2')
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex3_1')
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex2_6')

from tableformat import TextTableFormatter, print_table
from reader import read_csv_as_instances
from stock import Stock

class PortfolioFormatter(TextTableFormatter):
        def row(self, rowdata):
            formats = ['%s','%d','%0.2f']
            rowdata = [(fmt % d) for fmt, d in zip(formats, rowdata)]
            super().row(rowdata) #call the method from the superclass TextTableFormatter

def main():
    
    portfolio = read_csv_as_instances('Data/portfolio.csv', Stock)

    formatter = PortfolioFormatter()
    print_table(portfolio, ['name','shares','price'], formatter)
      
if __name__=='__main__':
    main()