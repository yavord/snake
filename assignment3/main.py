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
    
    

    while True:
        ui.show()

if __name__ == "__main__":
    main()
