def processEvent(event, snakeController, appleController, ui):
    if event.name == 'alarm':
        ui.clear()
        snakeController.animateSnake()
        snakeController.placeSnake()
        snakeController.updatePositions()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)
