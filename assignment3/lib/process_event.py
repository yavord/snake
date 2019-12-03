def processEvent(event, snakeController, appleController, ui, width, height):
    if event.name == 'alarm':
        ui.clear()
        snakeController.animateSnake()
        snakeController.placeSnake()
        appleController.placeApple()
        snakeController.updateDirections()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)
