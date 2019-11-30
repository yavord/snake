from ipy_lib import SnakeUserInterface
import ui
import wall
import controller


def main():
    w = wall.Wall()
    u = ui.Ui()

    while True:
        u.processEvent()


if __name__ == "__main__":
    main()
