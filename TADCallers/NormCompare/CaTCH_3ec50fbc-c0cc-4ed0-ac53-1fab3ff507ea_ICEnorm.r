library(CaTCH)
input <- "/storage/store/TADMaster/data/job_3ec50fbc-c0cc-4ed0-ac53-1fab3ff507ea/temp_ICEnorm/CaTCH.bed"
options(max.print = .Machine$integer.max)
sink("/storage/store/TADMaster/data/job_3ec50fbc-c0cc-4ed0-ac53-1fab3ff507ea/temp_ICEnorm/CaTCH_results_raw.bed")
domain.call(input)
