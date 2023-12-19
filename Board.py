from copy import deepcopy

class Board:

    def __init__(self,n):
        self.__BoardSize = n
        self.__MovCounter = 0
        self.__GoalBoard = list()
        self.__SearchTree = {} # tree
        self.__Solution = list()

    def setSearchSpace(self, space):
        self.__SearchTree = deepcopy(space)

    def getRestPath(self):
        return self.__Solution

    def getSolution(self):
        self.getPath()  # ['left','down','right']
        self.__Solution.reverse()
        return self.__Solution

    def clearSolution(self):
        self.__Solution = list()

    def setBOARDERSIZE(self, N):
        self.__BoardSize = N

    def getBOARDERSIZE(self):
        return self.__BoardSize

    def getTILESIZE(self):
        return int(250 / self.__BoardSize)

    def getMovCounter(self):
        return self.__MovCounter

    def incMovCounter(self):
        self.__MovCounter += 1

    def resetMovCounter(self):
        self.__MovCounter = 0


    # space is searchspace map of keys : [0:state, 1:heuristec value, 2:lastmove, 3:parentState key]
    # 13: [[[1, 4, 7], [2, 5, 8], [3, 6, None]], 0, 'up', 13]  THIS IS soluation
    def getPath(self):
        laststate = self.__SearchTree.popitem()  # laststate is goal  # __SearchSpace is tree
        # print("this is last",laststate)
        key = laststate[1][3]  # key = is parent
        # print("key",key)
        # self.__Solution.append(laststate[1][2])
        while True:
            if (self.__SearchTree.get(key))[3] == -1:
                break
            self.__Solution.append(self.__SearchTree.get(key)[2])
            # print(self.__Solution)
            # self.__Solution.append(laststate[1][2])
            key = self.__SearchTree.get(key)[3]


    def getGoal(self):
       if self.__BoardSize==3:
           return [[1, 4, 7], [2, 5, 8], [3, 6, None]]

       elif self.__BoardSize==4:
           return [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, None]]
       else:
           return [[1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24], [5, 10, 15, 20, None]]

