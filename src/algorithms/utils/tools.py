# --- Built-ins ---
import copy

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np

MIN_VALUE = -100001
π = 3.14159265358979

def surrounding_values_finder(x: int, y: int, grid: np.array, gridshape: tuple)->list[float]:
    surrounding_values = []

    # === Check whether x, y are at the edge of the matrix ===
    if x<=0:
        if y<=0:
            # Location is top left of matrix
            surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
            surrounding_values.append(grid[y]   [x+1])
            surrounding_values.append(grid[y+1] [x+1])
            surrounding_values.append(grid[y+1] [x])
            surrounding_values.extend([MIN_VALUE, MIN_VALUE])
            
        elif y>=gridshape[1]-1:
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
    
    elif x>=gridshape[1]-1:
        if y<=0:
            # Location is top right of matrix
            surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE, MIN_VALUE])
            surrounding_values.append(grid[y+1] [x])
            surrounding_values.append(grid[y+1] [x-1])
            surrounding_values.append(grid[y]   [x-1])
            
        elif y>=gridshape[1]-1:
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

    elif y<=0:
        # Location is top row
        surrounding_values.extend([MIN_VALUE, MIN_VALUE, MIN_VALUE])
        surrounding_values.append(grid[y]   [x+1])
        surrounding_values.append(grid[y+1] [x+1])
        surrounding_values.append(grid[y+1] [x])
        surrounding_values.append(grid[y+1] [x-1])
        surrounding_values.append(grid[y]   [x-1])
    
    elif y>=gridshape[1]-1:
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

def divide_grid_circular(nr_drones: int, grid: GridInfo)-> list[int]:
    '''
        Function that divides the grid into a number of circular sections with equal area.
        Obviously it isn't actually circular because we work with a grid
    '''
    gridsize = grid.size
    radius = gridsize[0]/2
    radius_partial = radius/(nr_drones)
    
    # round off to integers because we'll use these as indices
    radii = [int(radius_partial*i) for i in range(0, nr_drones)]
    radii.append(int(radius))

    return radii

def create_circular_grids(radii: list[int], grid: GridInfo)->list[GridInfo]:
    original_grid = copy.deepcopy(grid)
    original_grid_values = original_grid.gridshape
    original_grid_size = original_grid.size
    
    new_grids = []
    
    for index in range(len(radii)-1):
        grid_values = np.ones(original_grid_size)*MIN_VALUE

        # assign values to the top side of the rectangle
        grid_values[radii[index]:   radii[index+1], radii[index]:  original_grid_size[0]-radii[index]] = \
            original_grid_values[radii[index]:   radii[index+1], radii[index]:  original_grid_size[0]-radii[index]]
        
        # assign values to the right vertical side of the rectangle
        grid_values[radii[index+1]: original_grid_size[0]-radii[index+1], original_grid_size[0]-radii[index+1]:original_grid_size[0]-radii[index]] = \
            original_grid_values[radii[index+1]: original_grid_size[0]-radii[index+1], original_grid_size[0]-radii[index+1]:original_grid_size[0]-radii[index]]
        
        # assign values to the bottom of the rectangle
        grid_values[original_grid_size[0]-radii[index+1]:   original_grid_size[0]-radii[index], radii[index]:  original_grid_size[0]-radii[index]] = \
            original_grid_values[original_grid_size[0]-radii[index+1]:   original_grid_size[0]-radii[index], radii[index]:  original_grid_size[0]-radii[index]]
        
        # assign values to the left vertical side of the rectangle
        grid_values[radii[index+1]: original_grid_size[0]-radii[index+1], radii[index]:radii[index+1]] = \
            original_grid_values[radii[index+1]: original_grid_size[0]-radii[index+1], radii[index]:radii[index+1]]
            
        new_grids.append(GridInfo(name=f'Grid{index}',
                                  gridshape=grid_values,
                                  reset_time=original_grid.reset_time))
            
    return new_grids