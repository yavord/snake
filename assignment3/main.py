from ipy_lib import SnakeUserInterface
import util
from model import *
from controller import *


def main():
    ui = SnakeUserInterface(
        util.height,
        util.width,
        util.scale
    )
    ui.set_animation_speed(30)
    
    snake = Snake()
    apple = Apple()

    snakeController = SnakeController(snake, ui)
    appleController = AppleController(apple, ui)
    
    while True:
        snakeController.placeSnake()
        ui.show()

if __name__ == "__main__":
    main()
