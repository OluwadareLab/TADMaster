#! /usr/bin/python3
# this converts the Arrowhead output to match the rest, including splitting chromosomes
import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python convertArrowhead.py <absolute_file_path>")
    sys.exit()
else:
    path = sys.argv[1]

with open(path, 'r') as f:
	tad_list = f.readlines()
	# delete headers
	del tad_list[0]
	del tad_list[0]
	chromo_list = []
	tads = []
	# get a list of the chromosome represented in the output file
	for line in tad_list:
		tad = re.split(r'\t+', str(line))
		tads.append(tad)
		if tad[0] not in chromo_list:
			chromo_list.append(tad[0])
	
	# write the bounds for each chromosome to its own file
	for chromo in chromo_list:
		chromo_tads = []
		for tad in tads:
			if tad[0] == chromo:
				chromo_tads.append(tad[1] + "-" + tad[2])
		chromo_tads.sort()
		with open(path[:-4] + '.' + chromo + '.bed', 'w') as f:
			for tad in chromo_tads:
				f.write('%s\n' % tad)