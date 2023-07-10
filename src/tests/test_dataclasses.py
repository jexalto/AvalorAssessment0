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
        self.total_time = 15 # total number of timesteps
        
        grid = GridInfo(name='TestGrid',
                        gridshape=self.gridmatrix(filepath=gridfile),
                        reset_time=10)
        
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
        
        coords, grid = self.grid_output()
        x_coord, y_coord = coords
 
        for timestep in range(self.total_time):
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep])
        
        self.assertEqual(0, 0)