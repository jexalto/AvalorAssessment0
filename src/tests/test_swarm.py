# --- Built-ins ---
from pathlib import Path
import os
import unittest
import copy

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.findpath_swarm_circular import FindPathSwarm
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.tests.inputs import testinputs

# --- External ---
import numpy as np

BASE_DIR = Path(__file__).parents[1]
MIN_VALUE = -100001

class TestGrid(unittest.TestCase):
    def test_swarm(self):
        total_time = 2 # this is a single timestep, it's assumed that timestep one is used to distribute the drones over the initial 8 squares.
        _, grid, drone, total_time = testinputs()
        dronegrid0 = DroneGridInfo( drone=DroneInfo(name='Drone0_section0', 
                                                    starting_point=np.add([3, 3], 0)), 
                                    grid=grid)
        dronegrid1 = DroneGridInfo( drone=DroneInfo(name='Drone1_section1', 
                                                    starting_point=np.add([5, 6], 0)), 
                                    grid=grid)
        dronegrid2 = DroneGridInfo( drone=DroneInfo(name='Drone2_section2', 
                                                    starting_point=np.add([8, 10], 0)), 
                                    grid=grid)
        dronegrid3 = DroneGridInfo( drone=DroneInfo(name='Drone3_section3', 
                                                    starting_point=np.add([10,10], 0)), 
                                    grid=grid)
        
        # TODO: horrible coding convention but i ran into memory reference issues
        drone_properties = [dronegrid0,
                            dronegrid1,
                            dronegrid2,
                            dronegrid3]

        pathfinder = FindPathSwarm(dronegrid_properties=drone_properties)
        pathfinder.findpath(total_time=total_time)
        
        # === Test whether correct circles were assigned to correct drones ===
        self.assertDictEqual(pathfinder.circle_drone_index, {0:0, 1:1, 2:2, 3:3})