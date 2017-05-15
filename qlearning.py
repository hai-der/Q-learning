# Haider Tiwana
# COMP 372: Artificial Intelligence
# Project 4: Nim with Q-learning

from random import randint, seed
from datetime import datetime
from copy import deepcopy

QValues = {}

class Nim(object):
    def __init__(self, array):
        self.board = array
        self.player = "A"
        self.myPile = -1
        self.myObjects = -1

    def randomize(self):
        self.myPile = -1
        self.myObjects = -1
        availablePiles = []

        seed(datetime.now())
        self.myPile = randint(0, 2)

        # find piles that are not 0
        for i in range(len(self.board)):
            if self.board[i] != 0:
                availablePiles.append(i)

        # pick a different pile from available
        myRandom = randint(0, len(availablePiles)-1)
        self.myPile = availablePiles[myRandom]
        self.myObjects = randint(1, self.board[self.myPile])

    def move(self, pilePick, numObjects):

        self.board[pilePick] -= numObjects
        self.player = "A" if self.player == "B" else "B"
        
    def end(self):
        if sum(self.board) == 0:
            return True
        else:
            return False

def QLearning(g):
    temp = deepcopy(g)

    while (not temp.end()):

        stateConfig = ""

        temp.randomize()
        
        stateConfig = temp.player + str(temp.board[0]) + str(temp.board[1]) + str(temp.board[2])
        myTuple = (stateConfig, str(temp.myPile) + str(temp.myObjects))
        
        if myTuple not in QValues.keys():
            QValues[myTuple] = 0

        temp.move(temp.myPile, temp.myObjects)

        result = temp.player + str(temp.board[0]) + str(temp.board[1]) + str(temp.board[2])
        myReward = reward(result)

        myKey = []
        for item in QValues.keys():
            if item[0] == result:
                myKey.append(item)

        keyReward = []
        for item in myKey:
            keyReward.append(QValues[item])

        minimum = 0
        maximum = 0
        
        if len(myKey) != 0:
            minimum = min(keyReward)
            maximum = max(keyReward)


        if temp.player == "A":
            QValues[myTuple] = myReward + (0.9 * maximum)
        elif temp.player == "B":
            QValues[myTuple] = myReward + (0.9 * minimum)

def reward(arr):
    myArr = [int(x) for x in arr[1:]]
    if sum(myArr) != 0:
        return 0
    if arr[0] == "A":
        return 1000
    if arr[0] == "B":
        return -1000

def printQ(myDict):
    q = list(myDict.keys())
    q.sort(key=lambda x: (x[0], x[1]))
    for item in q:
        print("Q[" + str(item[0]) + ", " + str(item[1]) + "] = " + str(myDict[item]))

def main():

    pile1 = int(input("How many in pile 0? "))
    pile2 = int(input("How many in pile 1? "))
    pile3 = int(input("How many in pile 2? "))
    myBoard = [pile1, pile2, pile3]
    game = Nim(myBoard)
    print("Initial board is", str(game.board[0]) + "-" + str(game.board[1]) + "-" + str(game.board[2]) + ", simulating 100,000 games.\n")

    for i in range(100000):
        QLearning(game)

    print("Final Q-values: \n")
    printQ(QValues)

    user = int(input("Who moves first, (1) User or (2) Computer? "))
    playAgain = 1
    while True:
        if user == 1:
            
            print("\nPlayer", str(game.player) + " (user)'s turn; board is (" + str(game.board[0]) + ", " + str(game.board[1]) + ", " + str(game.board[2]) + ").")
            pileNum = int(input("What pile? "))
            numObjects = int(input("How many? "))

            game.move(pileNum, numObjects)
            user = 2 if user == 1 else 1


            if game.end():
                print("\nGame over.")
                winner = game.player
                print("Winner is", winner, "(computer).\n")
                playAgain = int(input("Play again? (1) Yes (2) No: "))
                if playAgain == 1:
                    myBoard = [pile1, pile2, pile3]
                    game = Nim(myBoard)
                    user = int(input("Who moves first, (1) User or (2) Computer? "))
                else:
                    break
            else:
                continue
            
        if user == 2:

            print("\nPlayer", str(game.player) + " (computer)'s turn; board is (" + str(game.board[0]) + ", " + str(game.board[1]) + ", " + str(game.board[2]) + ").")

            state = game.player + str(game.board[0]) + str(game.board[1]) + str(game.board[2])

            # derive policy 
            stateKey = []
            maximum = -1001
            minimum = 1001

            for s in QValues.keys():
                if s[0] == state:
                    stateKey.append(s)
                    if game.player == "A":
                        if QValues[s] > maximum:
                            maximum = QValues[s]
                            myMove = s[1]
                    if game.player == "B":
                        if QValues[s] < minimum:
                            minimum = QValues[s]
                            myMove = s[1]
                    
            game.move(int(myMove[0]), int(myMove[1]))
            print("Computer chooses pile", myMove[0], "and removes", myMove[1], ".")
            user = 1 if user == 2 else 2


            if game.end():
                print("Game over.")
                winner = game.player
                print("Winner is", winner, "(user).\n")
                playAgain = int(input("Play again? (1) Yes (2) No: "))
                if playAgain == 1:
                    myBoard = [pile1, pile2, pile3]
                    game = Nim(myBoard)
                    user = int(input("Who moves first, (1) User or (2) Computer? "))
                else:
                    break
            else:
                continue

        keepGoing = False
        

main()
