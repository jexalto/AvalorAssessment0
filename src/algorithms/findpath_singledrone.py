# --- Built-ins ---
from pathlib import Path

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.pathproperties import DroneGridInfo

# --- External ---
import numpy as np

class FindPathGreedy:
    def __init__(self, dronegrid_properties: list[DroneGridInfo]):
        # === Initialise drones on grid and set starting point grid value to zero ===
        for idronegrid in dronegrid_properties:
            starting_point = idronegrid.drone.starting_point
            idronegrid.grid.drone_moved_to_square(coords=starting_point, time=0)
        self.dronegrid_properties = dronegrid_properties
    
    def findpath(self, total_time: int)->list[list[int]]:
        '''
            Coordinates look like this:
                    x - >
            
                0,0 - 0,1 - .,. - 0,n
            y   1,0 - .,. - .,. - 1,n
            |   .,. - .,. - .,. - .,.
            v   .,. - .,. - .,. - .,.
                n,0 - .,. - .,. - n,n
        '''
        nr_paths = len(self.dronegrid_properties) # we have 8 possible paths to follow
        
        x_index = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_index = [-1, -1, -1, 0, 1, 1, 1, 0]
        
        # === Move drone into 8 directions ===
        
        
        for timestep in range(2, total_time+1):
            for idronegrid in self.dronegrid_properties:
                # === Find max numerical value around square ===
                pathvalues = idronegrid.get_surrounding_values()
                max_index = np.argmax(pathvalues)
                
                # === Find new drone coords ===            
                current_drone_coords = idronegrid.drone.path[-1]
                new_drone_coords = [current_drone_coords[0]+x_index[max_index], 
                                    current_drone_coords[1]+y_index[max_index]]
                
                # === Update drone path ===
                idronegrid.drone.move_drone(coords_new=new_drone_coords)
                idronegrid.drone.add_to_sum(square_value=
                                                idronegrid.grid.gridshape[current_drone_coords[0]][current_drone_coords[1]])
                
                # === Update grid ===
                idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=timestep)
                
        return idronegrid
    
class FindPathGravity(DroneGridInfo):
    def __init__(self):
        pass
    
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
        surrounding_values = self.get_surrounding_values()
        return surrounding_values