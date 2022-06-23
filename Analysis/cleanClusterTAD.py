import numpy as np

if len(sys.argv) < 4:
	print("Usage: python cleanClusterTAD.py <input_path> <resolution> <output_path>")
	sys.exit()
else:
	input_path = sys.argv[1]
	resolution = int(sys.argv[2])
	output = sys.argv[3]

with open(input_path, 'r') as file:
	bed = [[float(digit) for digit in line.split(sep='-')] for line in file]
	bed = np.asarray(bed)
	bed = bed / resolution

with open(output_path, 'w') as file
	for row in bed:
		file.write(str(row[0]) + "," + str(row[1]) + '\n')