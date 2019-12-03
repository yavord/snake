class SnakeController:
    def __init__(self, snake, ui):
        self.snake = snake
        self.ui = ui
    
    def animateSnake(self):
        for snakePiece in self.snake.snake:
            if snakePiece.direction == 'u':
                snakePiece.y -= 1
            elif snakePiece.direction == 'd':
                snakePiece.y += 1
            elif snakePiece.direction == 'l':
                snakePiece.x -= 1
            elif snakePiece.direction == 'r':
                snakePiece.x += 1

    def changeDirection(self, direction):
        if self.snake.snake[0].direction == 'u' and direction != 'd':
            self.snake.snake[0].direction = direction
        elif self.snake.snake[0].direction == 'd' and direction != 'u':
            self.snake.snake[0].direction = direction
        elif self.snake.snake[0].direction == 'l' and direction != 'r':
            self.snake.snake[0].direction = direction
        elif self.snake.snake[0].direction == 'r' and direction != 'l':
            self.snake.snake[0].direction = direction

    def updateDirections(self):
        for i in range(len(self.snake.snake)-1, 0, -1):
            self.snake.snake[i].direction = self.snake.snake[i-1].direction

    def eatApple(self):
        self.snake.growSnake()

    def checkSnakePosition(self, apple):
        firstIndex = self.snake.snake[0]
        if [firstIndex.x, firstIndex.y] == [apple.x, apple.y]:
            return True
        for i in range(1, len(self.snake.snake)-1):
            if [firstIndex.x, firstIndex.y] == [self.snake.snake[i].x, self.snake.snake[i].y]:
                return self.gameOver 

    def gameOver(self):
        self.ui.print_('Game Over')
        self.ui.stay_open()

    def placeSnake(self):
        for snakepiece in self.snake.snake:
            try:
                self.ui.place(snakepiece.x, snakepiece.y, snakepiece.color)
            except:
                return self.gameOver
