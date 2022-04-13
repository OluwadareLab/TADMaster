# this converts the .bed results from TAD callers into the input for the heatmap script
import sys

if len(sys.argv) < 5:
    print("Usage: python shift_nxn.py <input_path> <temp_path> <name> <chr> <resolution>")
    sys.exit()
else:
    input_path = sys.argv[1]
    temp_path = sys.argv[2]
    name = sys.argv[3]
    chr = sys.argv[4]
    res = int(sys.argv[5])

# read the bed file
with open(input_path, 'r') as f:
    data = f.readlines()
count = 0
# rewrite it as a bin file (bed divided by resolution)
with open(temp_path + '/' + name, 'w+') as f:
    for line in data:
        start = res * count
        end = res * (count+1)
        f.write('chr' + chr + '\t' + str(start) + '\t' + str(end) + '\t' + line)
        count += 1
