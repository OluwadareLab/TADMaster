#using args through sys, importing libraries gcMapExplorer
import sys
from gcMapExplorer import lib as gmlib

#
#input: ccmap file location and booleans whether to process normalizations
#sys.argv[1] = input ccmap file path in temp folder
#sys.argv[2] = process KR? T:F
#sys.argv[3] = process VC? T:F
#sys.argv[4] = process IC? T:F
#sys.argv[5] = process MCFS? T:F
#output: Sparse matrices derived from ccmap
#

#
#checking args for if info was processed, if so then process file conversion
#
if (sys.argv[2] == 'True'):
	input = sys.argv[1] + "/KRoutput.ccmap"
	output = sys.argv[1] + "/KRSparse.txt"
	#importing ccmap file
	ccmap1 = gmlib.ccmap.load_ccmap(input)
	#converting to sparse matrix
	gmlib.ccmap.export_cmap(ccmap1, output, doNotWriteZeros=True)

if (sys.argv[3] == 'True'):
	input = sys.argv[1] + "/VCoutput.ccmap"
	output = sys.argv[1] + "/VCSparse.txt"
	#importing ccmap file
	ccmap2 = gmlib.ccmap.load_ccmap(input)
	#converting to sparse matrix
	gmlib.ccmap.export_cmap(ccmap2, output, doNotWriteZeros=True)

if (sys.argv[4] == 'True'):
	input = sys.argv[1] + "/ICEoutput.ccmap"
	output = sys.argv[1] + "/ICESparse.txt"
	#importing ccmap file
	ccmap3 = gmlib.ccmap.load_ccmap(input)
	#converting to sparse matrix
	gmlib.ccmap.export_cmap(ccmap3, output, doNotWriteZeros=True)
	
if (sys.argv[5] == 'True'):
	input = sys.argv[1] + "/MCFSoutput.ccmap"
	output = sys.argv[1] + "/MCFSSparse.txt"
	#importing ccmap file
	ccmap4 = gmlib.ccmap.load_ccmap(input)
	#converting to sparse matrix
	gmlib.ccmap.export_cmap(ccmap4, output, doNotWriteZeros=True)
