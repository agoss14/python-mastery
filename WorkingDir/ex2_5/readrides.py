# readrides.py

import csv

from collections.abc import Sequence

#Custom container
class RideData(Sequence):
    def __init__(self):
        self.routes = []      # Columns
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    # with this, you can use istance_name[i] to get the i element of RideData instance
    def __getitem__(self, index):

        if isinstance(index, slice):
            ''' 
            Manage slicing: the aim is to return a RideData object with
            a proper number of dictionaries
            '''

            #indexes
            start, stop, step = index.start, index.stop, index.step

            if(start==None):
                start=0
            if(stop==None):
                stop=len(self)+1
            if(step==None):
                step=1
        
            sliced_ridedata = RideData()

            for i in range(start,stop,step):
                sliced_ridedata.append(self[i])

            return sliced_ridedata

        return { 'route': self.routes[index],
                 'date': self.dates[index],
                 'daytype': self.daytypes[index],
                 'rides': self.numrides[index] }

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

def read_rides(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()      # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                'route': route, 
                'date': date, 
                'daytype': daytype, 
                'rides' : rides
                }
            records.append(record)
    return records

if __name__ == '__main__':

    import tracemalloc

    tracemalloc.start()
        
    rows = read_rides('././Data/ctabus.csv')

    current, peak = tracemalloc.get_traced_memory()

    print('Memory Use: Current %d, Peak %d' % (current,peak))
    
    tracemalloc.stop()