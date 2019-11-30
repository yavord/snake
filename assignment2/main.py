from ipy_lib import SnakeUserInterface
import util





def processEvent(event, ui):
    if event.name == 'click':
        coords = event.data.split(' ')
        ui.place(int(coords[0]), int(coords[1]), 6)
        ui.print_('wall placed at '+coords[0]+' '+coords[1]+' ')
        ui.show()
    elif event.data == 'space':
        ui.clear()
        ui.show()
        ui.print_('space pressed, ui cleared ')
    elif event.name == 'alarm':
        ui.print_('fps tick ')


def main():
    ui = SnakeUserInterface(
        util.dimensions['width'], 
        util.dimensions['height'], 
        util.dimensions['scale']
        )
    
    ui.set_animation_speed(util.animationSpeed)

    while True:
        event = ui.get_event()
        processEvent(event, ui)


if __name__ == "__main__":
    main()
