# --- Built-ins ---
import os
from os.path import isfile, join
from pathlib import Path
import copy
import json

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.utils.gifs import dronepathplots, plotgrid, make_gif
from src.utils.plots import draw_regions
from src.tests.inputs import testinputs

# --- External ---
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE_DIR = Path(__file__).parents[1]
PICTURE_DIR = os.path.join(BASE_DIR, 'data', 'gifs', 'swarm', 'figures')
GIF_DIR = os.path.join(BASE_DIR, 'data', 'gifs', 'swarm')
    
def load_grids(data: dict, gridsize: int)->list[float]:
    '''
        Extract grids from (messy) dict
    '''
    grids = []
    for key in data.keys():
        if key[:4]=='grid':
            grids.append(np.array(data[key]).reshape(gridsize, gridsize))
            
    return grids

def load_drones(data: dict)->list[list[int]]:
    '''
        Extract drones from (messy) dict
    '''
    # TODO: please change the keys in the json this is horrendous
    drones_path, drone_value = [], []
    start_value = 0
    
    for key in data.keys():
        if key[:15]=='drone_pathDrone':
            drones_path.append(data[key])
            
    for key in data.keys():
        if key[:17]=='drone_path_values':
            drone_value.append(data[key])
            start_value+=data[key][0]
            
    return drones_path, drone_value, start_value
    
def load_circular_regions(radii: list[int], gridsize: list[int])->list[list[int]]:
    original_grid_size = gridsize
    x, y = [], []
    # assign values to the top side of the rectangle
    for index in range(len(radii)-1):
        x0, y0 = [radii[index], original_grid_size-radii[index], original_grid_size-radii[index], radii[index]], \
                    [radii[index], radii[index], original_grid_size-radii[index], original_grid_size-radii[index]]
        
        x.append(x0)
        y.append(y0)
        
    return [x, y]

if __name__=='__main__':
    # === Load in grid ===
    _, grid, drone, _ = testinputs()
    
    # === Read in json file with data ===
    with open(os.path.join(BASE_DIR, 'data', 'gifs', 'dronegrid_data', 'gridinfo.json'), 'r') as file:
        data=file.read()
    
    data = json.loads(data)
    total_time = data['total_time']
    nr_drones = data['nr_drones']

    gridsize = 20
    reset_time = 10 # pretty sure this is not used right now
    
    grids = load_grids(data=data, gridsize=gridsize)
    drones_path, drones_value, start_value = load_drones(data=data)
    circular_coords = load_circular_regions(radii=data['radii'], gridsize=gridsize)
    # assert len(grids)==total_time-1
    assert len(drones_path)==nr_drones
    
    total_value = start_value
    
    for timestep in range(total_time):
        total_value = 0
        
        grid_gif_input = GridInfo(name='TestGrid',
                        gridshape=np.multiply(grid.gridshape, grids[timestep]),
                        reset_time=reset_time)

        fig, ax = plotgrid(grid=grid_gif_input)
        draw_regions(ax=ax, coords=circular_coords, len_radii=len(data['radii']), gridsize=gridsize)
        
        for drone in range(nr_drones):
            dronepathplots(ax=ax, path=drones_path[drone][:timestep+1], starting_point=drones_path[drone][0])
            total_value += drones_value[drone][timestep+1]
        
        plt.title(f'Max Sum: {total_value}')
        plt.savefig(os.path.join(PICTURE_DIR, f'grid_{gridsize}_{timestep}.png'))
        plt.clf()
        plt.close()
        
    make_gif(picture_dir=PICTURE_DIR, framestop=10, output_dir=GIF_DIR, total_time=total_time, gridsize=gridsize)