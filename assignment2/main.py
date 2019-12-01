from ipy_lib import SnakeUserInterface
import ui as u
import wall as w
# import controller as c


def main():
    ui = u.Ui()
    ui.setAnimationSpeed('default')

    while True:
        ui.processEvent()   


if __name__ == "__main__":
    main()
