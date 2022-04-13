#! /usr/bin/python3
# this converts the matrix into the input for TopDom
import sys

if len(sys.argv) < 6:
	print("Usage: python preprocessTopDom.py <input_path> <cooler_path> <chr> <resolution> <job_id>")
	sys.exit()
else:
	input_path = sys.argv[1]
	cooler_path = sys.argv[2]
	chr = sys.argv[3]
	res = int(sys.argv[4])
	id = sys.argv[5]
	
with open(input_path, 'r') as f:
	data = f.readlines()
with open(cooler_path + 'cool' + '.bed', 'w') as f:
	bin = 0
	for line in data:
		f.write('{}\t{}\t{}\n'.format(chr, bin, bin + res))
		bin += res