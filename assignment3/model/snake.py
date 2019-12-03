from snakepiece import SnakePiece

class Snake:
    def __init__(self, height, width):
        self.snake = [
            SnakePiece(width/2, height/2, 'r'),
            SnakePiece(width/2-1, height/2, 'r'),
            SnakePiece(width/2-2, height/2, 'r'),
        ]

    def growSnake(self):
        # lastIndex = self.snake[-1]
        pass
