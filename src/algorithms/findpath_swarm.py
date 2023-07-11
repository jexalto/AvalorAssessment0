# --- Built-ins ---
import sys, os

# --- Internal ---
from src.base import DroneInfo, GridInfo

# --- External ---
import numpy as np


class FindPathSingleDrone:
    
    def __init__(self, drone: DroneInfo, grid: GridInfo, total_time: int):
        self.drone = drone
        self.grid = grid
        self.total_time = total_time
        pass
    
    def findpath(self):
        pass
    
    