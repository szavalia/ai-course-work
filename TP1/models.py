from constants import *

#State represents the layout of the board
class State:
    def __init__(self,board,empty_coords,heuristic=0):
        self.board = board
        self.empty_coords = empty_coords #coordinates x and y of empty space in list
        self.heuristic = heuristic
    
    def __eq__(self, other)->bool:
        return self.board == other.board

    def board_str(self):
        state_str = ""
        for (row_index,row) in enumerate(self.board):
            state_str = state_str + ' '.join(str(val) for val in row) + (' ' if row_index != HEIGHT else '')
        return state_str
    
    def __str__(self):
       return "Board:" + str(self.board) + "Positions:" + str(self.empty_coords)

#Node represents the state in a given step
class Node:
    def __init__(self, state:State,prev,depth):
        self.state = state
        self.prev = prev 
        self.next = [] #array of nodes representing children
        self.depth = depth #depth in tree

    def __eq__(self, other) -> bool:
        if (other == None):
            return False
        return self.state == other.state
    
    def __str__(self) -> str:
        return "State:" + str(self.state) + "Depth:" + str(self.depth)

class Metrics:
    def __init__(self,solved:bool,expanded,frontier,time,solution = None,depth=None):
        self.solved = solved
        self.expanded = expanded
        self.frontier = frontier
        self.time = time
        self.solution = solution
        self.depth = depth
            