source	TADMaster.config				    			# change path to config file
echo "Running TADMaster on $input_matrix"

#--------------------------------------------------------------------------------------------------------
#Make paths
#--------------------------------------------------------------------------------------------------------

normalized_input="$1"
norm_name=$(basename $normalized_input .txt)

home_path="${PWD}"											# change home_path
Caller_path="${home_path}/TADCallers"
Norm_method_path="${home_path}/normalization" 
job_path="${PWD}/example_job_output"      						# change output_path                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
input_path="${input_matrix}"
output_path="${job_path}/output"
temp_path="${job_path}/temp_${norm_name}"
additional_file_path="${job_path}/additional_files"
normalized_path="${job_path}/normalizations"
log_path="${job_path}/log_${norm_name}.txt"

mkdir $temp_path
touch $log_path
#--------------------------------------------------------------------------------------------------------
#Enter caller methods
#--------------------------------------------------------------------------------------------------------


if [ $data_input_type == 'cool' ]
then
	cool_or_h5_path="${input_matrix}"
fi

if [ $data_input_type == 'hic' ]
then
	hic_path="${input_matrix}"
fi

if [ $data_input_type == 'h5' ]
then
	cool_or_h5_path="${input_matrix}"
fi

input_path="$normalized_input"
output_path="${job_path}/output/$norm_name/"
mkdir $output_path

#CleanUp and remake

echo "${input_path}" >> $log_path
echo "Processing ${norm_name}" >> $log_path

#Armatus
if [ $armatus == 'True' ]
then
	printf 'Entering Armatus\n-----------------\n'
	echo "Entering Armatus" >> $log_path
	date >> $log_path 
	cd $Caller_path
	cd armatus-2.2
	gzip -k $input_path
	armatus_input="${input_path}.gz"
	./armatus-linux-x64 -i $armatus_input -g $armatus_gamma -o $temp_path/test_${norm_name} -r $resolution -s 0.025
	python3 $home_path/Analysis/cleanArmatus.py $temp_path/test_${norm_name}.consensus.txt $output_path
	rm -rf $armatus_input
	cd $home_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/Armatus.bed >> $log_path
	echo "Exiting Armatus" >> $log_path
	date >> $log_path 
fi

# Arrowhead
if [ $arrowhead == 'True' ] && [ $data_input_type == 'hic' ]
then
	echo "Entering Arrowhead" >> $log_path
	date >> $log_path 

	if [ $norm_name == 'VCnorm' ]
	then
		arrowhead_norm='VC'
	elif [ $norm_name == 'KRnorm' ]
	then
		arrowhead_norm='KR'
	elif [ $norm_name == 'Raw' ]
	then	
		arrowhead_norm='NONE'
	fi
	printf 'Entering Arrowhead\n-----------------\n'
	cd $Caller_path/Juicer/scripts
	 java -jar juicer_tools_1.22.01.jar arrowhead -c $chr  -r $resolution --threads 0 -k arrowhead_norm $hic_path $additional_file_path/Arrowhead.bed --ignore-sparsity
	cd $home_path
	echo "Exiting Arrowhead" >> $log_path
	date >> $log_path 
fi


# CaTCH
# Currently Disabled
if [ $catch == 'Skip' ]
then
	printf 'Entering CaTCH\n-----------------\n'
	echo "Entering CaTCH" >> $log_path
	date >> $log_path 

	cd $Caller_path/CaTCH_R
	python3 $home_path/Analysis/preprocessCaTCH.py $input_path $temp_path $chr
	catch_path=${Caller_path}/NormCompare/CaTCH_${job_id}_${norm_name}.r
	echo "library(CaTCH)" > $catch_path
	echo "input <- \"${temp_path}/CaTCH.bed\"" >> $catch_path
	# without this line, most of the results won't output
	echo "options(max.print = .Machine\$integer.max)" >> $catch_path
	echo "sink(\"${temp_path}/CaTCH_results_raw.bed\")" >> $catch_path
	echo "domain.call(input)" >> $catch_path
	chmod 777 "${catch_path}"
	 dos2unix $catch_path
	 Rscript "${catch_path}"
	 python3 $home_path/Analysis/postprocessCaTCH.py $temp_path/CaTCH_results_raw.bed 0.650,0.550 $resolution $output_path 
	rm -rf ${Caller_path}/NormCompare/CaTCH_${job_id}_${norm_name}.r
	cd $home_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/CaTCH_0.650.bin >> $log_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/CaTCH_0.550.bin >> $log_path
	echo "Exiting CaTCH" >> $log_path
	date >> $log_path 
fi


# ClusterTAD IS DISABLED IN PARALLEL DUE TO LONG RUN TIMES
if [ $clustertad == 'Skip' ]
then
	cd $temp_path
	cp $Caller_path/ClusterTAD.jar $temp_path/ClusterTAD.jar
	printf 'Entering ClusterTAD\n-----------------\n'
	echo "Entering ClusterTAD" >> $log_path
	date >> $log_path 

	 java -jar ClusterTAD.jar $input_path $resolution
	# move the best result to the output folder
	# Currently leaves all other in a file in TADCallers!!!!
	shopt -s nullglob
	for d in Output_*/ ; do
		for f in $d/TADs/BestTAD_* ; do
			mv $f "${output_path}/ClusterTAD.bed"
		done
	done
	mv Output_* "${additional_file_path}/Cluster"
	# convert ClusterTAD results
	 python3 $home_path/Analysis/convertClusterTAD.py $output_path/ClusterTAD.bed
	 python3 $home_path/Analysis/check_bed_error.py $output_path/ClusterTAD.bed >> $log_path
	echo "Exiting ClusterTAD" >> $log_path
	date >> $log_path 
fi


# TopDom
if [ $topdom == 'True' ]
then
	cd $Caller_path/TopDom
	printf 'Entering TopDom\n-----------------\n'
	echo "Entering TopDom" >> $log_path
	date >> $log_path 

	#NxN to NxN+3 format
	 python3 preprocessTopDom.py $input_path $temp_path/ $chr $resolution $job_id
	#set up driver code
	topdom_path=${temp_path}/Topdom_${job_id}_${norm_name}.r
	echo "setwd(\"${Caller_path}/TopDom/\")" > $topdom_path
	echo "source(\"TopDom.R\")" >> $topdom_path
	echo "TopDom(matrix.file=\"${temp_path}/TopDom_${job_id}.bed\", window.size=${topdom_window}, outFile=\"${output_path}/TopDom\")" >> $topdom_path
	#Run topdom
	 Rscript "${topdom_path}"
	rm -rf ${output_path}/TopDom.domain
	rm -rf ${output_path}/TopDom.binSignal
	 python3 $home_path/Analysis/cleanTopDom.py $output_path/TopDom.bed $output_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/TopDom.bed >> $log_path
	cd $home_path
	echo "Exiting TopDom" >> $log_path
	date >> $log_path 
fi


#GMAP
if [ $gmap == 'True' ]
then
	cd $Caller_path
	gmap_path=GMAP_${job_id}_${norm_name}.r
	printf 'Entering GMAP\n-----------------\n'
	echo "Entering GMAP" >> $log_path
	date >> $log_path 

	echo "library(rGMAP)" > $gmap_path
	echo "res = rGMAP(\"${input_path}\", resl = $resolution)" >> $gmap_path
	echo "sink(\"${output_path}/GMAP.txt\")" >> $gmap_path
	echo "print(res)" >> $gmap_path
	echo "sink()" >> $gmap_path
	 Rscript "${gmap_path}"
	rm -rf GMAP_${job_id}_${norm_name}.r
	 python3 $home_path/Analysis/GMAPClean.py $output_path/GMAP.txt
	 python3 $home_path/Analysis/check_bed_error.py $output_path/GMAP.txt >> $log_path
	echo "Exiting GMAP" >> $log_path
	date >> $log_path 
fi

#IC-Finder
if [ $ic_finder == 'True' ]
then
	printf 'Entering IC-Finder\n-----------------\n'
	echo "Entering IC-Finder" >> $log_path
	date >> $log_path 

	cd $Caller_path/IC-Finder
	path=ic-finder_${job_id}_${norm_name}.m
	{
	echo "pkg load statistics;"
	echo "dom = IC_Finder('${input_path}','Option','hierarchy','SigmaZero',5, 'SaveFigures',0, 'path', '${output_path}/');"
	}> $path
	 octave --no-gui "${path}"
	rm -rf ic-finder_${job_id}_${norm_name}.m
	 python3 $home_path/Analysis/IC-FinderClean.py $output_path/${norm_name}_sigmaZero5_domains.txt $resolution
	mv $output_path/${norm_name}_sigmaZero5_domains.txt $output_path/IC_Finder.txt
	 python3 $home_path/Analysis/check_bed_error.py $output_path/IC_Finder.txt >> $log_path 
	echo "Exiting IC-Finder" >> $log_path
	date >> $log_path 
fi

#HiCseg
if [ $hic_seg == 'True' ]
then
	cd $Caller_path
	printf 'Entering HiCseg\n-----------------\n'
	echo "Entering HiCseg" >> $log_path
	date >> $log_path 

	path=HiCseg_${job_id}_${norm_name}.r
	echo "library(HiCseg)" > $path
	echo "options(max.print=1000000)" >> $path
	echo "matrix <- read.table(\"${input_path}\", sep = \"\t\")" >> $path
	echo "hold <- matrix[,colSums(is.na(matrix))<nrow(matrix)]" >> $path
	echo "df <- as.numeric(unlist(hold))" >> $path
	echo "sink(\"${output_path}/HiCseg.txt\")" >> $path
	echo "HiCseg_linkC_R(length(hold), 1000, \"G\", df, \"D\")" >> $path
	echo "sink()" >> $path
	 Rscript "${path}"
	rm -rf HiCseg_${job_id}_${norm_name}.r
	 python3 $home_path/Analysis/HiCsegClean.py $output_path/HiCseg.txt $resolution $input_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/HiCseg.txt >> $log_path
	echo "Exiting HiCseg" >> $log_path
	date >> $log_path 
fi


#Insulation
if [ $insulation == 'True' ]
then
	cd $Caller_path
	printf 'Entering insulation\n-----------------\n'
	echo "Entering insulation" >> $log_path
	date >> $log_path 

	 python3 tadtool_bed.py $input_path $temp_path/ insulation $chr $resolution
	window_size=$(($resolution*50))
	 tadtool tads $input_path ${temp_path}/insulation.bin $window_size 2 $temp_path/insulation.values -v
	max_val=$(python3 $home_path/Analysis/tadtool_value.py $temp_path/insulation.values)
	
	cut_off=$(echo ".4*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/insulation.bin $window_size $cut_off $temp_path/insulation.results
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/insulation.results $output_path Insulation_Score_40
	 python3 $home_path/Analysis/check_bed_error.py $output_path/Insulation_Score_40.bed >> $log_path
	
	cut_off=$(echo ".5*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/insulation.bin $window_size $cut_off $temp_path/insulation.results
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/insulation.results $output_path Insulation_Score_50
	 python3 $home_path/Analysis/check_bed_error.py $output_path/Insulation_Score_40.bed >> $log_path

	
	cut_off=$(echo ".6*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/insulation.bin $window_size $cut_off $temp_path/insulation.results
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/insulation.results $output_path Insulation_Score_60
	 python3 $home_path/Analysis/check_bed_error.py $output_path/Insulation_Score_60.bed >> $log_path

	echo "Exiting insulation" >> $log_path
	date >> $log_path 
fi

#DI
if [ $di == 'True' ]
then
	cd $Caller_path
	printf 'Entering DI\n-----------------\n'
	echo "Entering DI" >> $log_path
	date >> $log_path 

	 python3 tadtool_bed.py $input_path $temp_path di $chr $resolution 
	window_size=$(($resolution*50))
	 tadtool tads $input_path ${temp_path}/di.bin $window_size 2 $temp_path/di.values -a directionality -v
	max_val=$(python3 $home_path/Analysis/tadtool_value.py $temp_path/di.values)
	
	cut_off=$(echo ".4*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/di.bin $window_size $cut_off $temp_path/di.results -a directionality
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/di.results $output_path DI_40
	 python3 $home_path/Analysis/check_bed_error.py $output_path/DI_40.bed >> $log_path

	cut_off=$(echo ".5*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/di.bin $window_size $cut_off $temp_path/di.results -a directionality
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/di.results $output_path DI_50
	 python3 $home_path/Analysis/check_bed_error.py $output_path/DI_50.bed >> $log_path
	
	cut_off=$(echo ".6*$max_val"|bc)
	 tadtool tads $input_path ${temp_path}/di.bin $window_size $cut_off $temp_path/di.results -a directionality
	 python3 $home_path/Analysis/cleanTADTool.py  $temp_path/di.results $output_path DI_60
	 python3 $home_path/Analysis/check_bed_error.py $output_path/DI_60.bed >> $log_path

	echo "Exiting DI" >> $log_path
	date >> $log_path 
fi

#HiCExplorer
if [ $hic_explorer == 'True' ] && [ $data_input_type != 'sparse' ] && [ $data_input_type != 'square' ]
then
	printf 'Entering HiCExplorer\n-----------------\n'
	echo "Entering HiCExplorer" >> $log_path
	date >> $log_path 
	if [ $norm_name == 'ICEnorm' ]
	then
		hicexplorer_norm='IC'
	elif [ $norm_name == 'KRnorm' ]
	then
		hicexplorer_norm='KR'
	fi

	#hicCorrectMatrix correct --matrix hic_matrix.h5 --filterThreshold -out corrected_matrix.h5
	cd $additional_file_path
	 hicFindTADs --matrix ${cool_or_h5_path} --outPrefix HICExplorer_${norm_name} --correctForMultipleTesting fdr --chromosomes $chr
	 python3 $home_path/Analysis/HiCExplorerClean.py $additional_file_path/HICExplorer_${norm_name}_domains.bed $resolution $output_path/HiCExplorer.bed
	echo "Exiting HiCExplorer" >> $log_path
	date >> $log_path 
fi

#Spectral
if [ $spectral == 'True' ]
then
	cd $Caller_path
	 python3 $home_path/Analysis/shift_nxn.py $input_path $temp_path spectral.matrix $chr $resolution
	spectral_input=${temp_path}/spectral.matrix
	spectral_path=spectral_${job_id}_${norm_name}.r
	printf 'Entering spectral\n-----------------\n'
	echo "Entering Spectral" >> $log_path
	date >> $log_path 

	echo "library(SpectralTAD)" > $spectral_path
	echo "matrix <- read.table(\"${spectral_input}\", sep = \"\t\")" >> $spectral_path
	echo "hold <- matrix[,colSums(is.na(matrix))<nrow(matrix)]" >> $spectral_path
	echo "spec_table <- SpectralTAD(hold, chr= \"chr${chr}\", out_format= \"bed\", out_path= \"${temp_path}/spectral.bed\")" >> $spectral_path
	 Rscript "${spectral_path}"
	rm -rf spectral_${job_id}_${norm_name}.r
	 python3 $home_path/Analysis/cleanSpectral.py $temp_path/spectral.bed  $output_path
	 python3 $home_path/Analysis/check_bed_error.py $output_path/Spectral.bed >> $log_path

	echo "Exiting Spectral" >> $log_path
	date >> $log_path
fi

rm -r ${temp_path}


#Not being used

#CHDF Curently fails due to unknown issue
#if [ $chdf == 'True' ]
#then
#	printf 'Entering chdf\n-----------------\n'
#	cd $Caller_path
#	./CHDF $input_path $output_path/chdf.bed 1535 1000 1000
#fi

#chromoR
if [ $chromo_r == 'True' ]
then
	cd $Caller_path
	printf 'Entering ChromoR\n-----------------\n'
	path=chromoR_${job_id}.r
	echo "library(chromoR)" > $path
	echo "matrix <- read.delim(\"${input_path}\", header = FALSE, sep = \"\t\", quote = \"\" )" >> $path
	echo "data = rowSums(matrix, na.rm=TRUE)" >> $path
	echo "res = segmentCIM(data)" >> $path
	echo "sink(\"${output_path}/chromoR.txt\")" >> $path
	echo "print(res)" >> $path
	echo "sink()" >> $path
	Rscript "${path}"
	rm -rf chromoR_${job_id}.r
	python3 $home_path/Analysis/chromoRClean.py $output_path/chromoR.txt $resolution $input_path
fi

