class Level:
    __slots__ = (
        "name",
        "size",         # Tuple : (x, y)
        "constraints",  # Array of size (x + y), x first elements are the list constraints for columns
    )
    def __init__(self, size, constraints, name = "NoName") -> None:
        self.size = size
        self.constraints = constraints
        self.name = name

    @staticmethod
    def from_file(path):
        name = path.split('/')[-1][:-4]
        f = open(path, 'r')
        values = [[int(c) for c in l.strip().split(' ')] for l in f.readlines()]
        f.close()
        return Level(tuple(values[0]), values[1:], name)