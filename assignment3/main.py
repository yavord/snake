from lib.ipy_lib import SnakeUserInterface
from lib.util import height, width, scale
from lib.process_event import processEvent
from controller import *
from model import *


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale
    )
    ui.set_animation_speed(30)
    snake = Snake(height, width)
    apple = Apple()
    snakeController = SnakeController(snake, ui)
    appleController = AppleController(apple, ui)
    
    while True:
        event = ui.get_event()
        processEvent(event, snakeController, appleController, ui)


if __name__ == "__main__":
    main()
