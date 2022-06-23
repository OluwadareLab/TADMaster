#! /usr/bin/python3
# this converts the ClusterTAD output to match the rest
import sys
import re

if len(sys.argv) < 3:
    print("Usage: python convertClusterTAD.py <absolute_file_path> <resolution>")
    sys.exit()
else:
    path = sys.argv[1]
    resolution = sys.argv[2]


with open(path, 'r') as f:
    tad_list = f.readlines()
    tads = []
    for line in tad_list:
        tad = re.split(r'\t', str(line))
        tad[1] = tad[1].strip(' \n')
        tad[0] = int(tad[0]) * int(resolution)
        tad[1] = int(tad[1]) * int(resolution)
        tads.append(str(tad[0]) + "," + str(tad[1]))
    print(tads)

with open(path, 'w') as f:
    for tad in tads:
        f.write('%s\n' % tad)
