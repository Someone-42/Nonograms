from Level import Level
from Solver import solve
from Utils import display_console_board

level = Level.from_file("src/AMOGUS.lvl")
solved = solve(level)
display_console_board(solved)