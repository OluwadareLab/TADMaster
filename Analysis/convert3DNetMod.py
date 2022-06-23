#! /usr/bin/python3
# this converts the 3DNetMod output to match the rest
import sys
import re

if len(sys.argv) < 2:
    print("Usage: python convert3DNetMod.py <absolute_file_path>")
    sys.exit()
else:
    path = sys.argv[1]
	
# read tads from the 3DNetMod output and sort them
with open(path, 'r') as f:
	tad_list = f.readlines()
	tads = []
	for line in tad_list:
		tad = re.split(r'\t+', str(line))
		tad[2] = tad[2].strip(' \n')
		tads.append(tad[1] + "-" + tad[2])
	tads.sort()

# write the output back
with open(path, 'w') as f:
	for tad in tads:
		f.write('%s\n' % tad)