# data_analysis.py

import sys
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex2_5')

from readrides import read_rides

from pprint import pprint

from collections import defaultdict, Counter

# how many bus ruotes exist in chicago
def counter_ruotes(rows):
    return len({ruote_record['route'] for ruote_record in rows})

# What is the total number of rides taken on each bus route?
def counter_rides_per_route(rows):

    result = defaultdict(int)
    for row in rows:
        result[row['route']] += row['rides']

    return result

def counter_rides_per_route_and_year(rows):

    result = defaultdict(int)
    for row in rows:
        year = row['date'][6:]
        result[(row['route'],year)] += row['rides']

    return result

# What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
def top_five_routes(records):
    
    #Get sum of rides foreach route
    count_rides_per_ruote_year = counter_rides_per_route_and_year(records)

    #Get set of distinct routes
    routes = {ruote_record['route'] for ruote_record in records}

    local_counter = Counter()

    #Calculate difference in rides between 2011 and 2001 foreach route
    for route in routes:
        rides_in_2001 = count_rides_per_ruote_year[(route, '2001')]
        rides_in_2011 = count_rides_per_ruote_year[(route, '2011')]
        local_counter[route] += (rides_in_2011 - rides_in_2001)
    
    return local_counter.most_common(5)



def main():
    rows = read_rides('././Data/ctabus.csv')

    #print('Number of ruotes in Chicago:', counter_ruotes(rows))

    # How many people rode the number 22 bus on February 2, 2011? 
    #print('Rides on route 22 on Feb 2, 2011:', [dd for dd in rows if dd['route']=='22' and dd['date']=='02/02/2011'])

    #print('Rides per route: ', counter_rides_per_route(rows))

    print(top_five_routes(rows))


if __name__ == '__main__':
    main()