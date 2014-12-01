'''
csci4155 A7 reinforcement learning
'''
import random
import matplotlib.pyplot as plt
import time
import math
import sys
import numpy as np

def move(player, b):
    # check value of each possible move that could be made from current state
    maxValue = (-(sys.maxint - 1))
    maxValueMoves = []
    otherMoves = []
    n = len(b)
    for move in xrange(n):
        if b[move] == -1:
            key = b[:]
            key[move] = player
            predictedValue = getValue(player, key)
            if predictedValue > maxValue:
                maxValue = predictedValue
                otherMoves.extend(maxValueMoves)
                del maxValueMoves[:]
                maxValueMoves.append(move)
            elif predictedValue == maxValue:
                maxValueMoves.append(move)
            else:
                otherMoves.append(move)

    if len(otherMoves) > 0 and random.random() < 0.1: # %10 of time choose some random valid move
        b[random.choice(otherMoves)] = player

    else: # make move with highest value
        if len(maxValueMoves) > 0:
            b[random.choice(maxValueMoves)] = player
        else:
            raise NameError('failed on finding a move')

def scoreGame(b):
    win_cond = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for i in win_cond:
        if b[i[0]] != -1 and b[i[0]] == b[i[1]] and b[i[1]] == b[i[2]]:
            b = b
            key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`
            if key not in winning[b[i[0]]]:
                winning[b[i[0]]][key] = key
            if DEBUG:
                print 'winner',b[i[0]]
            return (0, b[i[0]])
    if -1 in b:
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
    learningRate = 0.25
    v = V[player]

    #handle all 8 equivalent (rotation and mirrored) board layouts
    equivalent = ((0,1,2, 3,4,5, 6,7,8),
                  (2,5,8, 1,4,7, 0,3,6),
                  (8,7,6, 5,4,3, 2,1,0),
                  (6,3,0, 7,4,1, 8,5,2),

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
                if v[key] !=0.1 and v[key] != reward:
                    print key
                    raise NameError('v[key]:'+`v[key]`+' != reward:'+`reward`)
                v[key] = reward

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
        old = 0
        if DEBUG:
                printBoard(board, size)
        while continuePlaying:
            otherLastMove = lastMove[:]
            lastMove = previousBoard[:]
            previousBoard = board[:]
            move(player,board)
            if DEBUG:
                printBoard(board, size)
                old = getValue(player,board)
            continuePlaying, winner = scoreGame(board)
            if continuePlaying:
                #update only this players values
                updateValues(player, 0, board, lastMove)
                if DEBUG:
                    print old,'->',getValue(player, board),'\n'
                player = (player+1) % 2

        #reward
        rewardDraw = 4
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
            print old,'->',getValue(player, board),'\n'

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
    fig, ax = plt.subplots()
    fig.canvas.draw()
    first = fig.add_subplot(111)
    second = first.twinx()
    cmap = plt.cm.get_cmap('spectral')
    results = np.array(results)
    first.scatter (x=results[:,0], y=results[:,1], s=25, c=cmap(0.7), marker='o')
    first.scatter (x=results[:,0], y=results[:,2], s=25, c=cmap(0.8), marker='x')
    first.scatter (x=results[:,0], y=results[:,3], s=25, c=cmap(0.5), marker='_', label="draw")
    second.scatter(x=results[:,0], y=results[:,4], s=25, c=cmap(0.1), marker='1', label="states")
    second.scatter(x=results[:,0], y=results[:,5], s=25, c=cmap(0.3), marker='2', label="winning")

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



DEBUG = True
defaultValue = 0.1
numPlayers = 2
V = [{}]*numPlayers
winning = [{}]*numPlayers

tictactoe(50000)
