# gmxapi-tutorials
Python examples and tutorial material for gmxapi 0.3 on GROMACS 2022

This material is under development at https://github.com/kassonlab/gmxapi-tutorials for contribution to https://tutorials.gromacs.org/

## First

* Install the required software.
* Get the sample input files.
* Clone this repository or download the scripts of interest (from the [examples] directory) for local execution. Refer to internal documentation (comment strings) within the scripts for more information.

### Get the software

Get the gmxapi 2022 software stack

#### Option 1: Google Drive link

From an archive (contains Gromacs2022 beta2, gmxapi 0.3, and run_brer files):
https://drive.google.com/drive/folders/1-i4jY22Bg2jDtvfNKBlYuQwJOq08qraB?usp=sharing

or

#### Option 2: Download packages

Download archives from the following URLs.

* GROMACS 2022: https://gitlab.com/gromacs/gromacs/-/archive/release-2022/gromacs-release-2022.tar.gz
* gmxapi 0.3: gmxapi-0.3.0b6.tar.gz
  (Download from https://pypi.org/project/gmxapi/0.3.0b6/#files or use the [`--pre`](https://pip.pypa.io/en/stable/cli/pip_install/#pre-release-versions) option: `pip install --pre gmxapi` (after installing and activating GROMACS 2022)
* *Optional* Run_brer 2.0 (master branch) https://github.com/kassonlab/run_brer/ or https://github.com/kassonlab/run_brer/archive/master.tar.gz
* *Optional* Brer-plugin current master https://github.com/kassonlab/brer_plugin or https://github.com/kassonlab/brer_plugin/archive/master.tar.gz

### Install the software

Refer to installation instructions from the software archive or from the respective project web sites.

### Alternative: Docker

If you prefer to use a containerized installation of the software and examples, and you are comfortable with Docker, see the [Dockerfile](Dockerfile) in this repository or pull `gmxapi/tutorial` from [DockerHub](https://hub.docker.com/repository/docker/gmxapi/tutorial).

### Sample inputs

Sample input files for these examples have been shared from previous research projects. They are covered by separate copyright and licensing details.

BRER workflow sample inputs: [DOI 10.5281/zenodo.5122931](https://zenodo.org/record/5122931)

FS peptide ([`input_files/fs-peptide/`](input_files/fs-peptide/)):
Sorin and Pande, Biophys J. 2005 Apr; 88(4): 2472–2493; doi:10.1529/biophysj.104.051938 (used with permission).

## Example scripts

[examples/fs-peptide.py](examples/fs-peptide.py)

## Caveats (TODOs)

Workflow is not checkpointed. You are advised to use a clean working directory for each script invocation.
