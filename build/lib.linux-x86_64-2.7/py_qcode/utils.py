import cPickle as pkl

from simulation import Simulation
from lattice import SquareLattice
from error import depolarizing_model
from decoder import mwpm_decoder
from code import toric_code
from logical_operators import toric_log_ops

import cPickle as pkl

__all__ = ['sim_from_file', 'square_toric_code_sim']

def sim_from_file(filename):
    """
    The purpose of this function is to:

    + open a file containing a pickled dictionary of input values to a simulation,

    + initialize the objects which the corresponding `py_qcode.Simulation` takes as input,
    
    + run the simulation, and 

    + save the results to a file of the same name as the input, with a different extension.  
    """
    with open(filename,'r') as phil:
        sim_dict = pkl.load(phil)
    sim = Simulation(**sim_dict)
    sim.run()

    split_name = filename.split('.')
    try:
        file_prefix, file_ext = split_name
    except ValueError:
        raise ValueError('Filenames are assumed to be of the form'+\
        ' "prefix.ext".')

    output_name = '.'.join([file_prefix, 'out'])

    sim.save(output_name)

def square_toric_code_sim(size, error_rate, n_trials, filename):
    """
    This function is square in more than one sense; it does everything
    the most vanilla way possible, and it uses a square grid to define 
    the torus. You put in an integer size, an error rate and a number
    of trials to execute, and it produces a pickled dict containing 
    the input to a simulation object in a file.
    """
    
    sim_lattice = SquareLattice((size,size))
    sim_dual_lattice = SquareLattice((size,size), is_dual=True)
    sim_model = depolarizing_model(error_rate)
    sim_code = toric_code(sim_lattice, sim_dual_lattice)
    sim_decoder = mwpm_decoder(sim_lattice, sim_dual_lattice)
    sim_log_ops = toric_log_ops((size,size))

    sim_keys = ['lattice', 'dual_lattice', 'error_model', 'code', 
                            'decoder', 'logical_operators', 'n_trials']

    sim_values = [sim_lattice, sim_dual_lattice, sim_model, sim_code, 
                                sim_decoder, sim_log_ops, n_trials]
    
    sim_dict = dict(zip(sim_keys, sim_values))

    with open(filename, 'w') as phil:
        pkl.dump(sim_dict, phil)