class SnakeController:
    def __init__(self, snake, ui):
        self.snake = snake
        self.ui = ui
    
    def animateSnake(self):
        pass

    def changeDirection(self, direction):
        if self.snake[0].direction == 'u' and direction != 'd':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'd' and direction != 'u':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'l' and direction != 'r':
            self.snake[0].direction = direction
        elif self.snake[0].direction == 'r' and direction != 'l':
            self.snake[0].direction = direction


    def eatApple(self):
        self.snake.growSnake()

    def gameOver(self):
        pass

    def placeSnake(self):
        for snakepiece in self.snake.snake:
            self.ui.place(snakepiece.x, snakepiece.y, snakepiece.color)