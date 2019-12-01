from ipy_lib import SnakeUserInterface

height = 49
width = 49
scale = 1

class Ui:
    def __init__(self):
        self.ui = SnakeUserInterface(height+1, width+1, scale)
        self.wall = [0, 0]
        self.animationSpeed = 10


    def setAnimationSpeed(self, action):
        if action == 'decrease':
            if self.animationSpeed <= 0:
                pass
            else:
                self.animationSpeed -= 20
            return self.ui.set_animation_speed(self.animationSpeed)
        elif action == 'increase':
            self.animationSpeed += 20
            return self.ui.set_animation_speed(self.animationSpeed)
        elif action == 'default':
            return self.ui.set_animation_speed(self.animationSpeed)


    def processEvent(self):
        event = self.ui.get_event()
        wall = self.wall
        ui = self.ui
        print('name: '+event.name+' data: '+event.data)
        # print('animation speed: '+str(self.animationSpeed))

        if event.name == 'alarm':
            if wall[0] < width:
                ui.place(wall[0], wall[1], 6)
                ui.show()
                wall[0] += 1
            elif wall[0] == width:
                ui.place(wall[0], wall[1], 6)
                ui.show()
                wall[0] = 0
                if wall[1] < height:
                    wall[1] += 1
                elif wall[1] == height:
                    wall[1] = 1
        elif event.name == 'arrow':
            if event.data == 'l':
                self.setAnimationSpeed('decrease')
            elif event.data == 'r':
                self.setAnimationSpeed('increase')
