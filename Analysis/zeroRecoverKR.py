# this puts missing zero rows back after running KR
import sys

if len(sys.argv) < 4:
	print("Usage: python zeroRecoverKR.py <input_path_matrix> <input_path_zeros> <output_path>")
	sys.exit()
else:
	matrix_path = sys.argv[1]
	zeros_path = sys.argv[2]
	output_path = sys.argv[3]
	
data = []
zeros = []
# read the normalized matrix
with open(matrix_path, 'r') as f:
	for line in f:
		data.append(line.split())
# read the zeros
with open(zeros_path, 'r') as f:
	for line in f:
		zeros.append(line.strip('\n'))
for zero in zeros:
	# insert zeros in columns
	for line in data:
		line.insert(int(zero) - 1, 0)
		zeroRow = [0] * len(line)
	# insert row of zeros
	data.insert(int(zero) - 1,zeroRow)
# write the restored matrix back
with open(output_path, 'w+') as f:
	for line in data:
		for cell in line:
			f.write(str(cell) + '\t')
		f.write('\n')