# Author: Lemarchand Tristan, Tison Alexandre, Bensouiah Rayan
# Date: 10/12/2022

import Solver
from Board import Board
from Level import Level
from Utils import *

b = Level.from_file("src/TestBoard.txt")
b = Solver.solve(b)
display_console_board(b)