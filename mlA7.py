'''
csci4155 A7 reinforcement learning
'''
import random
import matplotlib.pyplot as plt
import time
import math
import sys

def move(player, b):
    # check value of each possible move that could be made from current checkValu
    maxValue = (-(sys.maxint - 1))
    maxValueMoves = []
    n = len(b)
    for move in xrange(n):
        if b[move] == -1:
            key = b[:]
            key[move] = player
            predictedValue = getValue(player, key)
            if predictedValue > maxValue:
                maxValue = predictedValue
                del maxValueMoves[:]
                maxValueMoves.append(move)
            elif predictedValue == maxValue:
                maxValueMoves.append(move)

    # make move with highest value
    if len(maxValueMoves) > 0:
        b[random.choice(maxValueMoves)] = player

    else:
        raise NameError('failed on finding a move')

def scoreGame(board):
    win_cond = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for i in win_cond:
        if board[i[0]] != -1 and board[i[0]] == board[i[1]] and board[i[1]] == board[i[2]]:
            b = board
            key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`
            if key not in winning[board[i[0]]]:
                winning[board[i[0]]][key] = key
            if DEBUG:
                print 'winner',board[i[0]]
            return (0, board[i[0]])
    if -1 in board:
        return (1, -1)
    else:
        if DEBUG:
            print 'draw'
        return (0, -1)

def getValue(player, b):
    v = V[player]
    key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`
    if not key in v:
        return defaultValue
    else:
        return v[key]

def updateValues(player, reward, b, lm):
    learningRate = 0.15
    v = V[player]

    #handle all 8 equivalent (rotation and mirrored) board layouts
    equivalent = ((0,1,2, 3,4,5, 6,7,8),
                  (2,5,8, 1,4,7, 0,3,6),
                  (8,7,6, 5,4,3, 2,1,0),
                  (3,6,0, 7,4,1, 8,5,2),

                  (2,1,0, 5,4,3, 8,7,6),
                  (0,3,6, 1,4,7, 2,5,8),
                  (6,7,8, 3,4,5, 0,1,2),
                  (8,5,2, 7,4,1, 6,3,0))

    lmkey = ''
    key = ''
    for i in equivalent:
        lmkey = `lm[i[0]]`+`lm[i[1]]`+`lm[i[2]]`+`lm[i[3]]`+`lm[i[4]]`+`lm[i[5]]`+`lm[i[6]]`+`lm[i[7]]`+`lm[i[8]]`
        key = `b[i[0]]`+`b[i[1]]`+`b[i[2]]`+`b[i[3]]`+`b[i[4]]`+`b[i[5]]`+`b[i[6]]`+`b[i[7]]`+`b[i[8]]`

        if reward != 0:
            #update value for winning state
            if not key in v:
                v[key] = reward
            else:
                v[key] = reward if reward!=0 else v[key]

        else:
            #update value that led to current state
            if not key in v:
                v[key] = defaultValue
            if not lmkey in v:
                v[lmkey] = defaultValue

            v[lmkey] = learningRate * (reward + v[key] - v[lmkey])

def tictactoe(numGames):
    size = 3
    playerScores = [0]*(numPlayers+1) #add one to store draws
    results = []
    resultRate = int(math.sqrt(numGames))

    for g in xrange(numGames):

        board = [-1]*(size*size)
        previousBoard = board[:]
        lastMove = board[:]
        otherLastMove = board[:]
        player = 1 #random.randint(0, 1)
        winner = -1
        continuePlaying = 1
        while continuePlaying:
            otherLastMove = lastMove[:]
            lastMove = previousBoard[:]
            previousBoard = board[:]
            move(player,board)
            continuePlaying, winner = scoreGame(board)
            if continuePlaying:
                #update only this players values
                old = getValue(player, lastMove)
                updateValues(player, 0, board, lastMove)
                player = (player+1) % 2

        if DEBUG:
            old = [0.0]*4
            old[0] = getValue((player+1) % 2, otherLastMove)
            old[1] = getValue(player, lastMove)
            old[2] = getValue((player+1) % 2, previousBoard)
            old[3] = getValue(player, board)

        #reward
        rewardDraw = 2
        rewardWin = 5
        rewardLoss = -rewardWin
        if winner == -1: #draw
            playerScores[numPlayers] += 1
            updateValues(player, rewardDraw, board, lastMove)
            updateValues( (player+1)%2, rewardDraw, previousBoard, otherLastMove)
        else: #winner==player
            playerScores[winner] +=1
            updateValues(player, rewardWin, board, lastMove)
            updateValues( (player+1)%2, rewardLoss, previousBoard, otherLastMove)

        if DEBUG:
            print 'last four moves on the board were....'
            printBoard(otherLastMove, size)
            print old[0],'->',getValue((player+1) % 2, otherLastMove),'\n'
            printBoard(lastMove, size)
            print old[1],'->',getValue(player, lastMove),'\n'
            printBoard(previousBoard, size)
            print old[2],'->',getValue((player+1) % 2, previousBoard),'\n'
            printBoard(board, size)
            print old[3],'->',getValue(player, board),'\n'

        if (g<1000 and g%10==0) or g%resultRate == 0:
            result = [g+1]
            for i in xrange(numPlayers):
                result.append(float(playerScores[i])/(g+1))
            result.append(float(playerScores[numPlayers])/(g+1))
            result.append(len(V[0]))
            result.append(len(winning[0])+len(winning[1]))
            results.append(result)

        #intermediate results
        if DEBUG or g%resultRate == 0:
            printStats(playerScores, g, player, size)
#             time.sleep(5)

    graphResults(results, numGames)

def graphResults(results, numGames):
    #graph results
    fig, ax = plt.subplots()
    fig.canvas.draw()
    first = fig.add_subplot(111)
    second = first.twinx()
    cmap = plt.cm.get_cmap('spectral')
    game = [0]*len(results)
    X = [0]*len(results)
    O = [0]*len(results)
    D = [0]*len(results)
    B = [0]*len(results)
    W = [0]*len(results)
    i = 0
    for g in results:
        game[i] = g[0]
        X[i] = g[1]
        O[i] = g[2]
        D[i] = g[3]
        B[i] = g[4]
        W[i] = g[5]
        i+=1
    first.scatter (x=game, y=X, s=25, c=cmap(0.7), marker='o')
    first.scatter (x=game, y=O, s=25, c=cmap(0.8), marker='x')
    first.scatter (x=game, y=D, s=25, c=cmap(0.5), marker='_', label="draw")
    second.scatter(x=game, y=B, s=25, c=cmap(0.1), marker='1', label="states")
    second.scatter(x=game, y=W, s=25, c=cmap(0.3), marker='2', label="winning")

    plt.xlabel("games")
    plt.xlim([0,numGames])
    plt.legend()

    plt.show()


def printBoard(board, size):

    for i in range(size):
        print " ",
        for j in range(size):
            if board[i*size+j] == 1:
                print 'X',
            elif board[i*size+j] == 0:
                print 'O',
            elif board[i*size+j] != -1:
                print board[i*size+j]-1,
            else:
                print ' ',

            if j != 2:
                print " | ",
        print

        if i != 2:
            print "-----------------"
        else:
            print

def printStats(playerScores, g, player, size):
    for i in xrange(numPlayers):
        print 'player' + `i` + ' score: ' + `float(playerScores[i]) / (g + 1)`
    print 'draws: ' + `float(playerScores[numPlayers]) / (g + 1)`
    print 'done game', g
    print 'boards O:', len(V[0]), ' X:',len(V[1])
    print 'winning', len(winning[0])+len(winning[1])
    v = V[1]
    for j in xrange(0,size):
        for k in xrange(0,size):
            boardkey = [-1]*(size*size)
            boardkey[j*size+k] = 1
            boardkey = ''.join(str(x) for x in boardkey)
            if boardkey in v:
                print 'pos '+ `j` +':'+`k` + ' ' + `v[boardkey]`
    print "====================="



DEBUG = False
defaultValue = 0.1
numPlayers = 2
V = [{}]*numPlayers
winning = [{}]*numPlayers

tictactoe(5000)
