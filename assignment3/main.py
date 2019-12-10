from lib import *
from controller import *
from model import *


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale,
    )

    ui.print_('Welcome, please press space to start (or pause) the game. '+'\n')
    snake = Snake(height, width)
    apple = Apple(ui.random(height), ui.random(width))
    snakeController = SnakeController(snake, ui)
    appleController = AppleController(apple, ui)

    while True:
        event = ui.get_event()
        eventHandler(event, snakeController, appleController, ui, width, height)


if __name__ == "__main__":
    main()
