import numpy as np

class Board:
    __slots__ = (
        "size",         # Tuple : (x, y)
        "constraints",  # Array of size (x + y), x first elements are the list constraints for columns
        "grid"         # 2D boolean array of size x by y, containing either True or False
        )
    def __init__(self, size, constraints):
        self.size = size
        self.constraints = constraints
        self.grid = np.zeros((size[0], size[1])) > 0

    @staticmethod
    def from_file(path):
        f = open(path, 'r')
        values = [[int(c) for c in l.strip().split(' ')] for l in f.readlines()]
        f.close()
        return Board(tuple(values[0]), values[1:])

    def display_console(self):
        for l in self.grid:
            for c in l:
                print('#' if c else ' ', end = " ")
            print()