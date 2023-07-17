# --- Built-ins ---
import copy

# --- Internal ---
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.base import GridInfo
from src.algorithms.utils.tools import surrounding_values_finder

# --- External ---
import numpy as np

MIN_VALUE = -100001

class FindPathGreedyTwoLayers:
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
            if idronegrid.drone.total_path_value[index]>maxpath:
                maxpath_index = index
                maxpath = idronegrid.drone.total_path_value[index]
        
        maxdronepath = copy.deepcopy(self.dronegrid_properties[maxpath_index])
        
        # === Reinitialise class and reset drone properties ===        
        self._initialise(dronegrid_properties=self.dronegrid_properties)
        self._reset_drone(dronegrid_properties=self.dronegrid_properties)
        
        return maxdronepath
    
    def _initialise(self, dronegrid_properties: list[DroneGridInfo])->None:
        starting_x, starting_y = dronegrid_properties[0].drone.starting_point
        for idronegrid in dronegrid_properties:
            idronegrid.grid.reset()
            # When initialising the dorne on the grid the multiplier should be set to zero for the starting position
            # TODO: integrate this in the drone-grid initialisation
            idronegrid.grid.grid_multiplier[starting_y][starting_x] = 0
            
        self.dronegrid_properties = dronegrid_properties
        
    def _reset_drone(self, dronegrid_properties: list[DroneGridInfo])->None:
        for idronegrid in dronegrid_properties:
            idronegrid.drone.reset()
         
    def _max_index_finder(self, surrounding_values: list[int], current_grid: GridInfo, current_coords: list[int])->int:
        '''
            In case there's multiple squares with the same maximum value we look one layer deeper and assess what values has the
            highest summation of squares around it. That way we can say the algorithm is walking towards a 'more' rewarding region.
        '''
        # TODO: maybe make this global lists or sth
        temp = MIN_VALUE*8-1
        
        x_index = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_index = [-1, -1, -1, 0, 1, 1, 1, 0]
        
        max_indices = np.argmax(surrounding_values)
        max_values_indices = np.where(surrounding_values==surrounding_values[max_indices])[0]
        
        # === Check whether multiple values exist with the maximum value ===
        if len(max_values_indices)>1:
            for max_index in max_values_indices:
                sum_surrounding = np.sum(surrounding_values_finder(x=current_coords[1]+x_index[max_index], y=current_coords[0]+y_index[max_index], 
                                                            grid=current_grid.gridvalues, gridshape=np.shape(current_grid.gridvalues)))
                
                if sum_surrounding>temp:
                    temp=sum_surrounding
                    new_max_index = max_index
            
            return new_max_index
        
        else:
            return max_indices
    
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
            # === Add value of starting point ===
            current_drone_coords = idronegrid.drone.path[-1]

            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[current_drone_coords[1]][current_drone_coords[0]])
            
            # === Update drone path ===
            new_drone_coords = [current_drone_coords[0]+x_index[index], 
                                current_drone_coords[1]+y_index[index]]

            idronegrid.drone.move_drone(coords_new=new_drone_coords)            
            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[new_drone_coords[1]][new_drone_coords[0]])
            
            # === Update grid ===
            idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=1)

        # === Perform path finding operation for all 8 drone instances ===
        for timestep in range(2, total_time+1):
            for drone_index, idronegrid in enumerate(self.dronegrid_properties):
                self.dronegrid_properties[drone_index] = self._move_drone(drone=idronegrid, timestep=timestep)
                
        return self.dronegrid_properties
    
    def _move_drone(self, drone: DroneGridInfo, timestep: int)->DroneGridInfo:
        '''
            Move drone according to greedy algorithm with one extra layer if multiple squares
            have the same maximum value
        '''        
        # === Find max numerical value around square ===
        pathvalues = drone.get_surrounding_values()
        assert len(pathvalues) == 8
        
        return self._update_dronegridinfo(pathvalues=pathvalues, drone=drone, timestep=timestep)
        
    def _update_dronegridinfo(self, pathvalues: np.array, drone:DroneGridInfo, timestep: int):
        '''
            Update DroneGridInfo instance. This function is separate from self._move_drone 
            due to the swarm algoritm implementation.
        '''
        x_index = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_index = [-1, -1, -1, 0, 1, 1, 1, 0]
        # === Find new drone coords ===
        current_drone_coords = drone.drone.path[-1]

        max_index = self._max_index_finder(surrounding_values=pathvalues, current_grid=drone.grid,
                                            current_coords=current_drone_coords)
                        
        new_drone_coords = [current_drone_coords[0]+x_index[max_index], 
                            current_drone_coords[1]+y_index[max_index]]
        
        # === Update drone path ===
        drone.drone.move_drone(coords_new=new_drone_coords)
        drone.drone.add_to_sum(square_value=
                                        drone.grid.gridvalues[new_drone_coords[1]][new_drone_coords[0]])
        
        # === Update grid ===
        drone.grid.drone_moved_to_square(coords=new_drone_coords, time=timestep)
        
        return drone    
        

class FindPathGreedyTwoLayersGifs(FindPathGreedyTwoLayers):        
    def find_path(self, total_time)->DroneGridInfo:
        # === Find 8 distinct paths ===
        grids = self._process_paths(total_time=total_time)

        # === Filter out path with maximum return ===
        maxpath = 0
        maxpath_index = 0

        for index, idronegrid in enumerate(self.dronegrid_properties):
            if idronegrid.drone.total_path_value[-1]>maxpath:
                maxpath_index = index
                maxpath = idronegrid.drone.total_path_value[index]
        
        maxdronepath = copy.deepcopy(self.dronegrid_properties[maxpath_index])
        
        # === Reinitialise class and reset drone properties ===        
        self._initialise(dronegrid_properties=self.dronegrid_properties)
        self._reset_drone(dronegrid_properties=self.dronegrid_properties)
        
        return maxdronepath, maxpath_index, grids[maxpath_index]
    
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
        
        grids = {}
        
        # === Initially move drones into 8 directions ===
        for index, idronegrid in enumerate(self.dronegrid_properties):
            # === Add value of starting point ===
            current_drone_coords = idronegrid.drone.path[-1]
            
            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[current_drone_coords[1]][current_drone_coords[0]])
            
            grids[index] = [copy.deepcopy(idronegrid.grid)]
            
            # === Update drone path ===
            current_drone_coords = idronegrid.drone.path[-1]
            new_drone_coords = [current_drone_coords[0]+x_index[index], 
                                current_drone_coords[1]+y_index[index]]

            idronegrid.drone.move_drone(coords_new=new_drone_coords)            
            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[new_drone_coords[1]][new_drone_coords[0]])
            
            # === Update grid ===
            idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=1)
            
            grids[index].append(copy.deepcopy(idronegrid.grid))

        # === Perform path finding operation for all 8 drone instances ===
        for timestep in range(2, total_time+1):
            for index, idronegrid in enumerate(self.dronegrid_properties):
                # === Find max numerical value around square ===
                pathvalues = idronegrid.get_surrounding_values()
                
                assert len(pathvalues) == 8
                
                # === Find new drone coords ===
                current_drone_coords = idronegrid.drone.path[-1]

                max_index = self._max_index_finder(surrounding_values=pathvalues, current_grid=idronegrid.grid,
                                                   current_coords=current_drone_coords)
                                
                new_drone_coords = [current_drone_coords[0]+x_index[max_index], 
                                    current_drone_coords[1]+y_index[max_index]]
                
                # === Update drone path ===
                idronegrid.drone.move_drone(coords_new=new_drone_coords)
                idronegrid.drone.add_to_sum(square_value=
                                                idronegrid.grid.gridvalues[new_drone_coords[1]][new_drone_coords[0]])
                
                # === Update grid ===
                idronegrid.grid.drone_moved_to_square(coords=new_drone_coords, time=timestep)
                
                grids[index].append(copy.deepcopy(idronegrid.grid))
                
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
