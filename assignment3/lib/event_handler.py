def eventHandler(event, snakeController, appleController, ui, width, height):
    if event.name == 'alarm':
        ui.clear()
        snakeController.animateSnake()
        snakeController.placeSnake()
        appleController.placeApple()
        if snakeController.checkSnakePosition(appleController.apple) == True:
            snakeController.eatApple()
            appleController.getNewApple(width, height)
            for snakePiece in snakeController.snake.snakeList:
                while appleController.checkApplePosition(snakePiece) == True:
                    print('apple/snake check')
                    appleController.getNewApple(width, height)
                    if appleController.checkApplePosition(snakePiece) == False:
                        break
        elif snakeController.checkSnakePosition(appleController.apple) == False:
            snakeController.gameOver()
        snakeController.updateDirections()
        ui.show()
    elif event.name == 'arrow':
        ui.wait(20)
        snakeController.changeDirection(event.data)
