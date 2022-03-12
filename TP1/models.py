
class Board:
    def __init__(self,layout,dim,empty_coords):
        self.layout=layout
        self.dim=dim
        self.empty_coords = empty_coords #coordinates x and y of empty space in list
    
    def __eq__(self,other) -> bool:
        return self.layout == other.layout
    
    def __str__(self):
        board_str = ""
        for (row_index,row) in enumerate(self.layout):
            board_str = board_str + ' '.join(str(val) for val in row) + (' ' if row_index != self.dim else '')
        return board_str
    
#State represents the layout of the board
class State:
    def __init__(self,board:Board,heuristic=0):
        self.board = board
        self.heuristic = heuristic
    
    def __eq__(self, other)->bool:
        return self.board == other.board
    
    def __str__(self):
       return "Board:" + str(self.board) + " Heuristic: " + str(self.heuristic)

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
            