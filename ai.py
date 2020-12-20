from board import Board, swapColour

from random import randint
from copy import deepcopy
import time


class AI:
    _DEPTH = 4

    def __init__(self, colour, enemyColour, realBoard):
        self._realBoard = realBoard
        self._internalBoard = Board()

        self._colour = colour[0].upper()
        self._enemyColour = enemyColour[0].upper()

        self.winNum = 0

    def makeMove(self):
        newColumn = self.getMinMax()
        return self._realBoard.drop(newColumn, self._colour)

    def getMinMax(self):
        ## For timing AI turn times
        start = time.time()

        ## Getting the minmax for each column
        self._currentMinMax = list()
        minMaxColumnDict = dict()
        for column in range(8):
            self._getMinMaxForColumn(column, minMaxColumnDict, start)

        for i in range(8):
            self._currentMinMax.append(minMaxColumnDict[i])

        ## Put the highest scoring columns into a list to randomly choose from
        highest = [[-99999999, 0], ]
        for column, score in enumerate(self._currentMinMax):
            if score > highest[0][0]:
                highest = [[score, column], ]
            elif score == highest[0][0]:
                highest.append([score, column])

        res = highest[randint(0, len(highest) - 1)][1]
        print("\nAI placed in column {}\n".format(res + 1))
        return res

    def _getMinMaxForColumn(self, column, minMaxColumnDict, startTime):
        value = self._evaluateMove(column, self._colour, self._DEPTH)
        minMaxColumnDict[column] = value
        print("Columns calculated: {}/{} in {} seconds".format(column + 1, 8, round(time.time() - startTime, 4)), end="\r")

    def _evaluateMove(self, column, colour, depth):

        ## If column is filled, the move chain is neutral
        if self._internalBoard.columnIsFilled(column):
            return 0

        isAITurn = colour == self._colour

        pos = self._internalBoard.drop(column, colour)
        win = self._internalBoard.checkWinLocal(*pos, colour)

        ## If the AI wins, this move chain is positive, if the player wins, it's negative
        ## Move chain scores are weighted by how many moves away they are (depth)
        if win and isAITurn:
            value = 1000.0 * depth
        elif win and not isAITurn:
            value = -1000.0 * depth

        ## If the depth has been exhausted, the move chain is neutral
        elif depth == 0:
            value = 0

        ## Otherwise, recurse down the tree for more scores
        else:
            value = self._recurseMove(colour, isAITurn, depth)

        ## Remove the temporary move from the
        ## internal simulation board once the
        ## moves in the chain are being popped off
        self._internalBoard.remove(*pos)
        return value

    def _recurseMove(self, colour, isAITurn, depth):
        value = 0
        for nextColumn in range(8):
            newValue = self._evaluateMove(nextColumn, swapColour(colour), depth-1)
            if abs(newValue) > abs(value):
                value = newValue
        return value

    def updateInternalBoard(self):
        self._internalBoard = deepcopy(self._realBoard)






