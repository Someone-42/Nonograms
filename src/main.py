# Author: Lemarchand Tristan, Tison Alexandre, Bensouiah Rayan
# Date: 10/12/2022

import Solver
from Board import Board

game = Game(UI())
level = Level.from_file("src/Levels/Apple.lvl")
game.load_level(level)
game.run()
