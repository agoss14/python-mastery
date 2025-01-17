
# readport.py

import csv

from pprint import pprint

from collections import Counter, defaultdict

# A function that reads a file into a list of dicts
def read_portfolio(filename):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {
                'name' : row[0],
                'shares' : int(row[1]),
                'price' : float(row[2])
            }
            portfolio.append(record)
    return portfolio

def main():

    portfolio = read_portfolio('Data/portfolio.csv')
    pprint(portfolio)

    # Find all holdings more than 100 shares
    #pprint([dict['name'] for dict in portfolio if dict['shares']>100])

    # Compute total cost (shares * price)
    #pprint(sum([dict['shares']*dict['price'] for dict in portfolio]))

    # Find all unique stock names (set)
    #pprint({dict['name'] for dict in portfolio})

    # Count the total shares of each of stock
    totals = defaultdict(int)
    for s in portfolio:
        totals[s['name']] += s['shares']

    pprint(totals)


if __name__ == '__main__':
    main()