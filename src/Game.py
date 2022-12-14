from UnsafeStack import UnsafeStack
from Level import Level
from Board import Board
from Case import Case
from Action import Action
import Solver
import random
import numpy as np

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
        self.hint_keys = dict()
        self.hints = []
        self.user_actions_stack = UnsafeStack()
        self.ui.load()
        self.ui.update_level_name()

    def run(self):
        self.ui.run()

    def is_finished(self):
        return np.array_equal(self.user_board.grid, self.solved_board.grid)

    def _get_hint_type(self, x, y):
        user_xy, solved_xy = self.user_board.grid[y, x], self.solved_board.grid[y, x]
        if user_xy == 0:
            if solved_xy == 0:
                return -1       # Hint type -1 : Error/Discard
            if solved_xy > 0:
                return 1        # Hint type 1 : Solution case (auto colored)
        else:
            if solved_xy != user_xy:
                return 2        # Hint type 2 : Wrong color placement by the user
            else:
                return 3        # Hint type 3 : Right placement by the user

    def _get_hint_placements(self, hint_type: int) -> list:
        l = []
        for x in range(self.user_board.size[0]):
            for y in range(self.user_board.size[1]):
                if self._get_hint_type(x, y) == hint_type and ((x, y) not in self.hint_keys):
                    l.append((x, y))
        return l

    def new_hint(self, hint_type: int):
        hint_placements = self._get_hint_placements(hint_type)
        if not hint_placements:
            return -1, -1, -1
        x, y = random.choice(self._get_hint_placements(hint_type))
        self.hint_keys[(x, y)] = hint_type
        self.hints.append(Case(x, y, hint_type))
        return x, y, hint_type

    def can_undo(self):
        return not self.user_actions_stack.is_empty()

    def can_redo(self):
        return self.user_actions_stack.can_unpop()

    def undo(self):
        action = self.user_actions_stack.pop()
        self.user_board.grid[action.y, action.x] = action.previous_color

    def redo(self):
        action = self.user_actions_stack.unpop()
        self.user_board.grid[action.y, action.x] = action.new_color

    def color(self, x, y, color):
        action = Action(x, y, color, self.user_board.grid[y, x])
        if action.new_color == action.previous_color:
            return
        self.user_board.grid[y, x] = color
        self.user_actions_stack.push(action)

    def reset(self):
        self.user_board.clear()
        self.user_actions_stack.clear()
        self.hints.clear()
        self.hint_keys.clear()
        
