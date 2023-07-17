# --- Built-ins ---
import copy
import os
from pathlib import Path
import json

# --- Internal ---
from src.base import DroneInfo, GridInfo
from src.algorithms.utils.pathproperties import DroneGridInfo
from src.algorithms.findpath_singledrone_twolayers import FindPathGreedyTwoLayers
from src.algorithms.utils.tools import divide_grid_circular, create_circular_grids

# --- External ---
import numpy as np

MIN_VALUE = -100001
BASE_DIR = Path(__file__).parents[1]

class FindPathSwarm(FindPathGreedyTwoLayers):
    def __init__(self, dronegrid_properties: list[DroneGridInfo]):
        # === Initialise drones on grid and set starting point grid value to zero ===
        self._initialise(dronegrid_properties=dronegrid_properties)
        self.nr_drones = len(dronegrid_properties)
        self._initialise_drones()
    
    def findpath(self, total_time)->DroneInfo:
        self._find_closest_circle()
        self._swarm_policy(total_time=total_time)        
    
    def _find_closest_circle(self)->dict:
        '''
            Move drone to closest circle
        '''
        # TODO: check what drones are already in a circular region
        
        # === Find drone circular grid combinations ===
        distances_drones_circles = []

        for drone in self.dronegrid_properties:
            radii = divide_grid_circular(nr_drones=self.nr_drones, grid=drone.grid)
            circular_grids = create_circular_grids(radii=radii, grid=drone.grid)
            
            distances_drones_circles.append(drone.distance_to_circle(radii=radii))

        distances_drones_circles_tmp = copy.deepcopy(distances_drones_circles)

        circle_drone_index = {}
        
        for circle_index in range(len(radii)-1):
            distances = []
            for distance in distances_drones_circles_tmp:
                distances.append(distance[circle_index])
                
            for indices in range(len(distances)):
                smallest_indices = np.argpartition(distances, indices)
                if smallest_indices[indices] not in circle_drone_index.values():
                    circle_drone_index[circle_index] = smallest_indices[indices]
                    break
            
            # distances_drones_circles_tmp.remove(distances_drones_circles_tmp[closest_drone])
        
        self.circle_drone_index = circle_drone_index
        
        # === Assign circular grids to respective drone ===
        for drone_index, drone in enumerate(self.dronegrid_properties):
            # TODO: circle_drone_index was swapped around
            drone.circular_grid(grid=circular_grids[circle_drone_index[drone_index]])
            
    def _initialise_drones(self)->None:
        '''
            Initialise all drones and add the initial value to their total_path_value
        '''
        # === Initially move drones into 8 directions ===
        for index, idronegrid in enumerate(self.dronegrid_properties):
            # === Add value of starting point ===
            current_drone_coords = idronegrid.drone.path[-1]

            idronegrid.drone.add_to_sum(square_value=
                                            idronegrid.grid.gridvalues[current_drone_coords[1]][current_drone_coords[0]])

    
    def _swarm_policy(self, total_time)->None:
        '''
            Move drone to either its assigned circular section or continue the algorithm
        '''
        radii = divide_grid_circular(nr_drones=self.nr_drones, grid=self.dronegrid_properties[0].grid)

        for timestep in range(total_time):
            for drone_index, drone in enumerate(self.dronegrid_properties):
                # The grids need to be synced each cycle
                # TODO: it should actually be during each run but it's horrible inefficient and for now i don't run into drones wanting to
                    # occupy the same square
                self._sync_grids()
                radius_index = self.circle_drone_index[drone_index]

                drone_in_section, direction = drone.drone_direction(radii=radii, radius_index=radius_index)
                
                if drone_in_section:
                    # perform standard two layer drone algo
                    pathvalues = drone.get_surrounding_values_circular()
                    self.dronegrid_properties[drone_index] = self._update_dronegridinfo(pathvalues=pathvalues, drone=dronegrid, timestep=timestep)
                
                else:
                    # drone must be moved to its assigned circular section
                    pathvalues = drone.get_surrounding_values_circular()
                    if direction==[1,0]:
                        # move drone upward
                        pathvalues[3:] = [MIN_VALUE]*len(pathvalues[3:])
                    elif direction==[0,1]:
                        # move drone rightward
                        pathvalues[:2] = [MIN_VALUE]*len(pathvalues[:2])
                        pathvalues[5:] = [MIN_VALUE]*len(pathvalues[5:])
                    elif direction==[-1,0]:
                        # move drone downward
                        pathvalues[:4] = [MIN_VALUE]*len(pathvalues[:4])
                        pathvalues[7:] = [MIN_VALUE]*len(pathvalues[7:])
                    elif direction==[0,-1]:
                        # move drone leftward
                        pathvalues[1:6] = [MIN_VALUE]*len(pathvalues[1:6])
                    else:
                        assert ValueError
                        print('ERROR: Direction not given!')
                    self.dronegrid_properties[drone_index] = self._update_dronegridinfo(pathvalues=pathvalues, drone=drone, timestep=timestep)
    
    def _sync_grids(self):
        '''
            Make sure all different grid have the same multiplier value
            TODO: O(N*N*X) This function is spectacularly inefficient but idh time to improve it rn
                    To improve this part introduce a shared grid_multiplier matrix. This requires rewriting all dataclasses though.
        '''
        grid_size = self.dronegrid_properties[0].grid.size
        for index_row in range(grid_size[0]):
            for index_col in range(grid_size[1]):
                tmp = 1.1
                for idronegrid in self.dronegrid_properties:
                    tmp = min(idronegrid.grid.grid_multiplier[index_row, index_col], tmp)
                
                # all matrices get the minimum multiplier value
                for dronegrid_index in range(len(self.dronegrid_properties)):
                    self.dronegrid_properties[dronegrid_index].grid.grid_multiplier[index_row, index_col] = tmp

class FindPathSwarmGif(FindPathSwarm):
    def _swarm_policy(self, total_time)->None:
        '''
            Move drone to either its assigned circular section or continue the algorithm.
            Slgihtly modified version to deal with creating a gifs
        '''
        dronegriddict = {}
        dronegriddict['total_time'] = total_time
        dronegriddict['nr_drones'] = self.nr_drones
        radii = divide_grid_circular(nr_drones=self.nr_drones, grid=self.dronegrid_properties[0].grid)

        with open(os.path.join(BASE_DIR, 'data', 'gifs', 'dronegrid_data',  'gridinfo.json'), 'w') as file:
            for timestep in range(total_time):
                for drone_index, dronegrid in enumerate(self.dronegrid_properties):
                    self._sync_grids()
                    radius_index = self.circle_drone_index[drone_index]

                    drone_in_section, direction = dronegrid.drone_direction(radii=radii, radius_index=radius_index)
                    
                    if drone_in_section:
                        # perform standard two layer drone algo
                        pathvalues = dronegrid.get_surrounding_values_circular()
                        self.dronegrid_properties[drone_index] = self._update_dronegridinfo(pathvalues=pathvalues, drone=dronegrid, timestep=timestep)
                    
                    else:
                        # drone mus tbe moved to its assigned circular section
                        pathvalues = dronegrid.get_surrounding_values_circular()
                        if direction==[1,0]:
                            # move drone upward
                            pathvalues[3:] = [MIN_VALUE]*len(pathvalues[3:])
                        elif direction==[0,1]:
                            # move drone rightward
                            pathvalues[:2] = [MIN_VALUE]*len(pathvalues[:2])
                            pathvalues[5:] = [MIN_VALUE]*len(pathvalues[5:])
                        elif direction==[-1,0]:
                            # move drone downward
                            pathvalues[:4] = [MIN_VALUE]*len(pathvalues[:4])
                            pathvalues[7:] = [MIN_VALUE]*len(pathvalues[7:])
                        elif direction==[0,-1]:
                            # move drone leftward
                            pathvalues[1:6] = [MIN_VALUE]*len(pathvalues[1:6])
                        else:
                            assert ValueError
                            print('ERROR: Direction not given!')
                        self.dronegrid_properties[drone_index] = self._update_dronegridinfo(pathvalues=pathvalues, drone=dronegrid, timestep=timestep)
                        
                # === Save grid info for each drone at each timestep ===
                dronegriddict['grid_t'+str(timestep)] = dronegrid.grid.gridvalues.flatten().tolist()
            
            for drone_index, dronegrid in enumerate(self.dronegrid_properties):
                dronegriddict['drone_path'+dronegrid.drone.name] = dronegrid.drone.path
                dronegriddict['drone_path_values'+dronegrid.drone.name] = dronegrid.drone.total_path_value
                
            json.dump(dronegriddict, file)