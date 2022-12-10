# Author: Lemarchand Tristan, Tison Alexandre, Bensouiah Rayan
# Date: 10/12/2022

import Solver
from Board import Board

b = Board.from_file("src/TestBoard.txt")
b = Solver.solve(b)
b.display_console()