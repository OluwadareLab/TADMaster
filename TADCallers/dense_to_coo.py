import sys
import csv
import numpy as np
from scipy import sparse


if len(sys.argv) < 3:
	print("Usage: python dense_to_coo.py <input_path> <output_path>")
	sys.exit()
else:
	input_path = sys.argv[1]
	output_path = sys.argv[2]

#extract dense matrix from tab delimited square matrix
with open(input_path, 'r') as f:
    dense = np.genfromtxt(f, delimiter="\t")

#delete last column if nan
if np.isnan(dense[0][len(dense[0]) -1]):
	dense = np.delete(dense, len(dense[0])-1, 1)

print(dense.shape)

sparse = sparse.csr_matrix(dense)
with open(output_path, 'w') as f:
	for i, j in zip (*sparse.nonzero()):
		if i <= j:
			f.write('{}\t{}\t{}\n'.format(i, j, sparse[i,j]))
