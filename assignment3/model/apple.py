import sys
sys.path.append('..')
import util
from ipy_lib import SnakeUserInterface as s

class Apple:
    def __init__(self):
        self.coords = []
        self.color = 4

    def placeApple(self):
        self.coords = [s.random(util.width),s.random(util.height)]

