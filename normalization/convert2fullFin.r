#reading in args
args = commandArgs(trailingOnly=TRUE)
library(HiCcompare)

#if KR normalization performed, convert sparse to full matrix
if(args[3] == 'True')
{
	matrixIn<-paste(args[1], "/KRSparse.txt", sep = "")
	#reading in table
	matrix2convert <- read.table(matrixIn)
	#converting to full matrix
	full.mat <- sparse2full(matrix2convert)
	matrixOut<-paste(args[2], "/KRnorm.txt", sep = "")
	#writing the file with tab seperators
	write.table(full.mat, matrixOut, col.names = F, row.names = F, sep = '\t')
}

#if VC normalization performed, convert sparse to full matrix
if(args[4] == 'True')                  
{
	matrixIn<-paste(args[1], "/VCSparse.txt", sep = "")
	#reading in table
	matrix2convert <- read.table(matrixIn)
	#converting to full matrix
	full.mat <- sparse2full(matrix2convert)
	matrixOut<-paste(args[2], "/VCnorm.txt", sep = "")
	#writing the file with tab seperators
	write.table(full.mat, matrixOut, col.names = F, row.names = F, sep = '\t')
}

#if IC normalization performed, convert sparse to full matrix
if(args[5] == 'True')
{
	matrixIn<-paste(args[1], "/ICESparse.txt", sep = "")
	#reading in table
	matrix2convert <- read.table(matrixIn)
	#converting to full matrix
	full.mat <- sparse2full(matrix2convert)
	matrixOut<-paste(args[2], "/ICEnorm.txt", sep = "")
	#writing the file with tab seperators
	write.table(full.mat, matrixOut, col.names = F, row.names = F, sep = '\t')
}

#if MCFS normalization performed, convert sparse to full matrix
if(args[6] == 'True')                         
{
	matrixIn<-paste(args[1], "/MCFSSparse.txt", sep = "")                                                                                                                      
	#reading in table
	matrix2convert <- read.table(matrixIn)
	#converting to full matrix
	full.mat <- sparse2full(matrix2convert)
	matrixOut<-paste(args[2], "/MCFSnorm.txt", sep = "")
	#writing the file with tab seperators
	write.table(full.mat, matrixOut, col.names = F, row.names = F, sep = '\t')
}

#if SCN normalization called, converts to full matrix
if(args[7] == 'True')
{
	#reading in sparse matrix from args[8]
	matrix2convert <- read.table(args[8])
	#converting to full matrix
	full.mat <- sparse2full(matrix2convert)
	#performing SCN normalization
	full.mat <- SCN(full.mat)
	#output path concatenation
	outputMatrix<-paste(args[2], "/SCNnorm.txt", sep = "")
	write.table(full.mat, outputMatrix, col.names = F, row.names = F, sep = '\t')
}
