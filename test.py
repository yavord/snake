from ipy_lib import SnakeUserInterface
import util


# class UiHandler():
#     def __init__(self, events):
#         self.events = events

#     def processEvent(self):
#         event = self.events
#         print(event.name)


def processEvent(event, ui):
    print('name: '+event.name+' data: '+event.data)

    # print(event.data.split(' '))

    if event.name == 'click':
        coords = event.data.split(' ')
        ui.place(int(coords[0]), int(coords[1]), 4)
        ui.print_('wall placed at '+coords[0]+' '+coords[1])
        ui.show
    # else if event.data == 'space':

        


def main():
    ui = SnakeUserInterface(
        util.dimensions['width'], 
        util.dimensions['height'], 
        util.dimensions['scale']
        )

    # handler = UiHandler(ui.get_event())

    while True:
        event = ui.get_event()
        ui.place(50,50,6)
        processEvent(event, ui)
        

if __name__ == "__main__":
    main()
