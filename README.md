# TADMaster: A Comprehensive Web-based Tool For Analysis of Topologically Associated Domains 

<img src="http://biomlearn.uccs.edu/static/image/testing.jpg" width="700" height="500">
------------------------------------------------------------------------------------------------------------------------------------
**OluwadareLab, University of Colorado, Colorado Springs**
----------------------------------------------------------------------

#### Developers:
Sean Higgins <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [shiggins@uccs.edu](mailto:shiggins@uccs.edu)

Victor Akpokiro <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [vakpokir@uccs.edu](mailto:vakpokir@uccs.edu) <br /><br />

#### Contact:
Oluwatosin Oluwadare, PhD <br />
Department of Computer Science <br />
University of Colorado, Colorado Springs <br />
Email: [ooluwada@uccs.edu](ooluwada@uccs.edu) <br /><br />
	

--------------------------------------------------------------------
### Access TADMaster:  http://tadmaster.io
--------------------------------------------------------------------	

## Build Instructions:
TADMaster runs in a Docker-containerized environment. Before cloning this repository and attempting to build, install the Docker engine. To install and build HiCARN follow these steps.

1. Clone this repository locally using the command `git clone https://github.com/OluwadareLab/HiCARN.git && cd HiCARN`.
2. Pull the HiCARN docker image from docker hub using the command `docker pull oluwadarelab/hicarn:latest`. This may take a few minutes. Once finished, check that the image was sucessfully pulled using `docker image ls`.
3. Run the HiCARN container and mount the present working directory to the container using `docker run --rm --gpus all -it --name hicarn -v ${PWD}:${PWD} oluwadarelab/hicarn`.
4. `cd` to your home directory.

___________________


# Content of Folder

* **Website Draft**: A sketch draft of the TADMaster website
* **Source Code:** Download the TADMaster Source Code from this link: https://biomlearn.uccs.edu/Data/TADMaster.tar.gz
* Example data in cool format 
--------------------------------------------------------------------		

# Documentation

Please see [the wiki](https://github.com/OluwadareLab/TADMaster/wiki) for an extensive documentation of how to use TADMaster functions


--------------------------------------------------------------------		

# cite





 ![footer](http://biomlearn.uccs.edu/static/image/UCCS_Logo.png) © 2021 Oluwadare Lab 
	  
	



