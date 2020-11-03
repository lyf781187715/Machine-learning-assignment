import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if newNumberOfAttacks == 0 or i > 100:
                break

        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        ##squareArray[i][j]==1 的位置就是皇后位置
        board = self.squareArray.copy()
        costBoard = Board(board).getCostBoard().squareArray
        # print('----------------------------------------------------------')
        # print(costBoard)

        minPosition = []
        tempPosition = [0,0]
        minCost = 100
        col = 0
        row = 0
        for i in range(8):
            colMin = min(costBoard[i])
            if colMin == minCost:
                tempPosition[0] = i
                tempPosition[1] = costBoard[i].index(colMin)
                minPosition.append(tempPosition)
            if colMin < minCost:
                minCost = colMin
                minPosition.clear()
                tempPosition[0] = i
                tempPosition[1] = costBoard[i].index(colMin)
                minPosition.append(tempPosition)
        randomPosition = random.choice(minPosition)


        for i in range(8):
            for j in range(8):
                if board[i][j] == 1 and j == randomPosition[1]:
                    board[randomPosition[0]][j] = 1
                    board[i][j] = 0
                    col = j
                    newboard = Board(board)
                    return (newboard, minCost, randomPosition[0], col)

        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HEREY ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        row = {}
        dig1 = {}
        dig2 = {}
        attack = 0
        for i in range(8):
            for j in range(8):
                if self.squareArray[i][j] == 1:
                    if i in row:
                        attack+=row[i]
                        row[i]+=1
                    else:
                        row[i] = 1
                    if (i-j) in dig1:
                        attack+=dig1[i-j]
                        dig1[i-j]+=1
                    else:
                        dig1[i-j] = 1
                    if (i+j) in dig2:
                        attack+=dig2[i+j]
                        dig2[i+j]+=1
                    else:
                        dig2[i+j] = 1

        return attack
        util.raiseNotDefined()


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True) # 如果有-q参数 verbose将被赋值为false，默认为true
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)# 如果有-l参数 lectureExample将被赋值为true，默认为false
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")# 如果有-n 则给numberOfRuns赋值为-n后的数， 不然就是1
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
