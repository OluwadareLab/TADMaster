source TADMaster.config									# change path to config file
echo "Running TADMaster on $input_matrix"

#--------------------------------------------------------------------------------------------------------
#Make paths
#--------------------------------------------------------------------------------------------------------


home_path="${PWD}"										# change home_path
Caller_path="${home_path}/TADCallers"
Norm_method_path="${home_path}/normalization" 
job_path="${PWD}/tadmaster_output"     					# change output_path                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
input_path="${input_matrix}"
output_path="${job_path}/output"
temp_path="${job_path}/temp"
additional_file_path="${job_path}/additional_files"
normalized_path="${job_path}/normalizations"

#--------------------------------------------------------------------------------------------------------
# Create the folder structure in job path
#--------------------------------------------------------------------------------------------------------


if [ -d $job_path ] && [ -z "$(ls -A $job_path)" ]
then
	echo "Making directories in the job path provided"
	mkdir $output_path
	mkdir "${output_path}/Raw"
	mkdir $temp_path
	mkdir $additional_file_path
	mkdir $normalized_path
elif [ ! -d $job_path ]
then
	echo "Job path did not exist. Making Job path and directories"
	mkdir $job_path
	mkdir $output_path
	mkdir "${output_path}/Raw"
	mkdir $temp_path
	mkdir $additional_file_path
	mkdir $normalized_path
else
	echo "The job path that you using in the config file is currently occupied by anouther job"
	exit
fi


#--------------------------------------------------------------------------------------------------------
#Enter normalization methods
#--------------------------------------------------------------------------------------------------------

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


# Converting from ccmap to sparse
python3 ccmapConvert.py ${temp_path} $norm_kr $norm_vc $norm_ice $norm_mcfs

# Takes the sparse matrices and converts them to full, also runs SCN normalization if specified in config file
Rscript convert2fullFin.r ${temp_path} ${normalized_path} $norm_kr $norm_vc $norm_ice $norm_mcfs $norm_scn ${input_path}



if [ $norm_mcfs == 'False' ] && [ $norm_vc == 'False' ] && [ $norm_kr == 'False' ] && [ $norm_ice == 'False' ] && [ $norm_chromor == 'False' ]
then
	Rscript sparse2matrix_no_norm.r ${input_path} ${normalized_path}
fi
cd $home_path
