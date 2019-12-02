import snakepiece as s
import sys
sys.path.append('..')
import util

class Snake:
    def __init__(self):
        self.snake = [
            s.SnakePiece([util.width/2, util.height/2], 'r'),
            s.SnakePiece([util.width/2-1, util.height/2-1], 'r'),
            s.SnakePiece([util.width/2-2, util.height/2-2], 'r'),
        ]

    def growSnake(self):
        lastIndex = self.snake[-1]
        self.snake.append(s.SnakePiece)


