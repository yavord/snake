
class Apple:
    def __init__(self):
        self.x = None
        self.y = None
        self.color = 4

    def getNewApple(self, width, height, ui):
        self.x = ui.random(width)
        self.y = ui.random(height)
        
