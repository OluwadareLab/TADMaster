library(CaTCH)
input <- "/storage/store/TADMaster/data/job_00f03b6b-ad48-4c1d-a96e-28bca77d2c47/temp/CaTCH.bed"
options(max.print = .Machine$integer.max)
sink("/storage/store/TADMaster/data/job_00f03b6b-ad48-4c1d-a96e-28bca77d2c47/temp/CaTCH_results_raw.bed")
domain.call(input)
