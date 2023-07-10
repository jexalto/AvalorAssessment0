# --- Built-ins ---
from pathlib import Path
import sys, os
import unittest

sys.path.append(os.path.join(Path(__file__).parents[2]))

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).parents[1]

class TestGrid(unittest.TestCase):
    def gridmatrix(self, filepath: str):
        '''
            Function returns matrix, read in from ..data/grids/
        '''
        return np.loadtxt(filepath, dtype='i', delimiter=' ')
    
    def grid_output(self):
        '''
            This is the input function for all test functions
        '''
        gridsize = 20 # this determines what file is chose. Options are: 20, 100, 1000
        gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
        coords = [3, 2] # this location holds the value '2' in the original matrix
        self.total_time = 10 # total number of timesteps
        self.reset_time = 5
        
        grid = GridInfo(name='TestGrid',
                        gridshape=self.gridmatrix(filepath=gridfile),
                        reset_time=self.reset_time)
        
        return coords, grid
    
    def test_update_grid_to_zero(self):
        '''
            Test whether values get set to zero
        '''

        coords, grid = self.grid_output()
        x_coord, y_coord = coords
        
        grid.drone_moved_to_square(coords=[x_coord, y_coord])
        
        self.assertEqual(grid.gridshape[x_coord][y_coord], 0)
        
    def test_update_grid_increase(self):
        '''
            Test whether grid values increase again after being set to zero. 
            The drone moves over the diagonal from its starting position
        '''

        coords, grid = self.grid_output()
        x_coord, y_coord = coords
 
        for timestep in range(self.total_time):
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep])

            if timestep<=self.reset_time:
                # due to numerical error (1e-12) use almostequal
                self.assertAlmostEqual(grid.grid_multiplier[x_coord][y_coord], timestep/self.reset_time)
            
            else:
                self.assertAlmostEqual(grid.grid_multiplier[x_coord][y_coord], 1)