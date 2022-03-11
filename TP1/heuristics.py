from models import State
from constants import *

number_goal_positions = {}      # not hardcoded in case we want to extend for nxm boards
n = 1
for i in range(0, HEIGHT):
    for j in range(0, WIDTH):
        number_goal_positions[n] = (i, j)
        n += 1
del(number_goal_positions[HEIGHT*WIDTH])

def total_squares(state:State):
    squares = WIDTH*HEIGHT - 1  # -1 because the blank space is not counted

    for (row_index, row) in enumerate(state.board):
        for (col_index,square_val) in enumerate(row):
            if(((square_val-1) // HEIGHT) == row_index and ((square_val-1) % WIDTH) == col_index ): #comparison to identify if the element is placed in the correct position
                squares-=1

    return squares


def total_manhattan(state:State):
    manhattan_distance = 0
    for (row_index, row) in enumerate(state.board):
        for (col_index,square_val) in enumerate(row):
            if (square_val != 0):
                (row_goal, col_goal) = number_goal_positions[square_val]
                manhattan_distance += abs(row_index - row_goal) + abs(col_index - col_goal)
    
    return manhattan_distance
