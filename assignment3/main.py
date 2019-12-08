from lib import *
from controller import *
from model import *


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale,
    )

    ui.set_animation_speed(speed)
    snake = Snake(height, width)
    # apple = Apple(ui.random(width), ui.random(height))
    apple = Apple(15, 15)
    snakeController = SnakeController(snake, ui)
    appleController = AppleController(apple, ui)

    for snakePiece in snake.snakeList:
        print(snakePiece)

    while True:
        event = ui.get_event()
        eventHandler(event, snakeController, appleController, ui, width, height)


if __name__ == "__main__":
    main()
