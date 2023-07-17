# --- Built-ins ---
from pathlib import Path
import sys, os
import unittest

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.tests.inputs import testinputs

# --- External ---
import numpy as np

class TestGrid(unittest.TestCase):    
    def test_update_grid_to_zero(self):
        '''
            Test whether values get set to zero
        '''

        coords, grid, _, total_time = testinputs()
        x_coord, y_coord = coords
        
        grid.drone_moved_to_square(coords=[x_coord, y_coord], time=0)
        
        self.assertEqual(grid.grid_multiplier[y_coord][x_coord], 0)
        
    def test_update_grid_increase(self):
        '''
            Test whether grid values increase again after being set to zero. 
            The drone moves over the diagonal from its starting position
        '''

        coords, grid, _, total_time = testinputs()
        x_coord, y_coord = coords
 
        for timestep in range(total_time):
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep], time=timestep)

            if timestep<=grid.reset_time:
                # due to numerical error (1e-12) use almostequal
                self.assertAlmostEqual(grid.grid_multiplier[y_coord][x_coord], timestep/grid.reset_time)
            
            else:
                self.assertAlmostEqual(grid.grid_multiplier[y_coord][x_coord], 1)
                
    def test_update_drone_info(self):
        '''
            Test whether grid values increase again after being set to zero. The test also assesses whether the drone path is appended
            The drone moves over the diagonal from its starting position.
        '''

        coords, grid, drone, total_time = testinputs()
        x_coord, y_coord = coords
        temp = 0
 
        for timestep in range(total_time):
            # === Move drone and retrieve square value ===
            gridvalue = grid.gridshape[x_coord+timestep][y_coord+timestep]
            drone.move_drone(coords_new=[x_coord+timestep, y_coord+timestep])
            drone.add_to_sum(square_value=gridvalue)

            # === Update grids value ===
            grid.drone_moved_to_square(coords=[x_coord+timestep, y_coord+timestep], time=1)

            # === Update unittest values ===
            temp += gridvalue

            # use almostequal due to numerical error (1e-12)
            self.assertAlmostEqual(drone.total_path_value[-1], temp)
            
            self.assertEqual(len(drone.path), timestep+2)