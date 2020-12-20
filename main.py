from board import Board, drawBoard, swapColour
from ai import AI

def getUserInput(board):
    column = int(input("Choose slot: ")) - 1
    while not (0 <= column < Board.BOARDWIDTH) or board._boardFreeSlots[column] == Board.BOARDHEIGHT:
        print("Please choose a valid slot.")
        column = int(input("Choose slot: ")) - 1
    print()
    return column

def gameLoop():

    playerColour = "O"
    aiColour = "X"
    currentColour = playerColour

    board = Board()
    ai = AI(aiColour, playerColour, board)
    win = False

    while not win:
        drawBoard(board)

        if currentColour == playerColour:
            print("Your turn!")
            userInput = getUserInput(board)
            tokenPosition = board.drop(userInput, currentColour)
        elif currentColour == aiColour:
            print("AI is thinking!")
            tokenPosition = ai.makeMove()

        if board.checkWinLocal(*tokenPosition, currentColour):
            win = True
            if currentColour == playerColour:
                print("----- You Win! -----")
            elif currentColour == aiColour:
                print("----- AI Wins! -----")
            drawBoard(board)

        ai.updateInternalBoard()
        currentColour = swapColour(currentColour)


if __name__ == "__main__":
    gameLoop()
