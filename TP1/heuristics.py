from models import State
from constants import *

def total_squares(state:State):
    squares = WIDTH*HEIGHT

    for (row_index, row) in enumerate(state.board):
        for (col_index,square_val) in enumerate(row):
            if(((square_val-1) // HEIGHT) == row_index and ((square_val-1) % WIDTH) == col_index ): #comparison to identify if the element is placed in the correct position
                squares-=1
            elif(square_val == 0 and row_index == WIDTH-1 and col_index == HEIGHT-1): #position of empty square should be in the last square of the board by finishing the game
                squares-=1
    
    return squares/(WIDTH*HEIGHT) 


