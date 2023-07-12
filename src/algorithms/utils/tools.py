# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np

MIN_VALUE = -100001

def surrounding_values_finder(x: int, y: int, grid: np.array, gridshape: tuple)->list[float]:
    surrounding_values = []

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