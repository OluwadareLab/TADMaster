# this converts the .bed results from TAD callers into the input for the heatmap script
import os, sys

if len(sys.argv) < 5:
    print("Usage: python bedToBin.py <input_path> <temp_path> <name> <resolution>")
    sys.exit()
else:
	input_path = sys.argv[1]
	temp_path = sys.argv[2]
	name = sys.argv[3]
	res = int(sys.argv[4])
	
# read the bed file
with open(input_path, 'r') as f:
	data = [x.rstrip('\n\t').split('-') for x in f.readlines()]
# rewrite it as a bin file (bed divided by resolution)
with open(temp_path + '/' + name + '.bin', 'w+') as f:
	for tad in data:
		print(tad[0])
		f.write(str(int(tad[0]) / res) + ',' + str(int(tad[1]) / res) + '\n')
	
