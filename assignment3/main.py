from lib.ipy_lib import SnakeUserInterface
from lib.util import height, width, scale
from controller import *
from model import *


def processEvent(event, snakeController, appleController, ui):
    if event.name == 'alarm':
        ui.clear()
        appleController.placeApple()
        snakeController.animateSnake()
        snakeController.placeSnake()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale
    )
    ui.set_animation_speed(30)
    snake = Snake(height, width)
    snakeController = SnakeController(snake, ui)
    
    while True:
        snakeController.placeSnake()
        ui.show()


if __name__ == "__main__":
    main()
