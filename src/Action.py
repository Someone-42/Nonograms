class Action:
    __slots__ = (
        "x",
        "y",
        "new_color",
        "previous_color"
    )
    def __init__(self, x, y, new_color, previous_color = 0):
        self.x = x
        self.y = y
        self.new_color = new_color
        self.previous_color = previous_color