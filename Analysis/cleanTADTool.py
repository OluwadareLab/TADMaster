#! /usr/bin/python3
# Reformats TADTool bed files
import sys

if len(sys.argv) < 4:
	print("Usage: python cleanTAD.py <input_path> <out_path> <name>")
	sys.exit()
else:
	input_path = sys.argv[1]
	temp_path = sys.argv[2]
	name = sys.argv[3]

	
with open(input_path, 'r') as f:
	data = [x.rstrip('\n\t').split('\t') for x in f.readlines()]

with open(temp_path + '/' +name+'.bed', 'w+') as f:
	for line in data:
		f.write('{},{}\n'.format(line[1], line[2]))