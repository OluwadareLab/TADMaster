#! /usr/bin/python3
# this converts the matrix into the input for 3DNetMod
import sys
import re

if len(sys.argv) < 5:
	print("Usage: python preprocess3DNetMod.py <absolute_file_path> <temp_path> <chr> <resolution>")
	sys.exit()
else:
	path = sys.argv[1]
	temp_path = sys.argv[2]
	chr = sys.argv[3]
	res = sys.argv[4]
	
	
# create the interaction file	
def createInteraction(path, temp_path):
	with open(path, 'r') as f:
		with open(temp_path + '/3DNetMod.inter', 'w') as g:
			tad_list = f.readlines()
			x = 0
			for line in tad_list:
				cells = line.split('\t')
				del cells[-1] # there's a newline at the end
				# side is fixing a scope issue, it's just keeping track of how long each row is
				createInteraction.side = len(cells)
				for y in range(len(cells)):
					g.write('{}\t{}\t{}\n'.format(x, y, cells[y]))
				x += 1



# run the above function, and use the side attribute to create the bed file
with open(temp_path + '/3DNetMod.inputbed', 'w') as bed:
	createInteraction(path, temp_path)
	genomic = 0
	for i in range(createInteraction.side):
		bed.write('chr{}\t{}\t{}\t{}\n'.format(chr, genomic, genomic + int(res), i))
		genomic += int(res)
