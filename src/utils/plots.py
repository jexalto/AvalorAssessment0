# --- Built-ins ---
import os
from pathlib import Path
import copy

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.algorithms.findpath_singledrone_twolayers import FindPathGreedyTwoLayers
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE_DIR = Path(__file__).parents[1]

def inputs():
    coords = [3, 3]

    drone = DroneInfo(name='TestDrone',
                        starting_point=coords)

    return coords, drone

def dronepathplots(ax, dronegrid: DroneGridInfo)->None:
    x, y = [], []
    path = dronegrid.drone.path
    x_starting, y_starting = dronegrid.drone.starting_point

    for ipath in path:
        x.append(ipath[0])
        y.append(ipath[1])
    
    width=1
    height=1
    
    ax.add_patch(Rectangle((x_starting-width/2, y_starting-height/2), width, height,
                    edgecolor = 'pink',
                    fill=False,
                    lw=2),
                )
    plt.plot(x, y, label='Drone Path', linewidth=3, color='black')
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
            
    cax = ax.matshow(image)
    # fig.colorbar(cax)
    plt.xticks(range(ncols), col_labels)
    plt.yticks(range(nrows), row_labels)
    # plt.show()
    return fig, ax

def draw_regions(ax, coords: list[int], len_radii: int, gridsize: int)->None:
    x_coords, y_coords = coords
    for index in range(len_radii-1):
        x_starting, y_starting = round(gridsize/2)-0.5, round(gridsize/2)-0.5
        width = x_coords[index][1]-x_coords[index][0]
        height = y_coords[index][2]-y_coords[index][1]
        ax.add_patch(Rectangle((x_starting-width/2, y_starting-height/2), width, height,
                        edgecolor = 'white',
                        fill=False,
                        lw=3),
                    )
    
if False:#__name__!='__main__':
    gridsize = 20
    gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
        
    grid = GridInfo(name='TestGrid',
                    gridshape=np.loadtxt(gridfile, dtype='i', delimiter=' '),
                    reset_time=10)
    
    total_time = 40
    coords, drone = inputs()
    dronegrid = DroneGridInfo(drone=drone, grid=grid),
    
    # TODO: horrible coding convention but i ran into memory reference issues
    dronegrid_properties = [copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0],
                            copy.deepcopy(dronegrid)[0]]

    pathfinder = FindPathGreedyTwoLayers(dronegrid_properties=dronegrid_properties)
    # all_paths = pathfinder._process_paths(total_time=total_time)
    # pathfinder._initialise(dronegrid_properties=dronegrid_properties)
    # pathfinder._reset_drone(dronegrid_properties=dronegrid_properties)
    drone_maxpath = pathfinder.find_path(total_time=total_time)
    
    index=0
    
    path = drone_maxpath#all_paths[index]
    
    fig, ax = plotgrid(grid=grid)
    dronepathplots(ax=ax, dronegrid=path)
    plt.title(f'Max Sum: {path.drone.total_path_value}')
    plt.savefig(os.path.join(BASE_DIR, 'data', 'figures', f'grid_{gridsize}_{index}.png'))
    plt.show()