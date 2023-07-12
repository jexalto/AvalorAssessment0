# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo

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
    
    def get_surrounding_values(self)->list[float]:
        '''
            This function retrieves the values surrounding square x, y.
            Given as:
                1   -   2   -   3
                8   -   X   -   4
                7   -   6   -   5
            TODO: this function looks inefficient, must be improved when you have time
        '''
        surrounding_values = []
        grid = self.grid.gridvalues
        gridshape = self.grid.size
        
        x, y = self.drone.path[-1]
        
        # === Check whether x, y are at the edge of the matrix ===
        if x==0:
            if y==0:
                # Location is top left of matrix
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y]   [x+1])
                surrounding_values.append(grid[y+1] [x+1])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE])
                
            elif y==gridshape[1]-1:
                # Location is bottom left of matrix
                surrounding_values.extend([MIN_VALUE])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.append(grid[y-1] [x+1])
                surrounding_values.append(grid[y]   [x+1])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
                
            else:
                # Location is somewhere in the left column
                surrounding_values.extend([MIN_VALUE])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.append(grid[y-1] [x+1])
                surrounding_values.append(grid[y]   [x+1])
                surrounding_values.append(grid[y+1] [x+1])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE])
        
        elif x==gridshape[1]-1:
            if y==0:
                # Location is top right of matrix
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.append(grid[y+1] [x-1])
                surrounding_values.append(grid[y]   [x-1])
                
            elif y==gridshape[1]-1:
                # Location is bottom right of matrix
                surrounding_values.append(grid[y-1] [x-1])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y]   [x-1])
                
            else:
                # Location is somewhere in the left column
                surrounding_values.append(grid[y-1] [x-1])
                surrounding_values.append(grid[y-1] [x])
                surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
                surrounding_values.append(grid[y+1] [x])
                surrounding_values.append(grid[y+1] [x-1])
                surrounding_values.append(grid[y]   [x-1])

        elif y==0:
            # Location is top row
            surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
            surrounding_values.append(grid[y]   [x+1])
            surrounding_values.append(grid[y+1] [x+1])
            surrounding_values.append(grid[y+1] [x])
            surrounding_values.append(grid[y+1] [x-1])
            surrounding_values.append(grid[y]   [x-1])
        
        elif y==gridshape[1]-1:
            # Location is bottom row
            surrounding_values.append(grid[y-1] [x-1])
            surrounding_values.append(grid[y-1] [x])
            surrounding_values.append(grid[y-1] [x+1])
            surrounding_values.append(grid[y]   [x-1])
            surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
            surrounding_values.append(grid[y]   [x-1])
          
        else:
            # Location is anywhere in the grid
            surrounding_values.append(grid[y-1][x-1])
            surrounding_values.append(grid[y-1][x])
            surrounding_values.append(grid[y-1][x+1])
            surrounding_values.append(grid[y][x+1])
            surrounding_values.append(grid[y+1][x+1])
            surrounding_values.append(grid[y+1][x])
            surrounding_values.append(grid[y+1][x-1])
            surrounding_values.append(grid[y][x-1])
            
        return surrounding_values