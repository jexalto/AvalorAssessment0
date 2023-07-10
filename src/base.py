# --- Built-ins ---
from dataclasses import dataclass
from functools import cached_property

# --- Internal ---

# --- External ---
import numpy as np

@dataclass
class DroneInfo:
    name: str
    starting_point: list[int]
    
    def __post_init__(self):
        self.total_path_value = 0.
        self.path = [self.starting_point]
    
    def move_drone(self, coords_new: list[int]):
        '''
            Adds new point to self.path
        '''
        self.path.append(coords_new) # extend or append?
        
    def add_to_sum(self, square_value: float):
        '''
            Adds newly collected value to total sum
        '''
        self.total_path_value += square_value

@dataclass
class GridInfo:
    name: str
    gridshape: np.array
    reset_time: int # the mount of time it takes to reset a square's value back to its original value from zero
    
    def __post_init__(self):
        self.size = self.gridshape.shape
        # After a square is visited, the grid_multiplier is set to zero
        self.grid_multiplier = np.ones(self.size)
        
    def drone_moved_to_square(self, coords: list[int]):
        '''
            Function that is called when drone moves. Consequently, time progresses
        '''
        self._update_grid_multiplier(coords=coords)
        self._update_grid_values()
        
    def _update_grid_multiplier(self, coords: list[int]):
        '''
            Grid values get updated for the square that is visited
        '''        
        # === Update the multiplier values that were previously set to zero ===
        # TODO: this operation is mega inefficient as is, will be improved later (pvp)
        for index_row, row in enumerate(self.grid_multiplier):
            for index_col, col in enumerate(row):
                if self.grid_multiplier[index_row][index_col] != 1:
                    self.grid_multiplier[index_row][index_col] += 1/self.reset_time
                    
        x, y = coords
        # === Set the newly visited square multiplier score to zero ===
        self.grid_multiplier[x][y] = 0
    
    def _update_grid_values(self):
        self.gridshape = np.multiply(self.gridshape, self.grid_multiplier)