args = commandArgs(trailingOnly=TRUE)
library(HiCcompare)

#reading in table
matrix2convert <- read.table(args[1])
#converting to full matrix
full.mat <- sparse2full(matrix2convert)
matrixOut<-paste(args[2], "/Raw.txt", sep = "")
#writing the file with tab seperators
write.table(full.mat, matrixOut, col.names = F, row.names = F, sep = '\t')