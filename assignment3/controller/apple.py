
class AppleController:
    def __init__(self, apple, ui):
        self.apple = apple
        self.ui = ui

    def placeApple(self):
        self.apple.getNewApple()