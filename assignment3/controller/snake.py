class SnakeController:
    def __init__(self, snake, ui):
        self.snake = snake
        self.ui = ui
    
    def animateSnake(self, direction):
        pass

    def eatApple(self):
        self.snake.growSnake()

    def gameOver(self):
        pass

    def placeSnake(self):
        for snakepiece in self.snake.snake:
            self.ui.place(snakepiece.x, snakepiece.y, snakepiece.color)