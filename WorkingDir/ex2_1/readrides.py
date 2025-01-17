# readrides.py

import csv

from collections import namedtuple

class Record:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

class RecordSlots:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_rides(filename,mode=1):
    '''
    Read the bus ride data as a list of tuples
    '''            
    records = []
    with open(filename) as f:

        rows = csv.reader(f)
        headings = next(rows)     # Skip headers

        for row in rows:
            
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])

            record=None

            if mode==1:
                record = (route, date, daytype, rides)
            elif mode==2:
                record = {
                    'route': route,
                    'date': date,
                    'daytype': daytype,
                    'rides': rides,
                }
            elif mode==3:
                record = Record(route, date, daytype, rides)
            elif mode==4:
                record = RecordSlots(route, date, daytype, rides)
            elif mode==5:
                record = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])

            records.append(record)

    return records

if __name__ == '__main__':

    import tracemalloc

    for i in range(1,6):
   
        tracemalloc.start()
        
        rows = read_rides('././Data/ctabus.csv',i)

        current, peak = tracemalloc.get_traced_memory()

        print('Method %d - Memory Use: Current %d, Peak %d' % (i,current,peak))
        
        tracemalloc.stop()