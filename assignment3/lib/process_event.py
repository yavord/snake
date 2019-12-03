def processEvent(event, snakeController, appleController, ui):
    if event.name == 'alarm':
        ui.clear()
        # appleController.placeApple()
        snakeController.animateSnake()
        snakeController.placeSnake()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)
