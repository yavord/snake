from ipy_lib import SnakeUserInterface
import util as u


def main():
    ui = SnakeUserInterface(
        u.height,
        u.width,
        u.scale
    )
    ui.set_animation_speed(30)

    while True:
        ui.show()

if __name__ == "__main__":
    main()
