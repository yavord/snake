
class AppleController:
    def __init__(self, apple, ui):
        self.apple = apple
        self.ui = ui

    def placeApple(self):
        self.ui.place(self.apple.x, self.apple.y, self.apple.color)

    def getNewApple(self, width, height):
        self.apple.x = self.ui.random(height-1)
        self.apple.y = self.ui.random(width-1)

    def checkApplePosition(self, snake):
        for snakePiece in snake.snake:

        #     print('appleX: '+str(self.apple.x))
        #     print('appleY: '+str(self.apple.y))
        #     print('snakepieceX: '+str(snakePiece.x))
        #     print('snakepieceY: '+str(snakePiece.y))
        # print('run complete')

            if [self.apple.x, self.apple.y]  == [snakePiece.x, snakePiece.y]:
                print('yup')
                return True
            else:
                return False
