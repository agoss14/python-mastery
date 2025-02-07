# simple_pipeline.py

from follow import follow
import csv
import os

file_path = os.path.abspath('Data/stocklog.csv')
print('Absolute path of the file: ',file_path)

# PRODUCER
lines = follow(file_path)

# PROCESSING
rows = csv.reader(lines)

# CONSUMER
print('Only one time printed because it\'s not in a loop!')
for row in rows:
    print(row)