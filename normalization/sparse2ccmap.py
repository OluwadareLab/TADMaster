#importing gcMapExplorer 
from gcMapExplorer import lib as gmlib
import sys

#
# sys.argv[1] is the directory of the input file
#
input = sys.argv[1]

##takes the temp file and conerts to ccmap to use
ccmap = gmlib.importer.CooMatrixHandler(inputFiles = input)

#outputting to temp_path
output = sys.argv[2] + "/exCCMap.ccmap"

#saving file
ccmap.save_ccmaps(outputFiles = output, xlabels=" ", ylabels=" ", compress=False)
