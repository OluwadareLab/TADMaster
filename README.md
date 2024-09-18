Read Me
-----------------------------------------------------------------------------------------------
File organization:
-----------------------------------------------------------------------------------------------

1) Files in Base Directory
	- The original contact matrix that was uploaded
	- Transformations of the original contact matrix
		-This includes the sparse format. If .hic or .h5 were selected, 
		 then the .cool transformation is also provided.
	- log.txt
		- This is the main log which reports the errors in the main pipeline.
	- log_norm.txt
		- This is the normalization specific log that reports errors for each
		  caller selected.
 	-TADMaster.config
		- This is the internal record of the methods selected.
2) Temp Directory
	-This directory holds any tempory files needed while processing. It likely only 
	 contains if CaTCH  is selected.

2) Additional_files Directory
	-This directory holds any additional files produced by methods.

3) Normalizations Directory
	- This directory contains the normalized square matrices of the original contact matrix.

4) Output Directory
	- This directory contains a directory for each normalizion selected. Note non-normalized
	  inputs are contained under the raw directory.
		- Every sub-directory cointains the bed files generated using the specified
		  normalized matrix

-----------------------------------------------------------------------------------------------
Re-Uploading Job:
-----------------------------------------------------------------------------------------------

Periodically jobs are removed from the server, but you can reupload the zipped version of the job 
at: http://biomlearn.uccs.edu/TADMaster/upload_previous_job/

Alternatively, you can any contact matrix and two bed files at:
http://biomlearn.uccs.edu/TADMaster/upload_existing/
*Note you can upload additional bed files once the job has been processed

-----------------------------------------------------------------------------------------------
TadMasterWeb Migration:
-----------------------------------------------------------------------------------------------
The TADMaster web server is dockerised. To move it to a new server:  
1) clone the TADMasterWeb Branch of the Tadmaster repo
2) open the docker file and ensure the exposed ports are free, or change the ports such that they are free.
3) run docker build . 
4) once the docker image is built, run /usr/bin/docker run --rm -p {targetHostPort}:8000 -v /storage/store/TADMaster:/var/www/html/TADMaster/Site/storage -it -d --name TADMaster tadmasterserver
5) where 8000 is the port inside the docker and targetHost port is the port on your host machine that you want the server to be avalible on IE: 80 for defualt http port.
6) set up a systemd task to ensure the start command runs on startup so that a server reboot does not take the server down.


-----------------------------------------------------------------------------------------------
Additional Information:
-----------------------------------------------------------------------------------------------

All additional information can be found at: https://github.com/OluwadareLab/TADMaster/wiki
