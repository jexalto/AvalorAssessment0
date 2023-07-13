# --- Built-ins ---
from pathlib import Path
import sys, os
import unittest

# --- Internal ---
from src.tests.inputs import testinputs
from src.algorithms.utils.tools import divide_grid_circular, create_circular_grids

# --- External ---
import numpy as np

BASE_DIR = Path(__file__).parents[1]

class TestGrid(unittest.TestCase):
    def divided_grid_output(self):
        nr_drones = 4
        coords, grid, drone, total_time = testinputs()
        return divide_grid_circular(nr_drones=nr_drones, grid=grid)
        
    def test_circular_distr(self):
        radii = self.divided_grid_output()
        
        self.assertEqual(radii, [0, 2, 5, 7, 10])
        
    def test_create_circular_grids(self):
        '''
            Check whether circular grids are properly generated
        '''
        radii = self.divided_grid_output()
        coords, grid, drone, total_time = testinputs()
        grid.gridshape = np.linspace(1, 400, 400).reshape(grid.size)
        
        circular_grids = create_circular_grids(radii=radii, grid=grid)
        
        for index, circular_grid in enumerate(circular_grids):
            
            self.assertAlmostEqual(circular_grid.gridshape[radii[index], radii[index]],\
                                   grid.gridshape[radii[index], radii[index]])