# --- Built-ins ---
from pathlib import Path
import sys, os
import unittest

# sys.path.append(os.path.join(Path(__file__).parents[2]))

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.pathproperties import DroneProperties

# --- External ---
import numpy as np

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
    
    def test_surrounding_values(self):
        '''
            Test whether surrounding values are found correctly.
        '''
        _, grid, drone = self.inputs()
        
        coords = [[0,0], [19, 0], [0, 19], [19,19], [3,2]]
        
        for icoords in coords:
            
            drone.move_drone(coords_new=icoords)
        
            pathfinder = DroneProperties(drone=drone, grid=grid, total_time=self.total_time)
            surrounding_values=pathfinder.get_surrounding_values()

            self.assertEqual(len(surrounding_values), 8)
            
    def test_findpath_greedy(self):
        '''
            Test whether the algorithm returns the correct quadrants of the matrix and their score.
        '''
        _, grid, drone = self.inputs()
        
        drone_lst = [drone, drone, drone, drone, drone, drone, drone, drone]
        
        pathfinder = DroneProperties(drone=drone, grid=grid, total_time=self.total_time)