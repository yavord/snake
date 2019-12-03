from snakepiece import SnakePiece

class Snake:
    def __init__(self, height, width):
        self.snake = [
            SnakePiece(width/2, height/2, 'r'),
            SnakePiece(width/2-1, height/2, 'r'),
            SnakePiece(width/2-2, height/2, 'r'),
        ]

    def growSnake(self):
        lastIndex = self.snake[-1]
        if lastIndex.direction == 'l':
            self.snake.append(SnakePiece(lastIndex.x+1, lastIndex.y, lastIndex.direction))
        elif lastIndex.direction == 'r':
            self.snake.append(SnakePiece(lastIndex.x-1, lastIndex.y, lastIndex.direction))
        elif lastIndex.direction == 'u':
            self.snake.append(SnakePiece(lastIndex.x, lastIndex.y+1, lastIndex.direction))
        elif lastIndex.direction == 'd':
            self.snake.append(SnakePiece(lastIndex.x, lastIndex.y-1, lastIndex.direction))

    # def changeFirstIndexDirection(self):
    #     firstIndex = self.snake[0]

