# TADMaster: A Comprehensive Web-based Tool For Analysis of Topologically Associated Domains 

#### OluwadareLab, University of Colorado, Colorado Springs
___________________

#### Developers:
Sean Higgins <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [shiggins@uccs.edu](mailto:shiggins@uccs.edu) <br />

Victor Akpokiro <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [vakpokir@uccs.edu](mailto:vakpokir@uccs.edu) 

#### Contact:
Oluwatosin Oluwadare, PhD <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [ooluwada@uccs.edu](ooluwada@uccs.edu) <br /><br />
	

___________________
### Access TADMaster:  http://tadmaster.io
___________________	

## Build Instructions:
TADMaster can be run in a Docker-containerized environment locally on users computer. Before cloning this repository and attempting to build, the [Docker engine](https://docs.docker.com/engine/install/), If you are new to docker [here is a quick docker tutorial for beginners](https://docker-curriculum.com/). <br> 
To install and build TADMaster follow these steps.

1. Clone this repository locally using the command `git clone https://github.com/OluwadareLab/TADMaster.git && cd TADMaster`.
2. Pull the TADMaster docker image from docker hub using the command `docker pull oluwadarelab/tadmaster:latest`. This may take a few minutes. Once finished, check that the image was sucessfully pulled using `docker image ls`.
3. Run the TADMaster container and mount the present working directory to the container using `docker run -v ${PWD}:${PWD}  -p 8050:8050 -it oluwadarelab/tadmaster`.
4. `cd` to your home directory.

:thumbsup: Congratulations! You can now run TADMaster and TADMaster Plus locally with no restriction.

___________________	
## Dependencies:
TADMaster is written in <i>Python3, Dash and includes many R, python c++ libraries </i> necessary to run the various tools included and perform analysis visualization. All dependencies are included in the Docker environment. GPU is not loaded into the docker container as it is not needed to run TADMaster.
_________________

## Running local versions of TADMaster
Now, that you are running a docker container, follow the step by step instructions to execute the cloned TADMaster source codes for job processing and visualization.

_________________
## Running TADMaster Plus: 

#### STEP 1: Parameter Setting in TADMaster.config file
* Make changes to the `TADMaster.config` file based on your preferences.
	* We have provided some default parameter settings as an example.
* Required Inputs are : Specify the **input matrix path**,  **chromosome number**,  **resolution** and  **input datatype**.
	* We have provided some default parameter setting as an example.
* Use `True` or `False` to turn on or off respectively a Normalization or TADCaller algorithm.
	* By default we Turned on Normalization: `KR` and TADCallers: `Armatus`
	
#### STEP 2: Path change in TADMasterPlus.sh and caller.sh scripts
In both scripts:
* Replace `path_directory` in line 1 to the directory where your `TADMaster.config` file is located
	* We have provided some default  settings as an example.
* Change the `home_path` to the directory where `TADMaster` repository files you downloaded is located
	* We have provided some default  settings as an example.
* _make a new directory_: `mkdir example_job_output`
* Change the `job_path` to the path directory where you want the job processing outputs to be saved
	* We assigned `job_path`  directory to`example_job_output` in both scripts.

#### STEP 3: Run the TADMasterPlus.sh script

```bash
$ chmod +x TADMasterPlus.sh 
$./TADMasterPlus.sh 
```
* Running this script with this settings should take about 2 minutes.
* Once Completed, TADMasterPlus will generate all outputs in the output path, `job_path` directory, that the user identified.
* TADMAster Plus also generates a `Read.me` file that describes the output file structure and organization.
 
#### STEP 4: Analysis Visualization

Refer to the [Visualization Section](https://github.com/OluwadareLab/TADMaster#analysis-and-visualization) below for this.

_________________
## Runing TADMaster: 
## STEP A: Data Preprocessing
There are two pathways for running TADMaster, **with contact matrix _OR_ without contact matrix** (optional). _Contact Matrix is **optional**_  because it is needed only to include TADs annotation on heat-maps visualization.

### PATHWAY 1: With Contact Matrix
#### STEP 1: Parameter Setting in TADMaster.config file
* Make changes to the `TADMaster.config` file based on your preferences.
* Required Inputs are: Specify the **input matrix path**,  **chromosome number**,  **resolution** and  **input datatype**.
* Turn off all Normalization or TADCaller algorithm by setting to `False` .
	* _The purpose of running this script_ is  to convert the input data from the accepted input format and extract the identified chromosome matrix.

#### STEP 2: Path change in TADMaster.sh script
* Replace `path_directory` in line 1 to the directory where your `TADMaster.config` file is located.
* Change the `home_path` to the directory where `TADMaster` repository files you downloaded is located.
* Change the `job_path` to the path directory where you want the job processing outputs to be saved.

#### STEP 3: Run the TADMaster.sh script

```bash
$ chmod +x TADMaster.sh 
$./TADMaster.sh 
```
* Once completed, TADMaster will generate all outputs in the output path, `job_path` directory, that the user identified.
* TADMaster  also generates a `Read.me` file that describes the output file structure and organization.

<br>

### PATHWAY 2: Without Contact Matrix
* Extract the TADMaster output file structure we provided.

```bash
$ tar -xvf job_tadmaster.tar.gz 
```
_________________

## STEP B: Bed file Upload
 Next, **copy** the `.bed` files you want to **perform analysis** on into the directory path specified below based on the pathway you followed above.
 
###### Path Description:
> ######  Pathway 1: With Contact Matrix
> - Path to copy the bed files into: `job_path/output/Nameofmatrix/` . 
_where_
> 	- `job_path` is the path directory where you specified for your job outputs to be saved
> 	- `Nameofmatrix` is the Name of the matrix you uploaded or extracted from the input data provided. Simply, users should expect to have one folder inside **output directory**
>
> ######  Pathway 2: Without Contact Matrix
> -  Path to copy the bed files into:  `job_tadmaster/output/NoMatrixProvided/` .
_where_
> 	- `job_tadmaster` by default is the name of the _passive output directory_ extracted in Step A into the TADMaster directory. Passive because it wasn't specified by you.
> 	- `NoMatrixProvided` by default is the Name of the folder because no matrix was provided
>

*Note*: See our wiki for information about [BED file formats](https://github.com/OluwadareLab/TADMaster/wiki/TADMaster#-bed-file-formats-accepted-) accepted by TADMaster
 
_________________

## STEP C: Analysis Visualization

Refer to the [Visualization Section](https://github.com/OluwadareLab/TADMaster#analysis-and-visualization) below for this.

____________


# Analysis and Visualization
#### Preliminary Information
* When you have completed a TADMaster or TADMaster job submission, the next step is Visualization.
* At this step, your job should be in the output path, `job_path` directory, which  would contain the BED Files to perform analysis and visualization on.
	* BED files will be located in `job_path/output/<name_of_normalization_used>/`
* To visualize the analysis from the bed files: 

### STEP 1: Parameter Setting in tadmaster_visualize.py  script
* Required Inputs are : Specify the `resolution`, `chromosome number`, and `job_path` of the job
	* We have provided some default input assignment as an example.

### STEP 2: Run the Visualize.py script

```bash
$ python tadmaster_visualize.py
```
### STEP 3: Visualize on your Local browser
* Once, you have executed the python script, You should get the message that `Dash is running on http://0.0.0.0:8050/`
(ignore warning messages provided).  :thumbsup: Congratulations! This means that you can visualize locally.


* Open your browser and copy the URL shown. You would be able to access the visualization of the output jobs.

Please note that for some browsers, like safari, localhost URL could be different. 
If URL:http://0.0.0.0:8050/ doesn't return a visualization, please use URL: http://127.0.0.1:8050

_________________

# Content of Folder:
- **job_861482c1-927a-487c-a18a-a2be43fe0478.zip**: A previously submitted job 
- **Data:** Sample input data accepted
- **TADCaller:**  TAD algorithm source codes used by TADMaster
- **Analysis:** Pre- and Post- processing scripts used by TADMaster 
- **normalization:** Libraries and Scripts to support data normalization for the web server



_________________

# Web Server Version Documentation

Please see [the wiki](https://github.com/OluwadareLab/TADMaster/wiki) for an extensive documentation of how to use TADMaster functions

_________________
	
### cite

_________________
 ![footer](http://biomlearn.uccs.edu/static/image/UCCS_Logo.png) © 2021 Oluwadare Lab 
	  
	



