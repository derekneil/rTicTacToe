'''
csci4155 A7 reinforcement learning
'''
import math
import random

def state(player, key):
    playerStates = states[player]
    if not key in playerStates:
        playerStates[key] = 0.1
    return playerStates[key]

def move(player, b):
    # check value of each possible move that could be made from current state
    key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`
    maxValue = 0
    maxValueMoves = []
    n = len(b)
    for move in xrange(n):
        if b[move] == -1:
            temp = list(key)[move] = `player`
            stateKey = ''.join(temp)
            predictedValue = state(player, stateKey)
            if predictedValue > maxValue:
                maxValue = predictedValue
                del maxValueMoves[:]
                maxValueMoves.append(move)
            elif predictedValue == maxValue:
                maxValueMoves.append(move)

    # make move with highest value
    if len(maxValueMoves) == 1:
        b[maxValueMoves[0]] = player

    #or pick randomly from those with highest value
    elif len(maxValueMoves) > 1:
        b[random.choice(maxValueMoves)] = player

    else:
        print 'fail whale, afraid to make a move?'

def scoreGame(board):
    win_cond = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(3,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in win_cond:
        if board[each[0]] != -1 and board[each[0]] == board[each[1]] and board[each[1]] == board[each[2]]:
            if DEBUG:
                print 'winner',board[each[0]]
            return (0, board[each[0]])
    if -1 in board:
        return (1, -1)
    else:
        if DEBUG:
            print 'draw'
        return (0, -1)

def updateValues(rewards, b, pb):
    learningRate = 0.25
    for i, reward in enumerate(rewards):
        playerFitness = fitness[i]

        pkey = `pb[0]`+`pb[1]`+`pb[2]`+`pb[3]`+`pb[4]`+`pb[5]`+`pb[6]`+`pb[7]`+`pb[8]`
        key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`

        #update value for winning state
        if not key in playerFitness:
            playerFitness[key] = reward

        #update value that led to winning state
        if not pkey in playerFitness:
            playerFitness[pkey] = 0.1
        playerFitness[pkey] += learningRate * (reward + playerFitness[key] - playerFitness[pkey])

def updateValue(player, b, pb):
    learningRate = 0.25
    playerFitness = fitness[player]

    pkey = `pb[0]`+`pb[1]`+`pb[2]`+`pb[3]`+`pb[4]`+`pb[5]`+`pb[6]`+`pb[7]`+`pb[8]`
    key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`

    #update value that led to current state
    if not pkey in playerFitness:
        playerFitness[pkey] = 0
    if not key in playerFitness:
        playerFitness[key] = 0.1
    playerFitness[pkey] += learningRate * (playerFitness[key] - playerFitness[pkey])

def tictactoe():
    size = 3

    numGames = 10000
    playerScores = [0]*(numPlayers+1)

    learning = []

    for g in xrange(numGames):
        board = [-1]*(size*size)
        previousBoard = board[:]
        lastMove = board[:]
        rewards = [0]*numPlayers
        player = random.randint(0, 1)
        winner = -1
        continuePlaying = 1
        while continuePlaying:
#             print 'player',player
            lastMove = previousBoard[:]
            previousBoard = board[:]
            move(player,board)
            player = (player + 1) % 2
            continuePlaying, winner = scoreGame(board)
            if continuePlaying:
                #update only this players values
                updateValue(player, board, lastMove)

        if DEBUG:
            print 'last three moves were....'
            print_board(lastMove)
            print_board(previousBoard)
            print_board(board)

        #reward
        if winner == -1:
            playerScores[numPlayers] += 1
            for i in xrange(numPlayers):
                rewards[i] += 0.1
        else:
            playerScores[winner] +=1
            rewards[winner] += 5
            for i in xrange(numPlayers):
                if i != winner:
                    rewards[i] -= 5

        updateValues(rewards, board, lastMove)

        #remember center value for after this game
        result = [g+1]
        for i in xrange(numPlayers):
            f = fitness[player]
            if '-1-1-1-10-1-1-1-1' in f:
                result.append(f['-1-1-1-10-1-1-1-1'])
            else:
                result.append(0)
            if '-1-1-1-11-1-1-1-1' in f:
                result.append(f['-1-1-1-11-1-1-1-1'])
            else:
                result.append(0)
        learning.append(result)

        #intermediate results
        if DEBUG:
            for i in xrange(numPlayers):
                print 'player'+`i+1`+' score: '+`float(playerScores[i])/(g+1)`

                if '-1-1-1-10-1-1-1-1' in f:
                    print 'player'+`i+1`+' center0 V: '+`fitness[player]['-1-1-1-10-1-1-1-1']`
                if '-1-1-1-11-1-1-1-1' in f:
                    print 'player'+`i+1`+' center1 V: '+`f['-1-1-1-11-1-1-1-1']`
            print 'draws: '+`float(playerScores[numPlayers])/(g+1)`
            print 'done game',g
            print "====================="
        else:
            if g%1000 == 0:
                for i in xrange(numPlayers):
                    print 'player'+`i+1`+' score: '+`float(playerScores[i])/(g+1)`
                    f = fitness[player]
                    if '-1-1-1-10-1-1-1-1' in f:
                        print 'player'+`i+1`+' center1 V: '+`fitness[player]['-1-1-1-10-1-1-1-1']`
                    if '-1-1-1-11-1-1-1-1' in f:
                        print 'player'+`i+1`+' center0 V: '+`f['-1-1-1-11-1-1-1-1']`
                print 'draws: '+`float(playerScores[numPlayers])/(g+1)`
                print 'done game',g
                print "====================="

    #final result
    for i in xrange(numPlayers):
        print 'player'+`i+1`+' score: '+`float(playerScores[i])/numGames`
        f = fitness[player]
        if '-1-1-1-10-1-1-1-1' in f:
            print 'player'+`i+1`+' center0 V: '+`fitness[player]['-1-1-1-10-1-1-1-1']`
        if '-1-1-1-11-1-1-1-1' in f:
            print 'player'+`i+1`+' center1 V: '+`f['-1-1-1-11-1-1-1-1']`
    print 'draws: '+`float(playerScores[numPlayers])/numGames`
    print 'games:',numGames
    print "====================="


def print_board(board):

    for i in range(3):
        print " ",
        for j in range(3):
            if board[i*3+j] == 1:
                print 'X',
            elif board[i*3+j] == 0:
                print 'O',
            elif board[i*3+j] != -1:
                print board[i*3+j]-1,
            else:
                print ' ',

            if j != 2:
                print " | ",
        print

        if i != 2:
            print "-----------------"
        else:
            print


'''

'''
def fourinarow():
    board = [[-1 for x in range(4)] for x in range(4)]
    print 'four',board

#run them
DEBUG = False
numPlayers = 2
states = [{}]*numPlayers
fitness = [{}]*numPlayers

tictactoe()

# fourinarow()
