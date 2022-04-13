args = commandArgs(trailingOnly=TRUE)
library(HiCcompare)
options(scipen = 999)
matrix<-as.matrix(read.table(args[1]))
size<-ncol(matrix)
names<-0:(size-1)
names<-names * as.integer(args[2])
colnames(matrix)<-names
sparse<-full2sparse(matrix)
write.table(sparse, file=args[3], row.names=FALSE, col.names=FALSE)