# gmxapi-tutorials
Python examples and tutorial material for gmxapi 0.3 on GROMACS 2022.

This material is under development at https://github.com/kassonlab/gmxapi-tutorials for contribution to https://tutorials.gromacs.org/

Clone this repository or pull a Docker image for an interactive walk-through of gmxapi 0.3.
Tutorial material is provided as Jupyter notebooks. (See below for instructions on installing software and accessing a Jupyter notebook server.)

## Repository Contents

* [Tutorial.ipynb](gmxapi-introduction/Tutorial.ipynb) provides an introduction to gmxapi concepts and syntax, and works up to an example of a parallel simulation and analysis loop. In our loop, we simulate a funnelweb spider peptide as it folds, comparing to a reference structure, extending the trajectory with each iteration. The loop terminates when the root-mean-squared displacement of the peptide backbone is within our selected tolerance of the reference structure (or when the "while loop" has exceeded a maximum number of iterations.)
* [fs-peptide.py](examples/fs-peptide.py) file captures all the above tutorial material in a script that can be executed with `mpiexec` (such as through a HPC job). See the script contents (or run with `--help`) for details on the run time logic and options.
* [overview.ipynb](gmxapi-introduction/overview.ipynb) contains additional preliminary information and checks to help set up and verify the Python environment.

## Sample inputs

Sample input files for these examples have been shared from previous research projects. They are covered by separate copyright and licensing details.

BRER workflow sample inputs: [DOI 10.5281/zenodo.5122931](https://zenodo.org/record/5122931)

FS peptide ([`input_files/fs-peptide/`](input_files/fs-peptide/)):
Sorin and Pande, Biophys J. 2005 Apr; 88(4): 2472–2493; doi:10.1529/biophysj.104.051938 (used with permission).

## Getting started

* Install the required software.
* Get the sample input files.
* Clone this repository or download the scripts of interest (from the [examples] directory) for local execution. Refer to internal documentation (comment strings) within the scripts for more information.

### Get the software

Get the gmxapi 2022 software stack

Download archives from the following URLs.

* GROMACS 2022: https://gitlab.com/gromacs/gromacs/-/archive/release-2022/gromacs-release-2022.tar.gz
* gmxapi 0.3: gmxapi-0.3.0.tar.gz
  (Download from https://pypi.org/project/gmxapi/0.3.0/#files or use `pip install gmxapi` (after installing and activating GROMACS 2022)
* *Optional* Run_brer 2.0 (master branch) https://github.com/kassonlab/run_brer/ or https://github.com/kassonlab/run_brer/archive/master.tar.gz
* *Optional* Brer-plugin current master https://github.com/kassonlab/brer_plugin or https://github.com/kassonlab/brer_plugin/archive/master.tar.gz

### Install the software

Refer to installation instructions at the respective project websites.
* [gmxapi on GROMACS](https://manual.gromacs.org/2022-rc1/gmxapi/userguide/install.html), 
* *run-brer TBD*, 
* *brer-plugin TBD*.

### Alternative: Docker

If you prefer to use a containerized installation of the software and examples, and you are comfortable with Docker, see the [Dockerfile](Dockerfile) in this repository or pull `gmxapi/tutorial` from [DockerHub](https://hub.docker.com/repository/docker/gmxapi/tutorial).

## Accessing the tutorial material

### From a local Python virtual environment

First, install GROMACS 2022, create a Python virtual environment, and install the `gmxapi` Python package (see above))

1. Install additional tutorial dependencies in the virtual environment, using the provided [requirements.txt](requirements.txt).
    ```shell
   $ . /path/to/venv/bin/activate
   $ pip install -r requirements.txt
   ```
2. Launch the Jupyter notebook server.
    ```shell
   $ jupyter notebook
    ```
3. If your desktop environment does not automatically take you to the web interface, copy the URL (with token) from the terminal output and paste into your web browser.
4. Navigate to `gmxapi-introduction`, and open `Tutorial.ipynb`.

### From Docker

If you have [Docker](https://www.docker.com/get-started) installed, you can build an image from the included [Dockerfile](Dockerfile) or `docker pull gmxapi/tutorial`.

Then, launch a container and redirect a local port to the 8888 http port in the container. Assuming port 8888 is available on your desktop:
```shell
$ docker run --rm -ti -p 8888:8888 gmxapi/tutorial
```

If your desktop environment does not automatically take you to the web interface, copy the URL (with token) from the terminal output and paste into your web browser. 
Navigate to `gmxapi-introduction`, and open `Tutorial.ipynb`.

**Warning:** The `--rm` in the command line above tells Docker to remove the container when you shut down the container. Any edits you make to the notebook will be lost. If you want to save your changes, the best choice is to use the File->Download option from within the notebook. Alternatively, you could explicitly make a snapshot of the container with [`docker commit`](https://docs.docker.com/engine/reference/commandline/commit/). You could run `docker` without the `--rm` option, but you will need to clean up extra containers manually to keep from filling up your hard disk.

## Caveats (TODOs)

Workflow is not checkpointed. You are advised to use a clean working directory for each script invocation.
