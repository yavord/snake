from lib import *
from model import *
from controller import SnakeController


def main():
    ui = SnakeUserInterface(
        height,
        width,
        scale
    )
    ui.set_animation_speed(30)
    
    snake = Snake()

    snakeController = SnakeController(snake, ui)
    
    while True:
        snakeController.placeSnake()
        ui.show()

if __name__ == "__main__":
    main()
