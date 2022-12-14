# Author: Lemarchand Tristan, Tison Alexandre, Bensouiah Rayan
# Date: 10/12/2022

from Game import Game
from Level import Level
from UI import UI

game = Game(UI())
level = Level.from_file("src/Levels/Apple.lvl")
game.load_level(level)
game.run()
