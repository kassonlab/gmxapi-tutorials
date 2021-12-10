"""Complete working example for figure 1.

Prerequisites:
    This script assumes it is running in a local copy of the
    https://github.com/kassonlab/gmxapi-tutorials repository. It will look for input
    files relative to the location of this file.

After installing GROMACS and gmxapi, execute this script with a Python 3.7+ interpreter.

For a trajectory ensemble, use `mpiexec` and `mpi4py`. For example, for an ensemble of
size 50, activate your gmxapi Python virtual environment and run

    mpiexec -n 50 `which python` -m mpi4py fs-peptide.py

"""
import logging
import os
import typing
from pathlib import Path

import gmxapi as gmx
import gmxapi.abc
from gmxapi import function_wrapper
from gmxapi.exceptions import UsageError

logging.basicConfig(level=logging.INFO)

logging.info(f'gmxapi Python package version {gmx.__version__}')
assert gmx.version.has_feature('mdrun_runtime_args')
assert gmx.version.has_feature('container_futures')
assert gmx.version.has_feature('mdrun_checkpoint_output')


try:
    import mpi4py.MPI
    ensemble_size = mpi4py.MPI.COMM_WORLD.Get_size()
    if mpi4py.MPI.COMM_WORLD.Get_rank() == 0 and ensemble_size > 1:
        logging.info(f'{ensemble_size} MPI ranks detected. Running ensemble.')
except:
    ensemble_size = 1

#
# Define some helpers
#


def less_than(lhs: typing.SupportsFloat, rhs: typing.SupportsFloat):
    """Compare the left-hand-side to the right-hand-side.

    Follows the Numpy logic for normalizing the numeric types of *lhs* and *rhs*.
    """
    import numpy as np
    dtype = int
    if any(isinstance(operand, float) for operand in (lhs, rhs)):
        dtype = float
    elif all(isinstance(operand, typing.SupportsFloat) for operand in (lhs, rhs)):
        if type(np.asarray([lhs, rhs])[0].item()) is float:
            dtype = float
    elif any(isinstance(operand, gmxapi.abc.Future) for operand in (lhs, rhs)):
        for item in (lhs, rhs):
            if hasattr(item, 'dtype'):
                if issubclass(item.dtype, (float, np.float)):
                    dtype = float
            elif hasattr(item, 'description'):
                if issubclass(item.description.dtype, (float, np.float)):
                    dtype = float
    else:
        raise UsageError(f'No handling for [{repr(lhs)}, {repr(rhs)}].')

    if dtype is int:
        def _less_than(lhs: int, rhs: int) -> bool:
            return lhs < rhs
    elif dtype is float:
        def _less_than(lhs: float, rhs: float) -> bool:
            return lhs < rhs
    else:
        raise UsageError('Operation only supports standard numeric types.')
    return function_wrapper()(_less_than)(lhs=lhs, rhs=rhs)


@function_wrapper()
def _numpy_min_float(data: gmx.NDArray) -> float:
    import numpy as np
    logging.info(f'Looking for minimum in {data}')
    return float(np.min(data._values))


def numeric_min(array):
    """Find the minimum value in an array.
    """
    return _numpy_min_float(data=array)


@gmx.function_wrapper(output={'data': gmx.NDArray})
def xvg_to_array(path: str, output):
    """Get an NxM array from a GROMACS xvg data file.

    For energy output, N is the number of samples, and the first of M
    columns contains simulation time values.
    """
    import numpy
    logging.info(f'Reading xvg file {path}.')
    data = numpy.genfromtxt(path, comments='@', skip_header=14)
    logging.info(f'Read array shape {data.shape} from {path}.')
    output.data = data


######################
# Confirm inputs exist
#

_script_dir = Path(__file__)
input_dir = _script_dir.parent.parent.resolve() / 'input_files' / 'fs-peptide'
if not all(p.exists() for p in (input_dir, input_dir / 'start0.pdb', input_dir / 'ref.pdb')):
    raise RuntimeError(f'Did not find input files in {input_dir}.')
reference_struct = input_dir / 'ref.pdb'


######################
# Complete code from figure 1
#

def figure1a():
    """Figure 1a: gmxapi command-line operation.

    Prepare a molecular model from a PDB file using the `pdb2gmx` GROMACS tool.
    """
    # Figure 1a code
    args = ['pdb2gmx', '-ff', 'amber99sb-ildn', '-water', 'tip3p']
    input_files = {'-f': os.path.join(input_dir, 'start0.pdb')}
    output_files = {
            '-p': 'topol.top',
            '-i': 'posre.itp',
            '-o': 'conf.gro'}
    make_top = gmx.commandline_operation('gmx', args, input_files, output_files)
    return make_top


def figure1b(make_top):
    """Figure 1b: gmxapi command on ensemble input

    Call the GROMACS MD preprocessor to create a simulation input file. Declare an
    ensemble simulation workflow starting from the single input file.

    Args:
        make_top operation handle, as generated in `figure1a`

    Returns:
        Trajectory output. (list, if ensemble simulation)
    """

    # Confirm inputs exist.
    make_top.run()
    assert os.path.exists(make_top.output.file['-o'].result())
    assert os.path.exists(make_top.output.file['-p'].result())
    cmd_dir = input_dir
    assert os.path.exists(input_dir / 'grompp.mdp')

    # Figure 1b code.
    grompp_input_files = {'-f': os.path.join(cmd_dir, 'grompp.mdp'),
                          '-c': make_top.output.file['-o'],
                          '-p': make_top.output.file['-p']}

    # make array of inputs
    N = ensemble_size
    grompp = gmx.commandline_operation(
        'gmx',
        ['grompp'],
        input_files=[grompp_input_files] * N,
        output_files={'-o': 'run.tpr'})
    tpr_input = grompp.output.file['-o'].result()

    input_list = gmx.read_tpr(tpr_input)

    md = gmx.mdrun(input_list, runtime_args={'-maxh': '0.001'})
    md.run()

    return {
        'input_list': input_list,
        'trajectory': md.output.trajectory.result()}


def figure1c(input_list):
    """Figure 1c: looping and custom operations"""
    subgraph = gmx.subgraph(variables={'found_native': False, 'checkpoint': '',
                                       'min_rms': 1e6, 'incomplete': True})
    with subgraph:
        md = gmx.mdrun(
            input_list,
            runtime_args={
                '-cpi': subgraph.checkpoint,
                '-maxh': '.001',
                '-noappend': None
            })
        logging.info(f'Binding checkpoint {md.output.checkpoint}')
        subgraph.checkpoint = md.output.checkpoint
        logging.info(f'Setting up rmsd calculation.')
        rmsd = gmx.commandline_operation(
            'gmx', ['rms'],
            input_files={
                '-s': reference_struct,
                '-f': md.output.trajectory},
            output_files={'-o': 'rmsd.xvg'},
            stdin='Backbone Backbone\n'
        )
        logging.info(f'Binding output {rmsd.output.file}')
        subgraph.min_rms = numeric_min(
            xvg_to_array(rmsd.output.file['-o']).output.data).output.data
        subgraph.found_native = less_than(lhs=subgraph.min_rms, rhs=0.3).output.data
        logging.info(f'Bound result {subgraph.found_native}')
        subgraph.found_native = False
        subgraph.incomplete = gmx.logical_not(subgraph.found_native)

    folding_loop = gmx.while_loop(operation=subgraph,
                                  condition=subgraph.incomplete)()
    logging.info('Beginning folding_loop.')
    folding_loop.run()
    logging.info(f'Finished folding_loop at iteration {subgraph.iteration}.')
    return folding_loop


if __name__ == '__main__':
    make_top = figure1a()
    logging.info('Created a handle to a commandline operation.')

    input_list, trajectory = figure1b(make_top).values()
    if isinstance(trajectory, list):
        logging.info(
            'Generated trajectories: '
            ', '.join(filename for filename in trajectory)
        )
    else:
        logging.info(f'Generated trajectory {trajectory}.')

    folding_loop = figure1c(input_list)
    logging.info(f'Folding loop result: {folding_loop}')
