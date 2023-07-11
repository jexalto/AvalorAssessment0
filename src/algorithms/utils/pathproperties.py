# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np

MIN_VALUE = -100001

class DroneGridInfo:
    '''
        This approach is based on the fact that 10 squares with a value of one, that are all reachable within one step are 
        equally valuable as a single square with value 10 that is 10 steps away.
        An analogy is drawn with the gravitational pull of planets, although gravity scales with r^2
    '''
    
    def __init__(self, drone: DroneInfo, grid: GridInfo, total_time: int)->None:
        self.drone = drone
        self.grid = grid
        self.total_time = total_time
    
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
        grid = self.grid.gridshape
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
                surrounding_values.append(grid[y-1] [x-1])
                surrounding_values.append(grid[y]   [x-1])
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