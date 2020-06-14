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
            if(newNumberOfAttacks == 0):
                break
            if(i > 100):
                if currentNumberOfAttacks <= newNumberOfAttacks:
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

        noAttacks=self.getNumberOfAttacks()
        newAttack=[]

        if noAttacks==0:
            return (self,noAttacks,0,0)
        else:
            for i in range(0,8):
                for j in range(0,8):
                    newAttack.append(self.getCostBoard().squareArray[i][j])
            minNumOfAttack=min(newAttack)
            newList=[]
            for i in range(0,8):
                for j in range(0,8):
                    if self.getCostBoard().squareArray[i][j]==minNumOfAttack:
                        newList.append((i,j))
            newrow,newcol=random.choice(newList)
            for k in range(0,8):
                if self.squareArray[k][newcol]==1:
                    oldrow=k
            betterboard=copy.deepcopy(self)
            betterboard.squareArray[newrow][newcol]=1
            betterboard.squareArray[oldrow][newcol]=0
            return (betterboard,minNumOfAttack,newrow,newcol)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        counter = 0
        for i in range(8):
            temp_row = temp_diag = temp_diag2 = row_queens = 0
            for j in range(8):
                if(self.squareArray[i][j] == 1):
                    row_queens = row_queens + 1
                    if(row_queens > 1):
                        temp_row = temp_row + (row_queens-1)
                    diag_queens1 = 0
                    for k in range(max(i,j), 8):
                        if(i>=j):
                            y = j + k - i
                            x = k
                        else:
                            y = k
                            x = i + k - j
                        if(self.squareArray[x][y] == 1):
                            diag_queens1 = diag_queens1 + 1
                            if(diag_queens1 > 1):
                                temp_diag = temp_diag + 1
                    diag_queens2 = 0
                    if((i+j)<7):
                        temp = i
                    for k in range(i, -1, -1):
                        y = j + i - k
                        x = k
                        if(y <= 7 and self.squareArray[x][y] == 1):
                            diag_queens2 = diag_queens2 + 1
                            if(diag_queens2 > 1):
                                temp_diag2 = temp_diag2 + 1
            counter = counter + temp_row + temp_diag + temp_diag2
        return(counter)

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
