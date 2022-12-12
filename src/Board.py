import numpy as np

class Board:
    __slots__ = (
        "size",        # Tuple : (x, y)
        "grid"         # numpy 2D array<int> of size x by y, where values represent colors
        )
    def __init__(self, size, _create_array = True):
        self.size = size
        if _create_array:
            self.grid = np.zeros((size[0], size[1]))
        else:
            self.grid = None

    def clear():
        self.grid *= 0