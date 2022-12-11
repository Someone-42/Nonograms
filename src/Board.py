import numpy as np

class Board:
    __slots__ = (
        "grid"         # numpy 2D array<int> of size x by y, where values represent colors
        )
    def __init__(self, size, constraints):
        self.size = size
        self.constraints = constraints
        self.grid = np.zeros((size[0], size[1]))