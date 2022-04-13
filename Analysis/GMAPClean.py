#! /usr/bin/python3
# this converts the ClusterTAD output to match the rest
import sys
import re

if len(sys.argv) < 2:
    print("Usage: python HiCsegClean.py <absolute_file_path>")
    sys.exit()
else:
    path = sys.argv[1]

with open(path, 'r') as f:
    tad_list = f.readlines()
    tads = []
    changePoints = True
    i = 1
    while changePoints:
        i += 1
        if re.match('[ \t]+'+'start'+'[ \t]+'+'end\n', tad_list[i]):
            changePoints = False
        elif tad_list[i] != '\n':
            tads.append(tad_list[i])

    temp = []
    for line in tads:
        temp.append(line.strip('\n'))

    tads = []
    for line in temp:
        tads.append(re.split(r' ', str(line)))
    only_tads = []

    for line in tads:
        hold = []
        for tad in line:
            if tad != '':
                hold.append(tad)
        only_tads.append(hold)

    tads = []
    for line in only_tads:
        tads.append(line[1] +','+line[2])

with open(path, 'w') as f:
    for tad in tads:
        f.write('%s\n' % tad)
