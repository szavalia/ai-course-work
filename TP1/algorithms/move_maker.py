from models import *
from constants import *

# Given the previous board and position and the new position, it returns a node with the executed transition
def shift(node : Node, new_position):
    # Copy the board
    new_board = [row[:] for row in node.state.board]
    # Switch empty space with new tile
    new_board[new_position[0]][new_position[1]] = node.state.board[node.state.empty_coords[0]][node.state.empty_coords[1]]
    new_board[node.state.empty_coords[0]][node.state.empty_coords[1]] = node.state.board[new_position[0]][new_position[1]] 

    # Create the new node and update parent
    new_node = Node(State(new_board,new_position), node, node.depth + 1)   
    
    return new_node

def expand(node : Node):
    new_position = [0,0]

    if node.state.empty_coords[1] > 0: # The empty slot can be moved left   
        # Shift the cero
        new_position[0] = node.state.empty_coords[0]
        new_position[1] = node.state.empty_coords[1]-1

        node.next.append(shift(node, new_position[:]))

    
    if node.state.empty_coords[0] > 0: # The empty slot can be moved up

        new_position[0] = node.state.empty_coords[0]-1
        new_position[1] = node.state.empty_coords[1]
        
        node.next.append(shift(node, new_position[:]))

    if node.state.empty_coords[1] < WIDTH-1: # The empty slot can be moved right  
        new_position[0] = node.state.empty_coords[0]
        new_position[1] = node.state.empty_coords[1]+1

        node.next.append(shift(node, new_position[:]))

    if node.state.empty_coords[0] < HEIGHT-1: # The empty slot can be moved down
        new_position[0] = node.state.empty_coords[0]+1
        new_position[1] = node.state.empty_coords[1]

        node.next.append(shift(node, new_position[:]))



    
