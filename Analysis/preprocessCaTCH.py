#! /usr/bin/python3
# this converts the matrix into the input for CaTCH
import sys

if len(sys.argv) < 4:
	print("Usage: python preprocessCaTCH.py <input_path> <temp_path> <chromosome number>")
	sys.exit()
else:
	input_path = sys.argv[1]
	temp_path = sys.argv[2]
	chr = int(sys.argv[3])
	
with open(input_path, 'r') as f:
	data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]
with open(temp_path + '/CaTCH.bed', 'w') as f:
	for x in range(len(data)):
		for y in range(len(data)):
			f.write('{} {} {} {:.4f}\n'.format(chr, x, y, float(data[x][y])))