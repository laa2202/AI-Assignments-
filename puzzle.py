from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource 


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        
        if self.blank_index < self.n:
                return None
        
        board = self.config[:]
        i = self.blank_index - self.n

        board[self.blank_index], board[i] = board[i], board[self.blank_index] 

        return PuzzleState(board, self.n, self, "Up", self.cost + 1)
      
    def move_down(self):
        
        if self.blank_index >= self.n * (self.n - 1):
                return None 
        board = self.config[:]
        
        i = self.blank_index + self.n

        board[self.blank_index], board[i] = board[i], board[self.blank_index]

        return PuzzleState(board, self.n, self, "Down", self.cost + 1)
      
    def move_left(self):
        
        if self.blank_index % self.n == 0:
                return None 
        board = self.config[:] 
        i = self.blank_index - 1 
        
        board[self.blank_index], board[i] = board[i], board[self.blank_index] 

        return PuzzleState(board, self.n, "Left", self.cost + 1)

    def move_right(self):
        
        if self.blank_index % self.n == self.n - 1: 
                return None 

        board = self.config[:] 
        i = self.blank_index + 1

        board[self.blank_index], board[i] = board[i], board[self.blank_index]

        return PuzzleState(board, self.n, self, "Right", self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(state, nodes_expanded, max_depth, running_time, max_ram_usage):

    path = []
 
    node = state

    while node.parent is not None:
 
        path.append(node.action)
 
        node = node.parent

    path.reverse()

    f = open("output.txt", "w")
    f.write("path_to_goal: " + str(path) + "\n")
    f.write("cost_of_path: " + str(state.cost) + "\n")
    f.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    f.write("search_depth: " + str(state.cost) + "\n")
    f.write("max_search_depth: " + str(max_depth) + "\n")
    f.write("running_time: %.8f\n" % running_time)
    f.write("max_ram_usage: %.8f\n" % max_ram_usage)
    f.close()


def bfs_search(initial_state):
    """BFS search"""
    
        frontier = Q.Queue()
        frontier.put(initial_state)

        frontier_states = {tuple(initital_state.config)}
        
        explored = set()

        nodes_expanded = 0 

        max_depth = 0 


        while not frontier.empty():
        
                current = frontier.get()
                frontier_states.remove(tuple(current.config))

                if test_goal(current):
                        return current, nodes_expanded, max_depth
                
                explored.add(tuple(current.config))
                nodes_expanded += 1

                for child in current.expand():
                        config = tuple(child.config)

                        if config not in explored and config not in frontier_states:
                                frontier.put(child)
                                frontier_states.add(config)


                                if child.cost > max_depth:
                                        max_depth = child.cost 

def dfs_search(initial_state):
    """DFS search"""
    
    frontier = [initial_state]
    frontier_states = {tuple(initial_state.config)}
    
    explored = set()

    nodes_expanded = 0
    
    max_depth = 0

    while frontier:

        current = frontier.pop()
        frontier_states.remove(tuple(current.config))

        if test_goal(current):
            return current, nodes_expanded, max_depth

        explored.add(tuple(current.config))
        nodes_expanded += 1

        children = current.expand()

        for child in reversed(children):
            config = tuple(child.config)

            if config not in explored and config not in frontier_states:
                frontier.append(child)
                frontier_states.add(config)

                if child.cost > max_depth:
                    max_depth = child.cost

def A_star_search(initial_state):
    """A * search"""
    
    frontier = Q.PriorityQueue()
    count = 0

    frontier.put((calculate_total_cost(initial_state), count, initial_state))

    frontier_states = {tuple(initial_state.config)}
      
    explored = set()

    nodes_expanded = 0
    

    max_depth = 0

    while not frontier.empty():

        cost, order, current = frontier.get()
        frontier_states.remove(tuple(current.config))

        if test_goal(current):
            return current, nodes_expanded, max_depth

        explored.add(tuple(current.config))
        nodes_expanded += 1

        for child in current.expand():
            config = tuple(child.config)

            if config not in explored and config not in frontier_states:
                count += 1

                frontier.put(
                    (calculate_total_cost(child), count, child)
                )

                frontier_states.add(config)

                if child.cost > max_depth:
                    max_depth = child.cost

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    
        total = state.cost 
        
        for i in range(len(state.config)):
                total += calculate_manhattan_dist(i, state.config[i], state.n)

        return total 


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
        
        if value == 0:
                return 0

        row = idx // n
        col = idx % n 


        goal_row = value // n 

        goal_col = value % n 


        return abs(row - goal_row) + abs(col - goal_col)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    
        return puzzle_state.config == list(range(puzzle_state.n * puzzle_state.n))

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
