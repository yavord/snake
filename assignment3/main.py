from lib import util
from lib.ipy_lib import SnakeUserInterface
from model import Apple
from model import Snake
from controller import SnakeController


def main():
    ui = SnakeUserInterface(
        util.height,
        util.width,
        util.scale
    )
    ui.set_animation_speed(30)
    
    snake = Snake()
    # apple = Apple()

    snakeController = SnakeController(snake, ui)
    # appleController = AppleController(apple, ui)
    
    while True:
        snakeController.placeSnake()
        ui.show()

if __name__ == "__main__":
    main()
