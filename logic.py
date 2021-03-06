import numpy as np

#
# CS1010FC --- Programming Methodology
#
# Mission N Solutions
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.
from random import *

#######
#Task 1a#
#######

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 1 mark for creating the correct matrix

def new_game(n):
    """
        Generates n x n grid
    """

    matrix = []

    for i in range(n):
        matrix.append([[0, 0]] * n)

    return matrix

###########
# Task 1b #
###########

# [Marking Scheme]
# Points to note:
# Must ensure that it is created on a zero entry
# 1 mark for creating the correct loop

def addNewValue(mat, turn):
    """
        Adds new value. 
        2 with prob 0.8 and 4 with prob 0.2

        turn can be one of {1, 2}
    """

    # Find two random indices
    a = randint(0, len(mat)-1)
    b = randint(0, len(mat)-1)
    while(mat[a][b][0] != 0):
        a = randint(0, len(mat)-1)
        b = randint(0, len(mat)-1)

    # Assign value (2, 4) with prob (0.8, 0.2)
    if np.random.uniform() < 0.8:
        mat[a][b] = [2, turn]
    else:
        mat[a][b] = [4, turn]

    return mat

###########
# Task 1c #
###########

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 0 marks for completely wrong solutions
# 1 mark for getting only one condition correct
# 2 marks for getting two of the three conditions
# 3 marks for correct checking

def game_state(mat):

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j][0] == 2048:
                return 'win'

    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0]) - 1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j][0] == mat[i + 1][j][0] or mat[i][j + 1][0] == mat[i][j][0]:
                return 'not over'

    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j][0] == 0:
                return 'not over'

    for k in range(len(mat) - 1): #to check the left/right entries on the last row
        if mat[len(mat) - 1][k][0] == mat[len(mat) - 1][k + 1][0]:
            return 'not over'

    for j in range(len(mat) - 1): #check up/down entries on last column
        if mat[j][len(mat) - 1][0] == mat[j + 1][len(mat) - 1][0]:
            return 'not over'

    return 'lose'

###########
# Task 2a #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

def reverse(mat):
    """
        Reverses each row
    """
    new = []
    for i in range(len(mat)):
        new.append(mat[i][:: -1 ])

    del mat
    return new

###########
# Task 2b #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

def transpose(mat):

    new=[]

    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    del mat
    return new

##########
# Task 3 #
##########

# [Marking Scheme]
# Points to note:
# The way to do movement is compress -> merge -> compress again
# Basically if they can solve one side, and use transpose and reverse correctly they should
# be able to solve the entire thing just by flipping the matrix around
# No idea how to grade this one at the moment. I have it pegged to 8 (which gives you like,
# 2 per up/down/left/right?) But if you get one correct likely to get all correct so...
# Check the down one. Reverse/transpose if ordered wrongly will give you wrong result.

def cover_up(mat):
    """
        Shifts everything to the right
        ex.     [[0, 1, 0, 0], [1, 1, 0, 1], [0, 0, 0, 1], [1, 1, 1, 0]]
        becomes [[1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [1, 1, 1, 0]]
    """

    new = [[], [], [], []]
    done = False
    
    for i in range(4):
        for j in range(4):
            if mat[i][j][0] != 0:
                new[i].append([mat[i][j][0], mat[i][j][1]])
                if len(new[i]) != j + 1:
                    done = True

        while len(new[i]) < 4:
            new[i].append([0, 0])

    del mat
    return (new, done)


def merge(mat, turn):
    """
        turn : current player, gets points for merging opposite players tiles
        Returns (mat, done)
        mat  : Matrix after merging
        done : wether merge happened or not
    """
    done = False

    score = 0

    for i in range(4):
        for j in range(3):
            if mat[i][j][0] == mat[i][j+1][0] and mat[i][j][0] != 0:

                if mat[i][j][1] == mat[i][j + 1][1] and mat[i][j][1] != turn:
                    score += mat[i][j][0] * 2

                newPos = (mat[i][j][0] * 2, turn)
                mat[i][j] = newPos
                mat[i][j + 1] = (0, 0)
                done = True

    return (mat, done, score)

def up(game, turn):

        print("Player ", turn, "up")

        # transpose makes it same as left
        # then shift left, merge, shift left
        # transpose again to get original direction

        game = transpose(game)

        game, shiftStatus = cover_up(game)
        game, mergeStatus, score = merge(game, turn)
        done = shiftStatus or mergeStatus
        game = cover_up(game)[0]
        game = transpose(game)
        return (game, done, score)

def down(game, turn):

        print("Player ", turn, "down")

        # transpose then reverse makes it same as left
        # then shift left, merge, shift left
        # reverse and transpose again to get original direction

        game = reverse(transpose(game))

        game, shiftStatus = cover_up(game)
        game, mergeStatus, score = merge(game, turn)
        done = shiftStatus or mergeStatus
        game = cover_up(game)[0]
        game = transpose(reverse(game))
        return (game, done, score)

def left(game, turn):

        print("Player ", turn, "left")

        # shift left, merge, shift left

        game, shiftStatus = cover_up(game)
        game, mergeStatus, score = merge(game, turn)
        done = shiftStatus or mergeStatus
        game = cover_up(game)[0]
        return (game, done, score)

def right(game, turn):

        print("Player ", turn, "right")

        # reverse makes it same as left
        # then shift left, merge, shift left
        # reverse again to get original direction

        game = reverse(game)
        game, shiftStatus = cover_up(game)
        game, mergeStatus, score = merge(game, turn)
        done = shiftStatus or mergeStatus
        game = cover_up(game)[0]
        game = reverse(game)
        return (game, done, score)
