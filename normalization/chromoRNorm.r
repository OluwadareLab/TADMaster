#obtaining file location from args
args = commandArgs(trailingOnly=TRUE)

#sourcing necesary library and function files
source("sparse2matrix.R")
source("gethicobjlist.R")
source("normchromoRfun.R")

#
#dirin1 is the directory of the input file
#dirout1 is the directory of the output normalized matrix
#species is the species name
#chr1 is the chromosome name
#args[6] is the input directory to get name of file to change
#
dirin1 <- args[1]
dirout1 <- args[2]
species1 <- args[3]
chr1 <-args[4]

#converting resolution to a numeric
resolution1 <- as.numeric(args[5]) 

#performing chromoR normalization based on figured from .config file
normchromoRfun(dirin=dirin1, dirout=dirout1, species=species1, chr=chr1, resolution=resolution1)

lf <- list.files(args[1])
filename  <- strsplit(lf, '[.]')[[1]]
finName = paste(args[2], '//', filename[1], '-chromoR.txt', sep="")
finchName = paste(args[2], '//', 'chromoRnorm.txt', sep="")
file.rename(finName, finchName)
