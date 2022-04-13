source TADMaster.config									# change path to config file
echo "Running TADMaster on $input_matrix"

#--------------------------------------------------------------------------------------------------------
#Make paths
#--------------------------------------------------------------------------------------------------------


home_path="${PWD}"											# change home_path
Caller_path="${home_path}/TADCallers"
Norm_method_path="${home_path}/normalization" 
job_path="${PWD}/example_job_output"     					# change output_path                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
input_path="${input_matrix}"
output_path="${job_path}/output"
temp_path="${job_path}/temp"
additional_file_path="${job_path}/additional_files"
normalized_path="${job_path}/normalizations"
log_path="${job_path}/log.txt"

#--------------------------------------------------------------------------------------------------------
# Create the folder structure in job path
#--------------------------------------------------------------------------------------------------------


if [ -d $job_path ]
then
	mkdir $output_path
	mkdir $temp_path
	mkdir $additional_file_path
	mkdir $normalized_path

fi


#--------------------------------------------------------------------------------------------------------
#Enter normalization methods
#--------------------------------------------------------------------------------------------------------

echo "Normalizing Matrix" > $log_path
date >> $log_path 

cd $Norm_method_path

if [ $data_input_type == 'square' ]
then
	 Rscript full2sparse.r ${input_path} ${resolution} ${job_path}/sparse_input.txt
	input_path="${job_path}/sparse_input.txt"
fi 

if [ $data_input_type == 'cool' ]
then
	cool_or_h5_path="${input_path}"
	MRES=$(cooler ls $cool_or_h5_path)
	if (( $(grep -c . <<<"$MRES") > 1 ))
	then
		 cooler dump --join -H ${input_path}::resolutions/${resolution} > $temp_path/mcool.txt
		 python3 cool_to_sparse.py -i $temp_path/mcool.txt -o ${job_path}/sparse_input.txt -r ${resolution} -c ${chr}	 

	else
		NCHR=$(cooler info -f nchroms ${input_path})           
		if [ $NCHR == '1' ]
		then
			 cooler dump --join -H ${input_path} > $temp_path/dump_sparse.txt
			 python3 cool_to_sparse.py -i $temp_path/dump_sparse.txt -o ${job_path}/sparse_input.txt -r ${resolution} -c ${chr}	  
		else
			hicConvertFormat --matrices ${input_path} --outFileName $temp_path/single.cool --inputFormat cool --outputFormat cool --chromosome ${chr}
			 cooler dump --join -H $temp_path/single.cool > $temp_path/dump_sparse.txt
			 python3 cool_to_sparse.py -i $temp_path/dump_sparse.txt -o ${job_path}/sparse_input.txt -r ${resolution} -c ${chr}	 
		fi
	fi
	input_path="${job_path}/sparse_input.txt"
fi

if [ $data_input_type == 'hic' ]
then
	hic_path="${input_path}"
	 hicConvertFormat -m ${input_path} --inputFormat hic --outputFormat cool -o ${job_path}/matrix.cool --resolutions ${resolution} --chromosome ${chr}
	mv "${job_path}/matrix_${resolution}.cool" "${job_path}/matrix.cool"
	cool_or_h5_path="${job_path}/matrix.cool"
	hicConvertFormat --matrices ${job_path}/matrix.cool --outFileName $temp_path/single.cool --inputFormat cool --outputFormat cool --chromosome ${chr}
	 cooler dump --join -H $temp_path/single.cool > $temp_path/dump_sparse.txt
	 python3 cool_to_sparse.py -i $temp_path/dump_sparse.txt -o ${job_path}/sparse_input.txt -r ${resolution} -c ${chr}
	input_path="${job_path}/sparse_input.txt"
fi

if [ $data_input_type == 'h5' ]
then
	cool_or_h5_path="${input_path}"
	hicConvertFormat -m ${input_path} --inputFormat h5 --outputFormat cool -o ${job_path}/matrix.cool --resolutions ${resolution} --chromosome ${chr}
	hicConvertFormat --matrices ${job_path}/matrix.cool --outFileName $temp_path/single.cool --inputFormat cool --outputFormat cool --chromosome ${chr}
	 cooler dump --join -H $temp_path/single.cool > $temp_path/dump_sparse.txt
	 python3 cool_to_sparse.py -i $temp_path/dump_sparse.txt -o ${job_path}/sparse_input.txt -r ${resolution} -c ${chr}
	input_path="${job_path}/sparse_input.txt"
fi




# converting sparse matrix to ccmap
 python3 sparse2ccmap.py ${input_path} ${temp_path}


# ChromoR
if [ $norm_chromor == 'True' ]
then
	 Rscript chromoRNorm.r ${input_path} ${normalized_path} ${species} ${chr} ${resolution} ${input_path}
fi


# Note: the input file is the ccmap generated from the matrix input, output is also ccmap


# IC
if [ $norm_ice == 'True' ]
then
	 gcMapExplorer normIC -i ${temp_path}/exCCMap.ccmap -fi ccmap -fo ccmap -o ${temp_path}/ICEoutput.ccmap
#	gcMapExplorer normIC -i ${temp_path}/exCCMap.ccmap -fi ccmap -fo gcmap -o ${temp_path}/ICEoutput.gcmap
fi


# KR
if [ $norm_kr == 'True' ]
then
	 gcMapExplorer normKR -i ${temp_path}/exCCMap.ccmap -fi ccmap -fo ccmap -o ${temp_path}/KRoutput.ccmap
fi


# VC
if [ $norm_vc == 'True' ]
then
	 gcMapExplorer normVC -i ${temp_path}/exCCMap.ccmap -fi ccmap -fo ccmap -o ${temp_path}/VCoutput.ccmap
fi


# MCFS
if [ $norm_mcfs == 'True' ]
then
	 gcMapExplorer normMCFS -i ${temp_path}/exCCMap.ccmap -fi ccmap -fo ccmap -o ${temp_path}/MCFSoutput.ccmap
fi


# Converting from ccmap to sparse
python3 ccmapConvert.py ${temp_path} $norm_kr $norm_vc $norm_ice $norm_mcfs

# Takes the sparse matrices and converts them to full, also runs SCN normalization if specified in config file
 Rscript convert2fullFin.r ${temp_path} ${normalized_path} $norm_kr $norm_vc $norm_ice $norm_mcfs $norm_scn ${input_path}



#if [ $norm_mcfs == 'False' ] && [ $norm_vc == 'False' ] && [ $norm_kr == 'False' ] && [ $norm_ice == 'False' ] && [ $norm_chromor == 'False' ]
#then
   Rscript sparse2matrix_no_norm.r ${input_path} ${normalized_path}
#fi
cd $home_path

#--------------------------------------------------------------------------------------------------------
#Enter caller methods
#--------------------------------------------------------------------------------------------------------
echo "Entering caller methods parallel" >> $log_path
date >> $log_path 

for input in ${normalized_path}/*.txt; do
	 bash caller.sh $1 $input &
done

wait
for normalized_input in ${normalized_path}/*.txt; do
	#Changing directories
	norm_name=$(basename $normalized_input .txt)
	input_path="$normalized_input"
	output_path="${job_path}/output/$norm_name/"
	mkdir -p $output_path

	#CleanUp and remake
	rm -r ${temp_path}
	mkdir $temp_path


	log_path="${job_path}/log_${norm_name}.txt"

	# CaTCH
	if [ $catch == 'True' ]
	then
		
		printf 'Entering CaTCH\n-----------------\n'
		echo "Entering CaTCH" >> $log_path
		date >> $log_path
		cd $Caller_path/CaTCH_R
		 python3 $home_path/Analysis/preprocessCaTCH.py $input_path $temp_path $chr
		catch_path=${Caller_path}/NormCompare/CaTCH_${job_id}.r
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
		rm -rf ${Caller_path}/NormCompare/CaTCH_${job_id}.r
		 python3 $home_path/Analysis/check_bed_error.py $output_path/CaTCH_0.650.bin >> $log_path
		 python3 $home_path/Analysis/check_bed_error.py $output_path/CaTCH_0.550.bin >> $log_path
		cd $home_path
		echo "Exiting CaTCH" >> $log_path
		date >> $log_path
	fi

	if [ $clustertad == 'True' ]
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

done
cp ${home_path}/Read.me ${job_path}/Read.me
log_path="${job_path}/log.txt"
echo "Jobs Done!" >> $log_path
date >> $log_path 