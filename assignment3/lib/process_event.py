def processEvent(event, snakeController, appleController, ui):
    if event.name == 'alarm':
        ui.clear()
        snakeController.animateSnake()
        snakeController.updatePositions()
        snakeController.placeSnake()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)
