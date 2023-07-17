# --- Built-ins ---
from pathlib import Path
import copy

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.tools import surrounding_values_finder

# --- External ---
import numpy as np

# TODO: replace all min_value with np.NINF
MIN_VALUE = -100001

class DroneGridInfo:
    '''
        Combines info about the grid and drones
    '''
    
    def __init__(self, drone: DroneInfo, grid: GridInfo)->None:
        self.drone = drone
        self.grid = grid
        starting_x, starting_y = self.drone.starting_point
        self.grid.grid_multiplier[starting_y][starting_x] = 0
    
    def circular_grid(self, grid: GridInfo):
        self.grid_circular = grid
    
    def get_surrounding_values(self)->list[float]:
        '''
            This function retrieves the values surrounding square x, y.
            Given as:
                1   -   2   -   3
                8   -   X   -   4
                7   -   6   -   5
            TODO: this function is inefficient, must be improved when you have time
        '''
        grid = self.grid.gridvalues
        gridshape = self.grid.size
        
        x, y = self.drone.path[-1]
        
        return surrounding_values_finder(x=x, y=y, grid=grid, gridshape=gridshape)
    
    def get_surrounding_values_circular(self)->list[float]:
        '''
            This function retrieves the values surrounding square x, y.
            Given as:
                1   -   2   -   3
                8   -   X   -   4
                7   -   6   -   5
            TODO: this function is inefficient, must be improved when you have time
        '''
        grid = self.grid_circular.gridvalues
        gridshape = self.grid.size
        
        x, y = self.drone.path[-1]
        
        return surrounding_values_finder(x=x, y=y, grid=grid, gridshape=gridshape)
    
    def distance_to_circle(self, radii: list[int])->int:
        '''
            Returns the index of the circle that a particular drone is closest to
        '''
        min_distance = []

        # === Mirror drone locations on the second half of the grid in either x or y direction ===
        droneloc = copy.deepcopy(self.drone.path[-1])
        
        gridsize = self.grid.size[0]
        
        for index, coord in enumerate(droneloc):
            if coord>gridsize/2:
                droneloc[index] = gridsize-coord

        x_distance, y_distance = self._distances(radii=radii, droneloc=droneloc)
        
        for x, y in zip(x_distance, y_distance):
            min_distance.append(min(x, y))
            
        return min_distance # the first radius doesn't count because it's the edge, so +1
    
    def drone_direction(self, radii: list[int], radius_index: int)->list[int]:
        '''
            In what direction should a drone move to end up in its assigned circular section.
        '''
        drone_in_section = False
        
        gridsize = self.grid.size[0]
        
        indices = [radii[radius_index], radii[radius_index+1]]
        droneloc = self.drone.path[-1]
        
        if self.grid_circular.gridvalues[droneloc[0]][droneloc[1]] != MIN_VALUE:
            drone_in_section = True
            direction = [0, 0]
            
        else:
            # === Find what x-direction to move the drone to ===
            x_locs_circular_section = np.array([radii[radius_index], radii[radius_index+1], gridsize-radii[radius_index+1], gridsize-radii[radius_index]])
            x_distance = np.subtract(x_locs_circular_section, droneloc[0])
            min_x_distance = np.min(x_distance)
            
            y_locs_circular_section = np.array([radii[radius_index], radii[radius_index+1], gridsize-radii[radius_index+1], gridsize-radii[radius_index]])
            y_distance = np.subtract(y_locs_circular_section, droneloc[1])
            min_y_distance = np.min(y_distance)
            
            if np.argmin([min_x_distance, min_y_distance]):
                # y-direction movement
                min_y_index = np.argmin(y_distance)
                if min_y_index==0 or min_y_distance==2:
                    # move down
                    direction = [0, -1]
                else:
                    # move up
                    direction = [0, 1]

            else:
                # x-direction movement
                min_x_index = np.argmin(x_distance)
                if min_x_index==0 or min_x_distance==2:
                    # move right
                    direction = [1, 0]
                else:
                    # move left
                    direction = [-1, 0]
        
        return drone_in_section, direction
    
    def _distances(self, radii: list[int], droneloc: list[int])->list[list[int]]:
        return abs(np.subtract(radii[1:], droneloc[0])), abs(np.subtract(radii[1:], droneloc[1]))