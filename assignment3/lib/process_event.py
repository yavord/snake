def processEvent(event, snakeController, appleController, ui, width, height):
    if event.name == 'alarm':
        ui.clear()
        snakeController.animateSnake()
        snakeController.placeSnake()
        appleController.placeApple()
        if snakeController.checkSnakePosition(appleController.apple) == True:
            snakeController.eatApple()
            appleController.getNewApple(width, height)
        snakeController.updateDirections()
        ui.show()
    elif event.name == 'arrow':
        snakeController.changeDirection(event.data)
