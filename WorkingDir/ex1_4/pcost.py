
def portfolio_cost(filename):

    print(filename)

    try:
        #open file Data/portfolio.dat
        with open(filename, 'r') as f:

            #read all lines
            lines = f.read().splitlines()

    except Exception as e:
        print("EXCEPTION: File name is not valid.")
        print("Reason: ", e)
        return

    #calculate sum of costs (shares*price) of all stocks in the file
    shares_totals = []

    for line in lines:

        try:
            fields = line.split()
            nshares = int(fields[1])
            price = float(fields[2])
            shares_totals.append(nshares * price)

        except ValueError as e:
            print(f'EXCEPTION: Couldn\'t parse: \'{line}\'')
            print('Reason: ', e)  
    
    total_cost = sum(shares_totals)
    
    print(f'{total_cost:.2f}')


def main():
    portfolio_cost('../../Data/portfolio2.dat')


if __name__ == "__main__":
    main()