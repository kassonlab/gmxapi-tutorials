# Provide an easy-to-reproduce environment in which to test full Python functionality.

# Build (requires Docker 17.05 or higher):
#     docker build -t gmxapi-tutorial .
#
# Run an interactive shell:
#     docker run --rm -ti gmxapi-tutorial bash
#     . venv/bin/activate
#     cd examples
#     python
#     from figure1 import *
#     make_top = figure1a()
#     ...

FROM gmxapi/gromacs-dependencies-mpich:2022b2 as python-base

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq --no-install-suggests --no-install-recommends \
    install \
        python3 \
        python3-dev \
        python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r tutorial && useradd -m -s /bin/bash -g tutorial tutorial

USER tutorial
WORKDIR /home/tutorial

ENV VENV /home/tutorial/venv
RUN python3 -m venv $VENV
RUN . $VENV/bin/activate && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

FROM gmxapi/gromacs-mpich:2022b2 as gromacs

FROM python-base

COPY --from=gromacs /usr/local/gromacs /usr/local/gromacs

USER tutorial
WORKDIR /home/tutorial

RUN $VENV/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel

RUN $VENV/bin/pip install --no-cache-dir mpi4py

RUN $VENV/bin/pip install --no-cache-dir jupyter

ARG BRER_URL="https://github.com/kassonlab/brer_plugin/archive/master.tar.gz"

RUN . $VENV/bin/activate && \
    wget $BRER_URL -O brer-plugin-master.tar.gz && \
    tar zxvf brer-plugin-master.tar.gz && \
    cd brer_plugin-master && \
    mkdir build && \
    cd build && \
    gmxapi_DIR=/usr/local/gromacs cmake .. && \
    cmake --build . --target install && \
    cd .. && \
    cd .. && \
    python -c 'import brer' && \
    rm -rf brer*

ARG RUN_BRER_URL="https://github.com/kassonlab/run_brer/archive/master.tar.gz"

RUN . $VENV/bin/activate && \
    wget $RUN_BRER_URL -O run-brer-master.tar.gz && \
    pip install --no-cache-dir ./run-brer-master.tar.gz && \
    python -c 'import run_brer' && \
    rm -rf run-brer-master.tar.gz

ARG GMXAPI_URL="https://files.pythonhosted.org/packages/82/4a/0f5fb4c880fc1149dadfdedc3fb240c64eb177bca78584ba6d6bb4dddf86/gmxapi-0.3.0b3.tar.gz"

RUN . $VENV/bin/activate && \
    wget --no-check-certificate $GMXAPI_URL -O gmxapi-0.3.0b3.tgz && \
    . /usr/local/gromacs/bin/GMXRC && \
    pip install --no-cache-dir ./gmxapi-0.3.0b3.tgz && \
    python -c 'import gmxapi' && \
    rm ./gmxapi-0.3.0b3.tgz

ADD --chown=tutorial:tutorial input_files /home/tutorial/input_files
ADD --chown=tutorial:tutorial examples /home/tutorial/examples
ADD --chown=tutorial:tutorial gmxapi-introduction /home/tutorial/gmxapi-introduction

ADD .entry_points/ /docker_entry_points/

CMD ["/docker_entry_points/notebook"]

#CMD mpiexec -n 2 /home/tutorial/venv/bin/python -X dev -m mpi4py /home/tutorial/examples/fs-peptide.py
#CMD /bin/bash
#CMD $VENV/bin/jupyter notebook

# MPI tests can be run in this container without requiring MPI on the host.
# (We suggest running your docker engine with multiple CPU cores allocated.)
