# gmxapi-tutorials
Python examples and tutorial material for gmxapi 0.3 on GROMACS 2022

## First

* Install the required software.
* Get the sample input files.
* Clone this repository or download the scripts of interest (from the [examples] directory) for local execution. Refer to internal documentation (comment strings) withint the scripts for more information.

### Get the software

Get the gmxapi 2022 software stack

#### Option 1: Google Drive link

From an archive (contains Gromacs2022 beta2, gmxapi 0.3, and run_brer files):
https://drive.google.com/drive/folders/1-i4jY22Bg2jDtvfNKBlYuQwJOq08qraB?usp=sharing

Example: `wget 'https://drive.google.com/uc?export=download&id=1-n-b6hmUNjaF9h4VBw0SkCKQbUIAvDsL' -O gmxapi-0.3.0b2.tgz`

or

#### Option 2: Download packages

Download archives from the following URLs.

* GROMACS 2022: https://gitlab.com/gromacs/gromacs/-/archive/v2022-beta2/gromacs-v2022-beta2.tar.bz2
* gmxapi 0.3: gmxapi-0.3.0b3.tar.gz
  Example: https://pypi.org/project/gmxapi/0.3.0b3/#files
* Run_brer 2.0 (master branch) https://github.com/kassonlab/run_brer/ or https://github.com/kassonlab/run_brer/archive/master.tar.gz
* Brer-plugin current master https://github.com/kassonlab/brer_plugin or https://github.com/kassonlab/brer_plugin/archive/master.tar.gz

### Install the software

Refer to installation instructions from the software archive or from the respective project web sites.

### Alternative: Docker

If you prefer to use a containerized installation of the software and examples, and you are comfortable with Docker, see the [Dockerfile](Dockerfile) in this repository.

### Sample inputs

Sample input files for these examples have been shared from previous research projects. They are covered by separate copyright and licensing details.

BRER workflow sample inputs: [DOI 10.5281/zenodo.5122931](https://zenodo.org/record/5122931)

FS peptide ([`input_files/fs-peptide/`](input_files/fs-peptide/)):
Sorin and Pande, Biophys J. 2005 Apr; 88(4): 2472–2493; doi:10.1529/biophysj.104.051938 (used with permission).

## Example scripts

[examples/fs-peptide.py](examples/fs-peptide.py)

## Caveats (TODOs)

Workflow is not checkpointed. You are advised to use a clean working directory for each script invocation.
