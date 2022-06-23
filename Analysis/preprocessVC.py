#! /usr/bin/python3
# this converts the matrix into the input for vanilla normalization
import sys

if len(sys.argv) < 4:
	print("Usage: python preprocessVC.py <input_path> <output_path> <resolution>")
	sys.exit()
else:
	input_path = sys.argv[1]
	output_path = sys.argv[2]
	res = int(sys.argv[3])
	
with open(input_path, 'r') as f:
	data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]
with open(output_path + '/VCSparse.bed', 'w') as f:
	for x in range(len(data)):
		for y in range(0, x + 1):
			f.write('{}\t{}\t{}\n'.format((x * res) + 1, (y * res) + 1, data[x][y]))