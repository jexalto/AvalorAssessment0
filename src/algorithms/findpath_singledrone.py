# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np

MIN_VALUE = -100001

class FindPathSingleDrone:
    
    def __init__(self, drone: DroneInfo, grid: GridInfo, total_time: int):
        self.drone = drone
        self.grid = grid
        self.total_time = total_time
    
    def findpath(self, coords:list[int])->list[list[int]]:
        '''
            Coordinates look like this:
                    x - >
            
                0,0 - 0,1 - .,. - 0,n
            y   1,0 - .,. - .,. - 1,n
            |   .,. - .,. - .,. - .,.
            v   .,. - .,. - .,. - .,.
                n,0 - .,. - .,. - n,n
        '''
        surrounding_values = self._get_surrounding_values(coords=coords)
        return surrounding_values
    
    def _get_surrounding_values(self, coords: list[int])->list[float]:
        '''
            This function retrieves the values surrounding square x, y.
            Given as:
                1   -   2   -   3
                8   -   X   -   4
                7   -   6   -   5
            TODO: this function looks inefficient, must be improved when you have time
        '''
        surrounding_values = []
        grid = self.grid.gridshape
        gridshape = self.grid.size
        
        x, y = coords
        
        # === Check whether x, y are at the edge of the matrix ===
        if x==0:
            if y==0:
                # Location is top left of matrix
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y]   [x+1])
                surrounding_values.append(grid[y+1] [x+1])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE])
                
            if y==gridshape[1]-1:
                # Location is bottom left of matrix
                surrounding_values.extend([MIN_VALUE])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.append(grid[y-1] [x-1])
                surrounding_values.append(grid[y]   [x-1])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
        
        elif x==gridshape[1]-1:
            if y==0:
                # Location is top right of matrix
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.append(grid[y+1] [x-1])
                surrounding_values.append(grid[y]   [x-1])
                
            if y==gridshape[1]-1:
                # Location is bottom right of matrix
                surrounding_values.append(grid[y-1] [x-1])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y]   [x-1])

        else:
            surrounding_values.append(grid[y-1][x-1])
            surrounding_values.append(grid[y-1][x])
            surrounding_values.append(grid[y-1][x+1])
            surrounding_values.append(grid[y][x+1])
            surrounding_values.append(grid[y+1][x+1])
            surrounding_values.append(grid[y+1][x])
            surrounding_values.append(grid[y+1][x-1])
            surrounding_values.append(grid[y][x-1])
            
        return surrounding_values