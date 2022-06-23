# this extracts the TADs for specific RI values from the CaTCH output file
import sys, os, math

if len(sys.argv) < 5:
	print("Usage: python postprocessCaTCH.py <input_path> <RI_ranges_comma_seperated> <resolution> <output_path>")
	sys.exit()
else:
	input = sys.argv[1]
	# ranges must be 4 digits, x.xxx, comme seperated with no spaces
	ranges = sys.argv[2].split(',')
	res = int(sys.argv[3])
	output = sys.argv[4]

data = []
with open(input, 'r') as f:
	for line in f:
		data.append(line.split())
del data[0:14] # remove header lines, should now be at the start of the data
del data[-1005:] # remove TAD count lines from the end
for range in ranges:
	# only save the bins of the insulation score we're looking at, skipping any NANs
	tads = [list((line[3], line[4])) for line in data if (line[2] == range and not math.isnan(float(line[5])))]
	with open(output + '/CaTCH_' + range + '.bin', 'w+') as f:
		for tad in tads:
			f.write(str(int(tad[0]) * res) + ',' + str(int(tad[1]) * res) + '\n')
