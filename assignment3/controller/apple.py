
class AppleController:
    def __init__(self, apple, ui):
        self.apple = apple
        self.ui = ui

    def placeApple(self):
        self.ui.place(self.apple.x, self.apple.y, self.apple.color)

    def getNewApple(self, width, height):
        self.apple.x = self.ui.random(width)
        self.apple.y = self.ui.random(height)

    def checkApplePosition(self, snake):
        snakePieces = snake.snake
        for snakePiece in snakePieces:
            if self.apple.x == snakePiece.x and self.apple.y == snakePiece.y:
                return True
            else:
                return False
