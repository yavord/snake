from ipy_lib import SnakeUserInterface


height = 100
width = 100
scale = 0.5


class WallController:
    def __init__(self, ui, wall):
        self.ui = ui
        self.wall = wall

    def processEvent(self):
        event = self.ui.get_event()
        print(event.name)

        if event.name == 'alarm':
            self.ui.print_('fps tick ')
