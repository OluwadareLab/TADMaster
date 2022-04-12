# TADMaster: A Comprehensive Web-based Tool For Analysis of Topologically Associated Domains 

__________________
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
TADMaster runs in a Docker-containerized environment. Before cloning this repository and attempting to build, the [Docker engine](https://docs.docker.com/engine/install/). If you are new to docker [here is a quick docker tutorial for beginners](https://docker-curriculum.com/). To install and build TADMaster follow these steps.

1. Clone this repository locally using the command `git clone https://github.com/OluwadareLab/TADMaster.git && cd TADMaster`.
2. Pull the TADMaster docker image from docker hub using the command `docker pull oluwadarelab/tadmaster:latest`. This may take a few minutes. Once finished, check that the image was sucessfully pulled using `docker image ls`.
3. Run the HiCARN container and mount the present working directory to the container using `docker run  --name tadmaster -v ${PWD}:${PWD}  -p 8050:8050 -it oluwadarelab/tadmaster`.
4. `cd` to your home directory.

Congratulations! You will now be able to run TADMaster and TADMaster Plus locally with no restriction.


If you are new to docker  https://docker-curriculum.com/
___________________	
## Dependencies:
TADMaster is written in Python3 and Dash and includes many R, python c++ libraries necessary to run the various tools includes and the visualization. All dependencies are included in the Docker environment. GPU is not loaded into the docker container as it is not needed to run TADMaster.
_________________

## Running local versions of TADMaster
Now, that you are running a docker container, the instruction below will guide you step by step on how to use the cloned TADMaster source codes

### How to Run TADMaster: 


### How to Run TADMaster Plus: 
#### STEP 1: Parameter Setting in TADMaster.config file
* Make changes to the `TADMaster.config` file based on your preferences.
* Required Input are : Specify the input matrix path, chromosome number, resolution and input datatype.
	`* We have provided some default  input assignment as an example`
* Use True or False to turn on or off respectively a Normalization or TADCaller algorithm.
	`* By default we Turned on Normalization: KR and TADCallers: Armatus and Insulation score`
	
#### STEP 2: Path change in TADMasterPlus.sh and caller.sh scripts
In both scripts:
* Replace `path_directory` in line 1 to the directory where your `TADMaster.config` file is located
* Change the `home_path` to the directory where `TADMaster` repository you downloaded is located
* Change the `job_path` to the path directory where you want the job processing outputs to be saved

#### STEP 3: Run the TADMasterPlus.sh script
* Now, you are all done:

```bash
$./TADMasterPlus.sh 
```
* Once Completed, TADMasterPlus will generate all outputs in the output path `job_path` that the user identified.
* TADMAster Plus also generated a `Read.me` file that describes the output file structure and organization.
 

_________________

## Visualization
#### Preliminary Information
* When you have completed a TADMaster or TADMaster job submission, the next step is Visualization.
* To visualize the analysis breakdown for your completed job and see the different plots, follow the instructions below: 

_________________

# Content of Folder:
- job_861482c1-927a-487c-a18a-a2be43fe0478.zip**: A previously submitted job 
- TADMaster
- 

docker run  --name tadmaster -v ${PWD}:${PWD}  -p 8050:8050 -it oluwadarelab/tadmaster

_________________

# Documentation

Please see [the wiki](https://github.com/OluwadareLab/TADMaster/wiki) for an extensive documentation of how to use TADMaster functions

_________________
	

# cite





 ![footer](http://biomlearn.uccs.edu/static/image/UCCS_Logo.png) © 2021 Oluwadare Lab 
	  
	



