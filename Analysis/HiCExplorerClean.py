import sys


if len(sys.argv) < 4:
    print("Usage: python HiCExplorerClean.py <Domain_bed_path> <resolution> <output_path>")
    sys.exit()
else:
    input_bed = sys.argv[1]
    resolution = int(sys.argv[2])
    output = sys.argv[3]

data = []
with open(input_bed, 'r') as f:
    for line in f:
        data.append(line.split())
with open(output, 'w') as f:
    for line in data:
        f.write(str(line[1]) + ", " + str(line[2]) + "\n")
