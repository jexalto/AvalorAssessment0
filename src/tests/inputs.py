# --- Built-ins ---
from pathlib import Path
import os
import unittest
import copy

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np

BASE_DIR = Path(__file__).parents[1]

def testinputs():
    total_time = 30 # total number of timesteps
    reset_time = 15
    
    gridsize = 20 # this determines what file is chose. Options are: 20, 100, 1000
    coords = [3, 3]

    grid = _grid_output(gridsize=gridsize, reset_time=reset_time)
    drone = DroneInfo(name='TestDrone',
                        starting_point=coords)

    return coords, grid, drone, total_time
    
def _grid_output(gridsize: int, reset_time: int):
    '''
        This is the grid input function for all test functions
    '''
    gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
    
    grid = GridInfo(name='TestGrid',
                    gridshape=np.loadtxt(gridfile, dtype='i', delimiter=' '),
                    reset_time=reset_time)
    
    return grid