from UnsafeStack import UnsafeStack
from Level import Level
from Board import Board
from Case import Case
import Solver
import random

class Game:
    __slots__ = (
        "level",
        "user_board",
        "solved_board",
        "hint_keys",
        "hints",
        "user_actions_stack",
        "ui"
    )
    def __init__(self, ui):
        self.level = None
        self.user_board = None
        self.solved_board = None
        self.hint_keys = None
        self.hints = None
        self.user_actions_stack = None
        self.ui = ui
        self.ui.game = self

    def load_level(self, level: Level):
        self.level = level
        self.user_board = Board(level.size)
        self.solved_board = Solver.solve(level)
        self.hint_keys = set()
        self.hints = []
        self.user_actions_stack = UnsafeStack()

    def run(self):
        self.ui.run()

    def is_finished(self):
        return self.solved_board == self.user_board

    def new_hint(self, hint_type: int):
        x, y = -1, -1
        while (x != -1) and ((x, y) not in self.hint_keys):
            x, y = random.randint(0, self.level.size[0] - 1), random.randint(0, self.level.size[1] - 1)
        self.hint_keys.add((x, y))
        self.hints.append(Case(x, y, hint_type))