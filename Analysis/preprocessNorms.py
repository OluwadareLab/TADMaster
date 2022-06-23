#! /usr/bin/python3
# this converts the matrix into the input for normalizations
import sys

if len(sys.argv) < 4:
	print("Usage: python preprocessNorms.py <input_path> <temp_path> <resolution>")
	sys.exit()
else:
	input_path = sys.argv[1]
	# the output path should be temp_path/Norms, because they take a directory as input
	temp_path = sys.argv[2]
	res = int(sys.argv[3])
	
with open(input_path, 'r') as f:
	# reads a tab seperated matrix as a 2D array
	data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]
with open(temp_path + '/NormSparse.txt', 'w+') as f:
	# write half the symmetric matrix in sparse format
	for x in range(len(data)):
		for y in range(0, x + 1):
			f.write('{}\t{}\t{}\n'.format(y * res, x * res, data[x][y]))