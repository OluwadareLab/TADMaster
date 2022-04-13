#! /usr/bin/python3
# Check bed files for errors
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python check_bed_error.py <input_path> ")
    sys.exit()
else:
    input_path = sys.argv[1]

empty = False
error = 0
if not os.path.exists(input_path):
    print('file not found')
    error = 1
else:
    if os.stat(input_path).st_size ==0:
        print('bed empty')
        empty = True
        error = 1
        os.remove(input_path)
    if not empty:
        with open(input_path, 'r') as f:
            data = f.readlines()
            for line in data:
                test_list = line.split(',')
                try:
                    numbers = [int(x.strip()) for x in test_list]
                except:
                    print('bed format error')
                    error = 1
                    os.remove(input_path)
                    break
    if error == 0:
        print('no errors with bed')