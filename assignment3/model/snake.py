import snakepiece as s

class Snake:
    def __init__(self, height, width):
        self.snake = [
            s.SnakePiece([width/2, height/2], 'r'),
            s.SnakePiece([width/2-1, height/2-1], 'r'),
            s.SnakePiece([width/2-2, height/2-2], 'r'),
        ]

    def growSnake(self):
        # lastIndex = self.snake[-1]
        pass
