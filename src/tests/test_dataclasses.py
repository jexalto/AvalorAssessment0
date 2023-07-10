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
    def inputs(self):
        self.total_time = 10 # total number of timesteps
        self.reset_time = 5
        
        gridsize = 20 # this determines what file is chose. Options are: 20, 100, 1000
        coords = [3, 2]

        grid = self._grid_output(gridsize=gridsize)
        drone = DroneInfo(name='TestDrone',
                          starting_point=coords)

        return coords, grid, drone
    
    def _grid_output(self, gridsize: int):
        '''
            This is the grid input function for all test functions
        '''
        gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
        
        grid = GridInfo(name='TestGrid',
                        gridshape=np.loadtxt(gridfile, dtype='i', delimiter=' '),
                        reset_time=self.reset_time)
        
        return grid
    
    def test_update_grid_to_zero(self):
        '''
            Test whether values get set to zero
        '''

        coords, grid, _ = self.inputs()
        x_coord, y_coord = coords
        
        grid.drone_moved_to_square(coords=[x_coord, y_coord])
        
        self.assertEqual(grid.gridshape[x_coord][y_coord], 0)
        
    def test_update_grid_increase(self):
        '''
            Test whether grid values increase again after being set to zero. 
            The drone moves over the diagonal from its starting position
        '''

        coords, grid, _ = self.inputs()
        x_coord, y_coord = coords
 
        for timestep in range(self.total_time):
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep])

            if timestep<=self.reset_time:
                # due to numerical error (1e-12) use almostequal
                self.assertAlmostEqual(grid.grid_multiplier[x_coord][y_coord], timestep/self.reset_time)
            
            else:
                self.assertAlmostEqual(grid.grid_multiplier[x_coord][y_coord], 1)
                
    def test_update_drone_info(self):
        '''
            Test whether grid values increase again after being set to zero. The test also assesses whether the drone path is appended
            The drone moves over the diagonal from its starting position.
        '''

        coords, grid, drone = self.inputs()
        x_coord, y_coord = coords
        temp = 0
 
        for timestep in range(self.total_time):
            # === Move drone and retrieve square value ===
            gridvalue = grid.gridshape[x_coord+timestep][y_coord+timestep]
            drone.move_drone(coords_new=[x_coord+timestep, y_coord+timestep])
            drone.add_to_sum(square_value=gridvalue)

            # === Update grids value ===
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep])

            # === Update unittest values ===
            temp += gridvalue

            # use almostequal due to numerical error (1e-12)
            self.assertAlmostEqual(drone.total_path_value, temp)
            
            self.assertEqual(len(drone.path), timestep+2)
