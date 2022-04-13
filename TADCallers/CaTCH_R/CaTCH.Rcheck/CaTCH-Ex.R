pkgname <- "CaTCH"
source(file.path(R.home("share"), "R", "examples-header.R"))
options(warn = 1)
library('CaTCH')

base::assign(".oldSearch", base::search(), pos = 'CheckExEnv')
base::assign(".old_wd", base::getwd(), pos = 'CheckExEnv')
cleanEx()
nameEx("domain.call")
### * domain.call

flush(stderr()); flush(stdout())

### Name: domain.call
### Title: Call a hierarchy of domains based on Hi-C data
### Aliases: domain.call domain.call.parallel
### Keywords: TADs hierarchy

### ** Examples

#R code to be here
	fileinput=system.file("Test.dat.gz",package="CaTCH")
	library(CaTCH)
	domain.call(fileinput)



### * <FOOTER>
###
cleanEx()
options(digits = 7L)
base::cat("Time elapsed: ", proc.time() - base::get("ptime", pos = 'CheckExEnv'),"\n")
grDevices::dev.off()
###
### Local variables: ***
### mode: outline-minor ***
### outline-regexp: "\\(> \\)?### [*]+" ***
### End: ***
quit('no')
