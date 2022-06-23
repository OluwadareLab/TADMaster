#! /usr/bin/python3
# this converts the ClusterTAD output to match the rest
import sys
import re

if len(sys.argv) < 2:
	print("Usage: python convertClusterTAD.py <absolute_file_path>")
	sys.exit()
else:
	path = sys.argv[1]
	
with open(path, 'r') as f:
	tad_list = f.readlines()
	del tad_list[0]
	tads = []
	for line in tad_list:
		tad = re.split(r'\t+', str(line))
		tad[3] = tad[3].strip(' \n')
		tads.append(tad[1] + "," + tad[3])

with open(path, 'w') as f:
	for tad in tads:
		f.write('%s\n' % tad)