# --- Built-ins ---
import unittest

# --- Internal ---
from base import DroneInfo, GridInfo

# --- External ---
import numpy as np

class TestGrid(unittest.TestCase):
    def test_update_grid(self):
        grid = GridInfo(name='TestGrid',
                        gridshape=self.gridmatrix)