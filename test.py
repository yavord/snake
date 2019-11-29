from ipy_lib import SnakeUserInterface
import util


class UiHandler():
    def __init__(self, ui):
        self.ui = ui

    def processEvent(self, ui):
        event = ui.get_event()
        print(event.name)
        

def processEvent(event):
    print(event.name)

def main():
    ui = SnakeUserInterface(
        util.dimensions['width'], 
        util.dimensions['height'], 
        util.dimensions['scale']
        )

    handler = UiHandler(ui)

    while True:
        handler.processEvent
        

if __name__ == "__main__":
    main()
