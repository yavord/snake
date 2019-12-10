import util

gameOn = False

def eventHandler(event, snakeController, appleController, ui, width, height):
    global gameOn
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
                    appleController.getNewApple(width, height)
                    if appleController.checkApplePosition(snakePiece) == False:
                        break
        elif snakeController.checkSnakePosition(appleController.apple) == False:
            snakeController.gameOver()
        snakeController.updateDirections()
        ui.show()
    elif event.name == 'arrow' and gameOn == True:
            ui.wait(20)
            snakeController.changeDirection(event.data)
    elif event.data == 'space':
        if gameOn == False:
            gameOn = True
            ui.set_animation_speed(util.speed)
        else:
            gameOn = False
            ui.set_animation_speed(0)
            ui.print_('Game paused, please press space to start again '+'\n')
