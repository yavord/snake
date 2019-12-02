import snakepiece as s
import assignment3.util as util

class Snake:
    def __init__(self):
        self.snake = [
            s.SnakePiece([util.width/2, util.height/2], 'r'),
            s.SnakePiece([util.width/2-1, util.height/2-1], 'r'),
            s.SnakePiece([util.width/2-2, util.height/2-2], 'r'),
        ]

    def growSnake(self):
        lastIndex = self.snake[-1]
        


