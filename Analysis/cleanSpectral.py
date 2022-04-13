#! /usr/bin/python3
# this converts the matrix into the input for CaTCH
import sys

if len(sys.argv) < 3:
    print("Usage: python cleanSpectral.py <input_path> <out_path> ")
    sys.exit()
else:
    input_path = sys.argv[1]
    out_path = sys.argv[2]


with open(input_path, 'r') as f:
    data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]

with open(out_path + '/Spectral.bed', 'w+') as f:
    for line in data:
        f.write('{},{}\n'.format(line[1].replace(" ", ""), line[2].replace(" ", "")))