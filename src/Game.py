from UnsafeStack import UnsafeStack
from Level import Level
from Board import Board
from Case import Case
from Action import Action
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
        self.ui.game = self
        self.ui.run()

    def is_finished(self):
        return self.solved_board == self.user_board

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

    def new_hint(self, hint_type: int):
        x, y = -1, -1
        hint_tp = -1
        while (x == -1) and ((x, y) in self.hint_keys) and (hint_tp != hint_type):
            x, y = random.randint(0, self.level.size[0] - 1), random.randint(0, self.level.size[1] - 1)
            hint_tp = self._get_hint_type(x, y)
        self.hint_keys.add((x, y))
        self.hints.append(Case(x, y, hint_type))

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
        self.user_board = Board(self.level.size)
        self.user_actions_stack = UnsafeStack()
        
