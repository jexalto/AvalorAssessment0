# --- Built-ins ---
import os
from pathlib import Path

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.base import GridInfo

# --- External ---
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parents[1]

def dronepathplots(dronegrid: DroneGridInfo)->None:
    

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
    fig = plt.figure(figsize=(8, 8), dpi=120)
    ax = fig.add_subplot(111)
    
    # === Print values in squares ===
    for irow in range(nrows):
        for icol in range(ncols):
            text = ax.text(icol, irow, grid.gridshape[irow, icol],
                    ha="center", va="center", color="w")
            
    cax = ax.matshow(image)
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
    
    plotgrid(grid=grid)