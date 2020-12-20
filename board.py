
import random

def index(x, y):
    return y * Board.BOARDWIDTH + x

def addVec(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

class Board:
    BOARDWIDTH = 8
    BOARDHEIGHT = 8
    positionModifiers = (
        (1, 0), (0, 1),
        (1, 1), (1, -1))
    startPositionModifiers = (
        (-3, 0), (0, -3),
        (-3, -3), (-3, 3))

    def __init__(self):
        self._board = [" " for i in range(self.BOARDWIDTH * self.BOARDHEIGHT)]
        self._boardFreeSlots = [0 for i in range(self.BOARDWIDTH)]

        self.win = False
        self.winner = "None"

    ## Drop a token into a column, so that it falls to the lowest possible row
    def drop(self, column, colour):
        if column < 0 or column >= self.BOARDWIDTH:
            raise IndexError("Cannot drop token off edges of board")
        row = self._boardFreeSlots[column]
        if row >= self.BOARDHEIGHT:
            raise IndexError("Cannot add token to full column")

        self._boardFreeSlots[column] += 1
        self._board[index(column, row)] = colour
        return [column, row] ## Valid, return position

    ## Remove token from board
    def remove(self, column, row):
        self._boardFreeSlots[column] -= 1
        row = self._boardFreeSlots[column]
        self._board[index(column, row)] = " "

    def __str__(self):
        string = list()
        for y in range(self.BOARDHEIGHT, 0, -1):
            string.append("|")
            for x in range(self.BOARDWIDTH):
                string.append(self._board[index(x, y - 1)])
                string.append("|")
            string.append("\n")
        return "".join(string)

    def checkWinLocal(self, x, y, colour):
        # Locally check for a win around a single position
        # \|/
        # -+-
        # /|\
        for i in range(4):
            ## Loop over each branch of the star (parallel branches are done as one)
            numInARow = 0
            pos = addVec([x, y], self.startPositionModifiers[i])
            for _ in range(7):
                ## Check for out of bounds
                if (not (0 <= pos[0] < self.BOARDWIDTH)
                    or not (0 <= pos[1] < self.BOARDHEIGHT)):
                    pos = addVec(pos, self.positionModifiers[i])
                    continue
                ## Traverse along branch
                if self._board[index(pos[0], pos[1])] == colour:
                    numInARow += 1
                else:
                    numInARow = 0
                if numInARow >= 4:
                    self.win = True
                    self.winner = colour
                    return True
                pos = addVec(pos, self.positionModifiers[i])
        return False

    def columnIsFilled(self, column):
        return self._boardFreeSlots[column] == Board.BOARDHEIGHT

def drawBoard(board):
    print(" 1 2 3 4 5 6 7 8")
    print(" v v v v v v v v")
    print(board)

def swapColour(colour : str):
    if colour == "O":
        return "X"
    elif colour == "X":
        return "O"


































