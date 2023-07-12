# --- Built-ins ---
from pathlib import Path
import os
import unittest
import copy

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.findpath_singledrone_twolayers import FindPathGreedyTwoLayers
from src.algorithms.utils.pathproperties import DroneGridInfo

# --- External ---
import numpy as np

BASE_DIR = Path(__file__).parents[1]
MIN_VALUE = -100001

class TestGrid(unittest.TestCase):
    def inputs(self):
        self.total_time = 30 # total number of timesteps
        self.reset_time = 5
        
        gridsize = 20 # this determines what file is chose. Options are: 20, 100, 1000
        coords = [3, 3]

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
            Test whether surrounding values are found correctly. Correct values were retrieved from the gridsize=20 array.
        '''
        _, grid, drone = self.inputs()
        
        coords = [[0,0], [19, 0], [0, 19], [19,19], [3,2]]
        
        surrounding_values_correct = [[MIN_VALUE, MIN_VALUE, MIN_VALUE, 0, 0, 1, MIN_VALUE, MIN_VALUE],
                                      [MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, 0, 2, 2],
                                      [MIN_VALUE, 2, 0, 1, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE],
                                      [0, 1, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, 2],
                                      [2, 1, 1, 1, 2, 1, 2, 2]]
        
        for index, icoords in enumerate(coords):
            
            drone.move_drone(coords_new=icoords)
        
            pathfinder = DroneGridInfo(drone=drone, grid=grid)
            surrounding_values = pathfinder.get_surrounding_values()

            self.assertEqual(len(surrounding_values), 8)
            self.assertEqual(surrounding_values, surrounding_values_correct[index])
            
    def test_drone_instances(self):
        '''
            Test whether the algorithm returns the correct grid multiplier matrices for the 8 distinct
            drone instances used to find the maximum path.
            Test for one time step!
        '''
        total_time = 2 # this is a single timestep, it's assumed that timestep one is used to distribute the drones over the initial 8 squares.
        _, grid, drone = self.inputs()
        dronegrid = DroneGridInfo(drone=drone, grid=grid)
        
        # TODO: horrible coding convention but i ran into memory reference issues
        drone_properties = [copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid)]

        pathfinder = FindPathGreedyTwoLayers(dronegrid_properties=drone_properties)
        dronegrid_properties_final = pathfinder._process_paths(total_time=total_time)
        
        # === Check whether all grid multiplication matrices have the correct number of zero's and 0.2's ===
        for idrongegrid in dronegrid_properties_final:
            grid_multiplier = idrongegrid.grid.grid_multiplier
            
            self.assertAlmostEqual(len(np.where(grid_multiplier==0)[0]), 1)
            self.assertAlmostEqual(len(np.where(grid_multiplier==0.2)[0]), 1)
            
    def test_find_path(self):
        total_time = 30
        _, grid, drone = self.inputs()
        dronegrid = DroneGridInfo(drone=drone, grid=grid),
        
        # TODO: horrible coding convention but i ran into memory reference issues
        drone_properties = [copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0]]

        pathfinder = FindPathGreedyTwoLayers(dronegrid_properties=drone_properties)
        drone_maxpath = pathfinder.find_path(total_time=total_time)
        
        self.assertAlmostEqual(len(drone_maxpath.drone.path)-1, total_time)