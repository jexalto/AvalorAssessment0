# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.tools import surrounding_values_finder

# --- External ---
import numpy as np

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
    
    def distance_to_circle(self, radii: list[int])->int:
        '''
            Returns the index of the circle that a particular drone is closest to
        '''
        min_distance = []

        droneloc = self.drone.path[-1]
        
        x_distance = abs(np.subtract(radii[1:], droneloc[0]))
        y_distance = abs(np.subtract(radii[1:], droneloc[1]))
        
        for x, y in zip(x_distance, y_distance):
            min_distance.append(min(x, y))
            
        return min_distance # the first radius doesn't count because it's the edge, so +1