
import sys
# print(sys.path)
sys.path.append('c:\\Users\\agost\\git_projects\\python-mastery\\WorkingDir\\ex2_1')

import tracemalloc
from pprint import pprint
import readrides
import csv


tracemalloc.start()

rows = readrides.read_rides('Data/ctabus.csv',2)
rt22 = [row for row in rows if row['route'] == '22']
print(max(rt22, key=lambda row: row['rides']))

current, peak = tracemalloc.get_traced_memory()

print('Method 1 - Memory Use: Current %d, Peak %d' % (current,peak))

tracemalloc.stop()

##############################################################################

tracemalloc.start()

f = open('Data/ctabus.csv')

f_csv = csv.reader(f)
headers = next(f_csv)

rows = (dict(zip(headers,row)) for row in f_csv)

rt22 = (row for row in rows if row['route'] == '22')

print(max(rt22, key=lambda row: int(row['rides'])))

current, peak = tracemalloc.get_traced_memory()

print('Method 2 - Memory Use: Current %d, Peak %d' % (current,peak))

tracemalloc.stop()