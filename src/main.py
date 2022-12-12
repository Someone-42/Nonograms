# Author: Lemarchand Tristan, Tison Alexandre, Bensouiah Rayan
# Date: 10/12/2022

from Game import Game
from UI import UI

game = Game(UI())
game.load_level()
game.run()