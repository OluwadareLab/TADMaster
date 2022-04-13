source("/home/lzephyr/TADMaster/scripts/Analysis/KR_Normalization.R")
input <- as.matrix(read.table(file="/home/lzephyr/TADMaster/jobs/normTest/input/uij.chr19"))
output <- "/home/lzephyr/TADMaster/jobs/normTest/temp/KR.bed"
output_zeros <- "/home/lzephyr/TADMaster/jobs/normTest/temp/KR_zeros.bed"
options(max.print = .Machine$integer.max)
KRnorm(input)
