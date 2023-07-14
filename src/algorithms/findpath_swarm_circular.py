# --- Built-ins ---
import sys, os

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.algorithms.findpath_singledrone_twolayers import FindPathGreedyTwoLayers
from src.algorithms.utils.tools import divide_grid_circular, create_circular_grids

# --- External ---
import numpy as np


class FindPathSwarm:
    def __init__(self, dronegrid_properties: list[DroneGridInfo]):
        # === Initialise drones on grid and set starting point grid value to zero ===
        self._initialise(dronegrid_properties=dronegrid_properties)
        self.nr_drones = len(dronegrid_properties)
        
    def _initialise(self, dronegrid_properties: list[DroneGridInfo])->None:
        starting_x, starting_y = dronegrid_properties[0].drone.starting_point
        for idronegrid in dronegrid_properties:
            idronegrid.grid.reset()
            # When initialising the dorne on the grid the multiplier should be set to zero for the starting position
            # TODO: integrate this in the drone-grid initialisation
            idronegrid.grid.grid_multiplier[starting_y][starting_x] = 0
            
        self.dronegrid_properties = dronegrid_properties
        
    def _reset_drone(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.drone.reset()
    
    def findpath(self)->DroneInfo:
        pass
    
    def _process_path(self)->list[DroneGridInfo]:
        self._find_closest_circle()
        self._move_drone_to_section()
    
    def _find_closest_circle(self)->dict:
        '''
            Move drone to closest circle
        '''
        
        # === Find drone circular grid combinations ===
        distances_drones_circles = []

        for drone in self.dronegrid_properties:
            radii = divide_grid_circular(nr_drones=self.nr_drones, grid=drone.grid)
            circular_grids = create_circular_grids(radii=radii, grid=drone.grid)
            
            distances_drones_circles.append(drone.distance_to_circle(radii=radii))

        drone_circle_pairs = {}
        
        for circle_index in range(len(radii)-1):
            distances = []
            for distance in distances_drones_circles:
                distances.append(distance[circle_index])
            closest_drone = np.argmin(distances)
            
            drone_circle_pairs[circle_index+closest_drone] = circle_index
            
            distances_drones_circles.remove(distances_drones_circles[closest_drone])
        
        self.drone_circle_pairs = drone_circle_pairs
        
        # === Give circular grid to respective drone ===
        for drone_index, drone in enumerate(self.dronegrid_properties):
            drone.circular_grid(grid=circular_grids[drone_circle_pairs[drone_index]])
    
    def _move_drone_to_section(self):
        '''
            Move drone to its assigned circular section
        '''
        for drone_index, drone in enumerate(self.dronegrid_properties):
            radii = divide_grid_circular(nr_drones=self.nr_drones, grid=drone.grid)
            radius_index = self.drone_circle_pairs[drone_index]
            drone.drone_direction(radii=radii, radius_index=radius_index)
        