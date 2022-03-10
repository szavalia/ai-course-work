#Node represents the state in a given step
class Node:
    def __init__(self, state,prev,next,depth):
        self.state = state
        self.prev = prev 
        self.next = next #array of nodes representing children
        self.depth = depth #depth in tree

#State represents the layout of the board
class State:
    def __init__(self,board):
        self.board = board  

