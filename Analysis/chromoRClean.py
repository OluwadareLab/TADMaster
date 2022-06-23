#! /usr/bin/python3
# this converts the ClusterTAD output to match the rest
import sys
import re

if len(sys.argv) < 4:
    print("Usage: python convertClusterTAD.py <absolute_file_path> <resolution> <input matrix>")
    sys.exit()
else:
    path = sys.argv[1]
    resolution = sys.argv[2]
    contact_matrix = sys.argv[3]
with open (contact_matrix,'r') as f:
    data = f.readlines()

with open(path, 'r') as f:
    tad_list = f.readlines()
    tads = []
    changePoints = True
    i = 0
    while changePoints:
        i += 1
        if tad_list[i] == "$L\n":
            changePoints = False
        elif tad_list[i] != '\n':
            tads.append(tad_list[i])
    tads = tads[0].strip('\n')

    tads = re.split(r' ', str(tads))
    only_tads = []
    for tad in tads:
        if re.match('\[.*?\]', tad) is None and tad != '':
            only_tads.append(tad)
    tads = []
    for i in range(len(only_tads)):
        if i == 0:
            tads.append('0' + ',' + str(int(only_tads[i]) * int(resolution)))
        elif i != len(only_tads) - 1:
            tads.append(str(int(only_tads[i]) * int(resolution)) + ',' + str(int(only_tads[i+1]) * int(resolution)))
        else:
            tads.append(str(int(only_tads[i]) * int(resolution)) + ',' + str(len(data) * int(resolution)))


with open(path, 'w') as f:
    for tad in tads:
        f.write('%s\n' % tad)
