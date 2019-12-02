from assignment3.model import *
from assignment3.ipy_lib import SnakeUserInterface

class SnakeController:
    def __init__(self, snake, ui):
        self.snake = snake
        self.ui = ui
    
    def animateSnake(self):
        pass

    def eatApple(self):
        pass

    def gameOver(self):
        pass

    def placeSnake(self):
        for snakepiece in self.snake:
            self.ui.place(snakepiece[0], snakepiece[1], snakepiece.color)