'''
csci4155 A7 reinforcement learning
'''
import random
import matplotlib.pyplot as plt
import time
import math
import sys
import numpy as np

def move(player, b, g, gs):
    # check value of each possible move that could be made from current state
    maxValue = (-(sys.maxint - 1))
    maxValueMoves = []
    otherMoves = []
    n = len(b)
    global totalMoves
    totalMoves+=1
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

    size = len(otherMoves)
    oSize = size>0
    oR = random.random()
    oPick = oR<0.1 # %10 of time choose some random valid move
    p1Rand = (gs%2==0 and player==1)
    p2Rand = (gs%2==1 and player==0)
    if g<70000 and (g<10000 or p1Rand or p2Rand) and oSize and oPick:
        b[random.choice(otherMoves)] = player
        global randNonOptimals
        randNonOptimals+=1

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
            return (0, b[i[0]]) #stop playing, winner
    if -1 in b:
        return (1, -1) #continue playing, no winner
    else:
        if DEBUG:
            print 'draw'
        return (0, -1) #stop playing, no winner

def getValue(player, b):
    key = `b[0]`+`b[1]`+`b[2]`+`b[3]`+`b[4]`+`b[5]`+`b[6]`+`b[7]`+`b[8]`
    if not key in v or key=='-1-1-1-1-1-1-1-1-1':
        return defaultValue
    else:
        return v[key]

def checkValue(v,key):
    if not key in v or key=='-1-1-1-1-1-1-1-1-1':
        return defaultValue
    else:
        return v[key]

def updateValues(player, reward, b, lm):
    learningRate = 0.15

    #handle all 8 equivalent (rotation and mirrored) board layouts
    equivalent = [[0,1,2, 3,4,5, 6,7,8], #regular board
                (2,5,8, 1,4,7, 0,3,6), #rotations...
                (8,7,6, 5,4,3, 2,1,0),
                (6,3,0, 7,4,1, 8,5,2),

                (2,1,0, 5,4,3, 8,7,6), #mirrored board
                (0,3,6, 1,4,7, 2,5,8), #rotations...
                (6,7,8, 3,4,5, 0,1,2),
                (8,5,2, 7,4,1, 6,3,0)]

    lmkey = ''
    key = ''

    if reward!=0: #update value for winning state
        for i in equivalent:
            key = `b[i[0]]`+`b[i[1]]`+`b[i[2]]`+`b[i[3]]`+`b[i[4]]`+`b[i[5]]`+`b[i[6]]`+`b[i[7]]`+`b[i[8]]`

            if not key in v:
                v[key] = reward
            else:
                if checkReward(v[key],reward):
                    print key
                    print 'v[key]:'+`v[key]`+' reward:'+`reward`
                    raise
                v[key] = reward

    else: #it's an intermediate update
        batchUpdate =[]*len(equivalent)
        #need to do a batch update to all rotation at same time to prevent recursive updates
        for i in equivalent:
            lmkey = `lm[i[0]]`+`lm[i[1]]`+`lm[i[2]]`+`lm[i[3]]`+`lm[i[4]]`+`lm[i[5]]`+`lm[i[6]]`+`lm[i[7]]`+`lm[i[8]]`
            key = `b[i[0]]`+`b[i[1]]`+`b[i[2]]`+`b[i[3]]`+`b[i[4]]`+`b[i[5]]`+`b[i[6]]`+`b[i[7]]`+`b[i[8]]`
            batchUpdate.append([lmkey, key, checkValue(v,lmkey), checkValue(v,key)])
            #             u       0     1          2                    3

        for u in batchUpdate:
            v[u[0]] = learningRate * (reward + u[3] - u[2])
#             print 'w/v[key]',checkValue(v,u[1]),' v[lmkey] update', u[2],'->', checkValue(v,u[0])

def checkReward(oldValue, reward):
    if oldValue == -reward:
        return True
    if oldValue==rewardDraw and (reward==rewardWin or reward==rewardLoss):
        return True
    if (oldValue==rewardWin or oldValue==rewardLoss) and reward==rewardDraw:
        return True
    return False

def tictactoe(numGames):
    size = 3
    playerScores = [0]*(numPlayers+1) #add draws
    results = []
    inter = [0]*(numPlayers+1)
    inters=0
    gs=0

    for g in xrange(numGames):

        board = [-1]*(size*size)
        previousBoard = board[:]
        lastMove = board[:]
        otherLastMove = board[:]
        player = 1 #random.randint(0, 1)
        winner = -1
        continuePlaying = 1
        old = 0
        if g%10000==0:
            gs+=1
        if DEBUG:
            printBoard(board, size)
        while continuePlaying:
            otherLastMove = lastMove[:]
            lastMove = previousBoard[:]
            previousBoard = board[:]
            move(player,board, g, gs)
            if DEBUG:
                printBoard(board, size)
                old = getValue(player,board)
            continuePlaying, winner = scoreGame(board)
            #update only this players values
            updateValues(player, 0, board, lastMove)
            if DEBUG:
                new = getValue(player, board)
                if old != new:
                    print old,'->',new,'\n'
            if continuePlaying:
                player = (player+1) % 2

        #reward
        inters+=1
        if winner == -1: #draw
            playerScores[numPlayers] += 1
            inter[winner] += 1
            updateValues(player, rewardDraw, board, lastMove)
            updateValues( (player+1)%2, rewardDraw, previousBoard, otherLastMove)
        else: #winner==player
            playerScores[winner] +=1
            inter[winner]+=1
            updateValues(player, rewardWin, board, lastMove)
            updateValues( (player+1)%2, rewardLoss, previousBoard, otherLastMove)

        if DEBUG:
            new = getValue(player, board)
            if old != new:
                print old,'->',new,'\n'

        if (g<1000 and g%10==0) or g%1000==0:
            result = [g+1]
            for i in xrange(numPlayers):
                result.append(float(playerScores[i])/(g+1))
            result.append(float(playerScores[numPlayers])/(g+1))
            result.append(len(v))
            result.append(len(winning[0])+len(winning[1]))
            result.append(float(randNonOptimals)/totalMoves)
            result.append(float(inter[numPlayers])/inters)
            for i in xrange(numPlayers):
                result.append(float(inter[i])/inters)
            inters=0
            inter =[0]*(numPlayers+1)
            results.append(result)


        #intermediate results
        if DEBUG or g%1000 == 0:
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
    first.scatter (x=results[:,0], y=results[:,8], s=25, c=cmap(0.9), marker='o')
    first.scatter (x=results[:,0], y=results[:,9], s=25, c=cmap(0.9), marker='x')
    first.scatter (x=results[:,0], y=results[:,3], s=25, c=cmap(0.5), marker='_', label="draw")
    first.scatter (x=results[:,0], y=results[:,7], s=25, c=cmap(0.9), marker='_', label="interdraw")
    first.scatter (x=results[:,0], y=results[:,6], s=25, c=cmap(0.9), marker='+', label="randNonOpt")
    second.scatter(x=results[:,0], y=results[:,4], s=25, c=cmap(0.1), marker='1', label="states")
    second.scatter(x=results[:,0], y=results[:,5], s=25, c=cmap(0.3), marker='2', label="winning")

#     first.lim([0,1])
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
    print 'randNonOptimals', float(randNonOptimals)/totalMoves
    print 'boards ', len(v)
    print 'winning', len(winning[0])+len(winning[1])
    for j in xrange(0,size):
        for k in xrange(0,size):
            boardkey = [-1]*(size*size)
            boardkey[j*size+k] = 1
            boardkey = ''.join(str(x) for x in boardkey)
            if boardkey in v:
                print 'pos '+ `j` +':'+`k` + ' ' + `v[boardkey]`
    print "====================="



DEBUG = False
rewardDraw = 1
rewardWin = 5
rewardLoss = -rewardWin
defaultValue = 0.1
numPlayers = 2
v = {}
winning = [{}]*numPlayers
randNonOptimals = 0
totalMoves = 0

tictactoe(100000)
