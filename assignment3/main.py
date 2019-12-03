from lib.ipy_lib import SnakeUserInterface
from lib.util import height, width, scale, speed
from lib.process_event import processEvent
from controller import *
from model import *


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale
    )
    ui.set_animation_speed(speed)
    snake = Snake(height, width)
    apple = Apple()
    snakeController = SnakeController(snake, ui)
    appleController = AppleController(apple, ui)
    snakeController.placeSnake()
    
    while True:
        event = ui.get_event()
        processEvent(event, snakeController, appleController, ui)
        print(snake.snake[0].direction)


if __name__ == "__main__":
    main()
