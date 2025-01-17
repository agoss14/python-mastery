def main():

    #open file Data/portfolio.dat
    with open('Data/portfolio.dat', 'r') as f:

        #read all lines
        lines = f.read().splitlines()

    #calculate sum of costs (shares*price) of all stocks in the file
    shares_totals = []

    for line in lines:
        shares_totals.append(int(line.split(' ')[1]) * float(line.split(' ')[2]))
    
    total_cost = sum(shares_totals)
    
    print(f'{total_cost:.2f}')



if __name__ == "__main__":
    main()