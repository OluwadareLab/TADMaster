#! /usr/bin/python3
# Obtain max insulation value for tadtool di or insulation score
import sys

if len(sys.argv) < 2:
    print("Usage: python preprocessInsulation.py <input_path>")
    sys.exit()
else:
    input_path = sys.argv[1]
max_val = 0
with open(input_path, 'r') as f:
    data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]
for line in data:
    if float(line[4]) > float(max_val):
        max_val = line[4]
print(max_val)
