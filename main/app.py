__author__ = 'prateek'

from flask import Flask
from input import input_file
from game import Game
matrix,M,N= input_file()

game= Game(matrix,M,N)
game.print_matrix()
game.formulate()
