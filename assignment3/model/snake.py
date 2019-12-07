from snakepiece import SnakePiece

class Snake:
    def __init__(self, width, height):
        self.snake = [
            # SnakePiece(width/2, height/2, 'r'),
            # SnakePiece(width/2-1, height/2, 'r'),
            # SnakePiece(width/2-2, height/2, 'r'),
            SnakePiece(19, 15, 'r'),
            SnakePiece(18, 15, 'r'),
            SnakePiece(17, 15, 'r'),
            SnakePiece(16, 15, 'r'),
            SnakePiece(15, 15, 'r'),
            SnakePiece(14, 15, 'r'),
            SnakePiece(13, 15, 'r'),
            SnakePiece(12, 15, 'r'),
            SnakePiece(11, 15, 'r'),
            SnakePiece(10, 15, 'r'),
        ]

    def moveSnakeOneOver(self):
        for snakePiece in self.snake:
            if snakePiece.direction == 'u':
                snakePiece.y -= 1
            elif snakePiece.direction == 'd':
                snakePiece.y += 1
            elif snakePiece.direction == 'l':
                snakePiece.x -= 1
            elif snakePiece.direction == 'r':
                snakePiece.x += 1

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

    def changeFirstIndexDirection(self, direction):
        if self.snake[0].direction == 'u' and direction != 'd':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'd' and direction != 'u':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'l' and direction != 'r':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'r' and direction != 'l':
            self.snake[0].direction = direction

    def getNewDirections(self):
        for i in range(len(self.snake)-1, 0, -1):
            self.snake[i].direction = self.snake[i-1].direction
            