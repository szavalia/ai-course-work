#Node represents the state in a given step
class Node:
    def __init__(self, state,prev,depth):
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
    

#State represents the layout of the board
class State:
    def __init__(self,board,empty_coords):
        self.board = board
        self.empty_coords = empty_coords #coordinates x and y of empty space in list
    
    def __eq__(self, other)->bool:
        return self.board == other.board
    
    def __str__(self):
        return "Board:" + str(self.board) + "Positions:" + str(self.empty_coords)

class Metrics:
    def __init__(self,solved,expanded,frontier,time,solution = None,depth=None):
        self.solved = solved
        self.expanded = expanded
        self.frontier = frontier
        self.time = time
        self.solution = solution
        self.depth = depth
            