import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


if len(sys.argv) < 3:
	print("Usage: python normConcordance.py <directory_path> <output_path>")
	sys.exit()
else:
	path = sys.argv[1]
	res = sys.argv[2]