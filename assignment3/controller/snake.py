class SnakeController:
    def __init__(self, snake, ui):
        self.snake = snake
        self.ui = ui
    
    def animateSnake(self):
        self.snake.moveSnakeOneOver()

    def changeDirection(self, direction):
        self.snake.changeFirstIndexDirection(direction)

    def updateDirections(self):
        self.snake.getNewDirections()

    def eatApple(self):
        self.snake.growSnake()

    def checkSnakePosition(self, apple):
        firstIndex = self.snake.snake[0]
        if [firstIndex.x, firstIndex.y] == [apple.x, apple.y]:
            return True
        for i in range(1, len(self.snake.snake)-1):
            if [firstIndex.x, firstIndex.y] == [self.snake.snake[i].x, self.snake.snake[i].y]:
                return False 

    def gameOver(self):
        self.ui.print_('Game Over ')
        self.ui.stay_open()

    def placeSnake(self):
        for snakepiece in self.snake.snake:
            try:
                self.ui.place(snakepiece.x, snakepiece.y, snakepiece.color)
            except:
                self.gameOver()
                #TODO: check how to set up try/catch statements
