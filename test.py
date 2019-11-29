from ipy_lib import SnakeUserInterface
import util


class UiHandler():
    def __init__(self, ui):
        self.ui = ui

    def processEvent(self, self.ui):
        event = ui.get_event()
        pass

def processEvent(event):
    print(event.name)

def main():
    ui = SnakeUserInterface(
        util.dimensions['width'], 
        util.dimensions['height'], 
        util.dimensions['scale']
        )

    while True:
        event = ui.get_event()
        processEvent(event)
        

if __name__ == "__main__":
    main()
