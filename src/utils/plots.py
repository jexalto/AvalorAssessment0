# --- Built-ins ---
import os
from pathlib import Path
import copy

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.algorithms.findpath_singledrone import FindPathGreedy
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parents[1]

def inputs():
    coords = [2, 2]

    drone = DroneInfo(name='TestDrone',
                        starting_point=coords)

    return coords, drone

def dronepathplots(dronegrid: DroneGridInfo)->None:
    x, y = [], []
    path = dronegrid.drone.path
    x_starting, y_starting = dronegrid.drone.starting_point

    for ipath in path:
        x.append(ipath[0])
        y.append(ipath[1])
        
    plt.plot(x, y, label='Drone Path', linewidth=3, color='black')
    plt.scatter(x_starting, y_starting, marker='x', color='black', linewidth=2, label='Starting point')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def plotgrid(grid: GridInfo)->None:
    # Make a 9x9 grid...
    nrows, ncols = grid.size
    image = np.zeros(nrows*ncols)

    # Set every other cell to a random number (this would be your data)
    image[::1] = grid.gridshape.flatten()

    # Reshape things into a 9x9 grid.
    image = image.reshape((nrows, ncols))

    row_labels = range(nrows)
    col_labels = range(nrows)
    fig = plt.figure(figsize=(10, 8), dpi=120)
    ax = fig.add_subplot(111)
    
    # === Print values in squares ===
    for irow in range(nrows):
        for icol in range(ncols):
            if grid.gridshape[irow, icol]==2:
                color='black'
            else:
                color='w'
            text = ax.text(icol, irow, grid.gridshape[irow, icol],
                    ha="center", va="center", color=color)
            
    cax = ax.matshow(image, )
    # fig.colorbar(cax)
    plt.xticks(range(ncols), col_labels)
    plt.yticks(range(nrows), row_labels)
    # plt.show()
    
if __name__=='__main__':
    gridsize = 20
    gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
        
    grid = GridInfo(name='TestGrid',
                    gridshape=np.loadtxt(gridfile, dtype='i', delimiter=' '),
                    reset_time=5)
    
    total_time = 10
    coords, drone = inputs()
    dronegrid = DroneGridInfo(drone=drone, grid=grid, total_time=total_time),
    
    # TODO: horrible coding convention but i ran into memory reference issues
    drone_properties = [copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0],
                        copy.deepcopy(dronegrid)[0]]

    pathfinder = FindPathGreedy(dronegrid_properties=drone_properties)
    drone_maxpath = pathfinder.find_path(total_time=total_time)
    
    plotgrid(grid=grid)
    dronepathplots(dronegrid=drone_maxpath)
    plt.savefig(os.path.join(BASE_DIR, 'data', 'figures', f'grid_{gridsize}.png'))
    plt.show()