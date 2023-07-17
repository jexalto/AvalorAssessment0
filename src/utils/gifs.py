# --- Built-ins ---
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import copy

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.algorithms.findpath_singledrone_twolayers import FindPathGreedyTwoLayersGifs
from src.algorithms.findpath_singledrone_onelayer import FindPathGreedySingleLayerGifs
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import imageio

BASE_DIR = Path(__file__).parents[1]

def dronepathplots(ax, path: list[int], starting_point: list[int])->None:
    x, y = [], []
    x_starting, y_starting = starting_point

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
    image[::1] = grid.gridvalues.flatten()

    # Reshape things into a 9x9 grid.
    image = image.reshape((nrows, ncols))

    row_labels = range(nrows)
    col_labels = range(nrows)
    fig = plt.figure(figsize=(10, 8), dpi=120)
    ax = fig.add_subplot(111)
    
    # === Print values in squares ===
    for irow in range(nrows):
        for icol in range(ncols):
            if grid.gridvalues[irow, icol]>1:
                color='black'
            else:
                color='w'
            text = ax.text(icol, irow, np.round(grid.gridvalues[irow, icol],1),
                    ha="center", va="center", color=color)
            
    cax = ax.matshow(image, interpolation='none', vmin=0, vmax=2)
    # fig.colorbar(cax)
    plt.xticks(range(ncols), col_labels)
    plt.yticks(range(nrows), row_labels)
    # plt.show()
    return fig, ax

def make_gif(picture_dir: str, framestop: int, output_dir: str, total_time: int, gridsize: int):    
    filenames = [join(picture_dir, f'grid_{gridsize}_{f}.png') for f in range(total_time) if isfile(join(picture_dir,  f'grid_{gridsize}_{f}.png'))]
    
    with imageio.get_writer(join(output_dir, f'video_grid{gridsize}_time{total_time}.gif'), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            for i in range(framestop):
                writer.append_data(image)
    
if __name__=='__main__':
    gridsize = 20
    total_time = 30
    reset_time = 10
    starting_coords = [3, 3]
    
    drone = DroneInfo(name='TestDrone',
                        starting_point=starting_coords)
    
    gridfile = os.path.join(BASE_DIR, 'data', 'grids', f'{gridsize}.txt')
    grid = GridInfo(name='TestGrid',
                    gridshape=np.loadtxt(gridfile, dtype='i', delimiter=' '),
                    reset_time=reset_time)
    
    dronegrid = DroneGridInfo(drone=drone, grid=grid)

    # TODO: horrible coding convention but i ran into memory reference issues
    dronegrid_properties = [copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid),
                            copy.deepcopy(dronegrid)]

    pathfinder = FindPathGreedyTwoLayersGifs(dronegrid_properties=dronegrid_properties)
    path, maxpath_index, grids = pathfinder.find_path(total_time=total_time)
    
    gifpath = []
        
    for index, path_coords in enumerate(path.drone.path):
        gifpath.append(path_coords)
        
        fig, ax = plotgrid(grid=grids[index])
        dronepathplots(ax=ax, path=gifpath, starting_point=path.drone.starting_point)

        plt.title(f'Max Sum: {path.drone.total_path_value[index+1]}')
        plt.savefig(os.path.join(BASE_DIR, 'data', 'gifs', 'figures', f'grid_{gridsize}_{index}.png'))
        plt.clf()
    
    dirpath = join(BASE_DIR, 'data', 'gifs', 'figures')
    filenames = [join(dirpath, f'grid_{gridsize}_{f}.png') for f in range(index) if isfile(join(dirpath,  f'grid_{gridsize}_{f}.png'))]
    
    with imageio.get_writer(join(BASE_DIR, 'data', 'gifs', f'video_grid{gridsize}_time{total_time}_twolayers.gif'), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            for i in range(5):
                writer.append_data(image)
                
    pathfinder = FindPathGreedySingleLayerGifs(dronegrid_properties=dronegrid_properties)
    path, maxpath_index, grids = pathfinder.find_path(total_time=total_time)
    
    gifpath = []
        
    for index, path_coords in enumerate(path.drone.path):
        gifpath.append(path_coords)
        
        fig, ax = plotgrid(grid=grids[index])
        dronepathplots(ax=ax, path=gifpath, starting_point=path.drone.starting_point)

        plt.title(f'Max Sum: {path.drone.total_path_value[index+1]}')
        plt.savefig(os.path.join(BASE_DIR, 'data', 'gifs', 'figures', f'grid_{gridsize}_{index}.png'))
        plt.clf()
    
    dirpath = join(BASE_DIR, 'data', 'gifs', 'figures')
    filenames = [join(dirpath, f'grid_{gridsize}_{f}.png') for f in range(index) if isfile(join(dirpath,  f'grid_{gridsize}_{f}.png'))]
    
    with imageio.get_writer(join(BASE_DIR, 'data', 'gifs', f'video_grid{gridsize}_time{total_time}_singlelayer.gif'), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            for i in range(5):
                writer.append_data(image)