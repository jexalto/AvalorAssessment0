# --- Built-ins ---
import copy

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.base import GridInfo

# --- External ---
import numpy as np
from matplotlib.patches import Rectangle


class FindPathGreedy:
    def __init__(self, dronegrid_properties: list[DroneGridInfo]):
        # === Initialise drones on grid and set starting point grid value to zero ===
        self._initialise(dronegrid_properties=dronegrid_properties)
        
    def find_path(self, total_time)->DroneGridInfo:
        # === Find 8 distinct paths ===
        self._process_paths(total_time=total_time)

        # === Filter out path with maximum return ===
        maxpath = 0
        maxpath_index = 0

        for index, idronegrid in enumerate(self.dronegrid_properties):
            if idronegrid.drone.total_path_value>maxpath:
                maxpath_index = index
                maxpath = idronegrid.drone.total_path_value
        
        maxdronepath = copy.deepcopy(self.dronegrid_properties[maxpath_index])
        
        # === Reinitialise class and reset drone properties ===        
        self._initialise(dronegrid_properties=self.dronegrid_properties)
        self._reset_drone(dronegrid_properties=self.dronegrid_properties)
        
        return maxdronepath
    
    def _initialise(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.grid.reset()
        self.dronegrid_properties = dronegrid_properties
        
    def _reset_drone(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.drone.reset()
    
    def _process_paths(self, total_time: int)->list[DroneGridInfo]:
        '''
            Coordinates look like this:
                    x - >
            
                0,0 - 0,1 - .,. - 0,n
            y   1,0 - .,. - .,. - 1,n
            |   .,. - .,. - .,. - .,.
            v   .,. - .,. - .,. - .,.
                n,0 - .,. - .,. - n,n
        '''        
        x_index = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_index = [-1, -1, -1, 0, 1, 1, 1, 0]
        
        # === Initially move drones into 8 directions ===
        for index, idronegrid in enumerate(self.dronegrid_properties):
            # === Update drone path ===
            current_drone_coords = idronegrid.drone.path[-1]
            new_drone_coords = [current_drone_coords[0]+x_index[index], 
                                current_drone_coords[1]+y_index[index]]
                
            idronegrid.drone.move_drone(coords_new=new_drone_coords)
            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[current_drone_coords[0]][current_drone_coords[1]])
            
            # === Update grid ===
            idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=1)

        # === Perform path finding operation for all 8 drone instances ===
        for timestep in range(2, total_time+1):
            for idronegrid in self.dronegrid_properties:
                # === Find max numerical value around square ===
                pathvalues = idronegrid.get_surrounding_values()
                
                assert len(pathvalues) == 8
                
                max_index = np.argmax(pathvalues)
                
                # === Find new drone coords ===            
                current_drone_coords = idronegrid.drone.path[-1]
                new_drone_coords = [current_drone_coords[0]+x_index[max_index], 
                                    current_drone_coords[1]+y_index[max_index]]
                
                # === Update drone path ===
                idronegrid.drone.move_drone(coords_new=new_drone_coords)
                idronegrid.drone.add_to_sum(square_value=
                                                idronegrid.grid.gridvalues[current_drone_coords[0]][current_drone_coords[1]])
                
                # === Update grid ===
                idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=timestep)
                
        return self.dronegrid_properties
    
class FindPathGreedyGifs:
    def __init__(self, dronegrid_properties: list[DroneGridInfo]):
        # === Initialise drones on grid and set starting point grid value to zero ===
        self._initialise(dronegrid_properties=dronegrid_properties)
        
    def find_path(self, total_time)->DroneGridInfo:
        # === Find 8 distinct paths ===
        grids = self._process_paths(total_time=total_time)

        # === Filter out path with maximum return ===
        maxpath = 0
        maxpath_index = 0

        for index, idronegrid in enumerate(self.dronegrid_properties):
            if idronegrid.drone.total_path_value>maxpath:
                maxpath_index = index
                maxpath = idronegrid.drone.total_path_value
        
        maxdronepath = copy.deepcopy(self.dronegrid_properties[maxpath_index])
        
        # === Reinitialise class and reset drone properties ===        
        self._initialise(dronegrid_properties=self.dronegrid_properties)
        self._reset_drone(dronegrid_properties=self.dronegrid_properties)
        
        return maxdronepath, maxpath_index, grids
    
    def _initialise(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.grid.reset()
        self.dronegrid_properties = dronegrid_properties
        
    def _reset_drone(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.drone.reset()
    
    def _process_paths(self, total_time: int)->list[DroneGridInfo]:
        '''
            Coordinates look like this:
                    x - >
            
                0,0 - 0,1 - .,. - 0,n
            y   1,0 - .,. - .,. - 1,n
            |   .,. - .,. - .,. - .,.
            v   .,. - .,. - .,. - .,.
                n,0 - .,. - .,. - n,n
        '''        
        x_index = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_index = [-1, -1, -1, 0, 1, 1, 1, 0]
        
        grids = []
        
        # === Initially move drones into 8 directions ===
        for index, idronegrid in enumerate(self.dronegrid_properties):
            # === Update drone path ===
            current_drone_coords = idronegrid.drone.path[-1]
            new_drone_coords = [current_drone_coords[0]+x_index[index], 
                                current_drone_coords[1]+y_index[index]]
                
            idronegrid.drone.move_drone(coords_new=new_drone_coords)
            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[current_drone_coords[0]][current_drone_coords[1]])
            
            # === Update grid ===
            idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=1)

        # === Perform path finding operation for all 8 drone instances ===
        for timestep in range(2, total_time+1):
            for idronegrid in self.dronegrid_properties:
                # === Find max numerical value around square ===
                pathvalues = idronegrid.get_surrounding_values()
                
                assert len(pathvalues) == 8
                
                max_index = np.argmax(pathvalues)
                
                # === Find new drone coords ===            
                current_drone_coords = idronegrid.drone.path[-1]
                new_drone_coords = [current_drone_coords[0]+x_index[max_index], 
                                    current_drone_coords[1]+y_index[max_index]]
                
                # === Update drone path ===
                idronegrid.drone.move_drone(coords_new=new_drone_coords)
                idronegrid.drone.add_to_sum(square_value=
                                                idronegrid.grid.gridvalues[current_drone_coords[0]][current_drone_coords[1]])
                
                # === Update grid ===
                idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=timestep)
                
                grids.append(idronegrid.grid)
                
        return grids
    
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
