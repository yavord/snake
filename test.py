from ipy_lib import SnakeUserInterface
import util


class UiHandler():
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def processEvent(self):
        pass


def main():
    ui = SnakeUserInterface(
        util.dimensions['width'], 
        util.dimensions['height'], 
        util.dimensions['scale']
        )

    while True:
        ui.get_event()
        

if __name__ == "__main__":
    main()
