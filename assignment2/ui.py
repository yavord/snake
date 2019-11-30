from ipy_lib import SnakeUserInterface

height = 50
width = 50
scale = 0.5

class Ui:
    def __init__(self):
        self.ui = SnakeUserInterface(height, width, scale)

    def processEvent(self):
        self.ui.set_animation_speed = 5
        event = self.ui.get_event()
        print('name: '+event.name+' data: '+event.data)

        if event.name == 'alarm':
            self.ui.print_('fps tick ')
