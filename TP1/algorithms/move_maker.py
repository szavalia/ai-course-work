from models import *

# Given the previous board and position and the new position, it returns a node with the executed transition
def shift(node : Node, new_position, heuristic_function):
    empty_coord_x = node.state.board.empty_coords[0]
    empty_coord_y = node.state.board.empty_coords[1]
    # Copy the board
    new_board = [row[:] for row in node.state.board.layout]
    # Switch empty space with new tile
    new_board[new_position[0]][new_position[1]] = node.state.board.layout[empty_coord_x][empty_coord_y]
    new_board[empty_coord_x][empty_coord_y] = node.state.board.layout[new_position[0]][new_position[1]] 

    # Create the new node and update parent
    new_heuristic = 0
    full_board = Board(new_board,new_position)
    new_state = State(full_board,new_heuristic)
    if heuristic_function != None:
        new_heuristic = heuristic_function(new_state)
        new_state = State(full_board,new_heuristic)
    new_node = Node(new_state, node, node.depth + 1)   
    
    return new_node

def expand(node : Node, heuristic_function):
    new_position = [0,0]
    empty_coord_x = node.state.board.empty_coords[0]
    empty_coord_y = node.state.board.empty_coords[1]

    if empty_coord_y > 0: # The empty slot can be moved left   
        # Shift the cero
        new_position[0] = empty_coord_x
        new_position[1] = empty_coord_y - 1
        node.next.append(shift(node, new_position[:], heuristic_function))
    
    if empty_coord_x > 0: # The empty slot can be moved up

        new_position[0] = empty_coord_x - 1
        new_position[1] = empty_coord_y
        node.next.append(shift(node, new_position[:], heuristic_function))

    if empty_coord_y < Board.dim-1: # The empty slot can be moved right  
        new_position[0] = empty_coord_x
        new_position[1] = empty_coord_y + 1
        node.next.append(shift(node, new_position[:], heuristic_function))

    if empty_coord_x < Board.dim-1: # The empty slot can be moved down
        new_position[0] = empty_coord_x + 1
        new_position[1] = empty_coord_y
        node.next.append(shift(node, new_position[:], heuristic_function))

def get_solution(node:Node):
    solution = []
    aux_node = node
    while aux_node.prev != None:
        solution.insert(0,aux_node.state.board.layout)
        aux_node = aux_node.prev
    solution.insert(0,aux_node.state.board.layout)
    return solution

    
