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
from pathlib import Path

import gmxapi as gmx
from gmxapi import logical_not

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


######################
# Confirm inputs exist
#

_script_dir = Path(__file__)
input_dir = _script_dir.parent.parent.resolve() / 'input' / 'fs-peptide'
if not all(p.exists() for p in (input_dir, input_dir / 'start0.pdb', input_dir / 'ref.pdb')):
    raise RuntimeError('Missing input files.')
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

    md = gmx.mdrun(input_list, runtime_args={'-maxh': '2'})
    md.run()

    return {
        'input_list': input_list,
        'trajectory': md.output.trajectory.result()}


def figure1c(input_list):
    """Figure 1c: looping and custom operations"""
    subgraph = gmx.subgraph(variables={'found_native': False, 'checkpoint': '', 'min_rms': 1e6})
    with subgraph:
        md = gmx.mdrun(
            input_list,
            runtime_args={
                '-cpi': subgraph.checkpoint,
                '-maxh': '2'
            })
        subgraph.checkpoint = md.output.checkpoint
        rmsd = gmx.commandline_operation(
            'gmx', ['rms'],
            input_files={
                '-s': reference_struct,
                '-f': md.output.trajectory},
            output_files={'-o': 'rmsd.xvg'},
            stdin='Backbone Backbone\n'
        )
        subgraph.min_rms = numeric_min(
            xvg_to_array(rmsd.output.file['-o']).output.data).output.data
        subgraph.found_native = less_than(lhs=subgraph.min_rms, rhs=0.3).output.data

    folding_loop = gmx.while_loop(operation=subgraph,
                                  condition=logical_not(subgraph.found_native))()
    folding_loop.run()
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
