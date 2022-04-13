#! /usr/bin/python3
# this creates the plots for TAD analysis
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


if len(sys.argv) < 3:
	print("Usage: python plots.py <directory_path> <resolution>")
	sys.exit()
else:
	path = sys.argv[1]
	res = sys.argv[2]
	
	
# colors
all_colors = {
'color_3dnetmod': '#EEEEEE',
'color_armatus': '#DF0707',
'color_clustertad': '#AAFE21',
'color_di': '#63E925',
'color_spectral': '#F835FB'}

# runs one tolerance value of shared bounds
def sharedBounds(all_bounds, name, ref_start, ref_end, tolerance):
	total_shared = []
	for i in range(tolerance):
		shared = 0
		unique = 0
		comp_start = [all_bounds[name][x][0] for x in range(len(all_bounds[name]))]
		comp_end = [all_bounds[name][x][1] for x in range(len(all_bounds[name]))]
		for j, k in zip(ref_start, ref_end):
			if i > 0:
				bin_range_start = range(int(j) - i, int(j) + i + 1)
				bin_range_end = range(int(k) - i, int(k) + i + 1)
				if any(x in comp_start for x in bin_range_start):
					for bin in comp_start:
						if bin in bin_range_start:
							comp_start.remove(bin)
							break
					shared += 1
				else:
					unique += 1
				if any(x in comp_end for x in bin_range_end):
					for bin in comp_end:
						if bin in bin_range_end:
							comp_end.remove(bin)
							break
					shared += 1
				else:
					unique += 1
			else:
				bin_range_start = int(j)
				bin_range_end = int(k)
				if bin_range_start in comp_start:
					index = comp_start.index(bin_range_start)
					del comp_start[index]
					shared += 1
				else:
					unique += 1
				if bin_range_end in comp_end:
					index = comp_end.index(bin_range_end)
					del comp_end[index]
					shared += 1
				else:
					unique += 1
		total_shared.append(shared)
	return total_shared
	
	
# count the TADs in each file
tad_count = {}
tad_size_total = {}
boundaries = {}
for file in os.listdir(path):
	if file.endswith('.bed'):
		with open(os.path.join(path, file), 'r') as f:
			tad_list = f.readlines()
			tads = []
			tad_size = []
			# save the size of each TAD
			for i in range(len(tad_list)):
				tads.append(tad_list[i].strip(' \n').split('-'))
				tads[-1][0] = (int(tads[-1][0]) / int(res))
				tads[-1][1] = (int(tads[-1][1]) / int(res))
				tad_size.append(int(tads[-1][1] - tads[-1][0]))	
			# strip the file extension and save which method these results were from
			tad_key = file[:-4]
			tad_size_total[tad_key] = tad_size
			# count the TADs
			tad_count[tad_key] = len(tad_list)
			boundaries[tad_key] = tads

# sort the data
names = []
for i in tad_count.keys():
	names.append(i)
names.sort()
count = []
size = []
colors = []
for name in names:
	count.append(tad_count[name])
	size.append(tad_size_total[name])
	colors.append(all_colors['color_' + str(name.lower())])
	
# count and size should now contain the data sorted alphabetically by method name
fig, (ax1, ax2) = plt.subplots(2)
fig.set_size_inches(16, 9)

# subplot for number of TADs
ax1.barh(names, count, align='center', alpha=0.5, color=colors, edgecolor=colors)
ax1.set_ylabel('TAD algorithms', fontweight='bold')
ax1.set_title('Number of TADs', fontweight='bold')
barXTicks = np.linspace(0, max(count), 10)
for i, j in zip(barXTicks, range(10)):
	barXTicks[j] = int(i)
ax1.set_xticks(barXTicks)
ax1.invert_yaxis()
for i, v in enumerate(count):
	ax1.text(v + .5, i, str(v), va='center', fontweight='bold')
	
# subplot for size of TADs
bp = ax2.boxplot(size, vert=False, showfliers=False, patch_artist=True)
ax2.set_ylabel('TAD algorithms', fontweight='bold')
ax2.set_title('Size of TADs (resolution: ' + res + ')', fontweight='bold')
ax2.set_yticklabels(names)
ax2.invert_yaxis()
for patch, color in zip(bp['boxes'], colors):
	patch.set_facecolor(color)

# save the plot
plt.savefig(path + 'plots.jpg')
plt.clf()

# subplot for shared boundries, one file created per method
for name in names:
	# defines number of ticks and overall size of graph
	tolerance = 9
	barWidth = .25
	ind = np.arange(float(tolerance))
	ref_start = [boundaries[name][x][0] for x in range(len(boundaries[name]))]
	ref_end = [boundaries[name][x][1] for x in range(len(boundaries[name]))]
	ax = plt.subplot(111)
	for i, j in zip(names, range(len(names))):
		if i != name:
			shared = sharedBounds(boundaries, i, ref_start, ref_end, tolerance)
			print(shared)
			ax.bar(ind, shared, color=colors[j], width=barWidth, edgecolor='white', label=i)
			ind += barWidth
	plt.xlabel('Bin Tolerance', fontweight='bold')
	plt.ylabel('Number of shared boundaries', fontweight='bold')
	ax.set_title('Shared boundaries: ' + name, fontweight='bold')
	ax.set_xticks(np.arange(float(tolerance)))
	ax.set_xticklabels(list(str(x) + ' bins' for x in range(tolerance)))
	plt.legend()
	plt.savefig(name + '_shared.jpg')
	plt.clf()

