lf <- list.files(args[1])
filename  <- strsplit(lf, '[.]')[[1]]
finName = paste(args[2], filename[1], '-chromoR.txt', sep="")
finchName = paste(args[2], 'chromoRnorm.txt', sep="")
file.rename(finName, finchName)
