import queue
import random
import time
from copy import deepcopy
import numpy as np

"""Creating a class state for various functions"""
class State:
    def __init__(self, stateInfo, f=0, h=0, g=0):
        self.grid_state = stateInfo
        self.fvalue = f
        self.gvalue = g
        self.hvalue = h

    """This function is used to get successors of the given grid"""
    def successors_of_grid(self):
        x = [1, -1, 0, 0]
        y = [0, -0, 1, -1]

        """Converting string format to integer format for grid"""
        grid_matrix = convert_to_grid(self.grid_state)
        for row in range(3):
            for column in range(3):
                if grid_matrix[row][column] == 0:
                    blank_row = row
                    blank_column = column
                    break

        successor_grid = []
        for (row_move, column_move) in zip(x, y):
            if 0 <= blank_row + row_move < 3 and 0 <= blank_column + column_move < 3:
                """keeping a copy of grid matrix for doing alteration on copied grid"""
                next_successor_state = deepcopy(grid_matrix)
                temp = next_successor_state[blank_row + row_move][blank_column + column_move]
                next_successor_state[blank_row + row_move][blank_column + column_move] = 0
                next_successor_state[blank_row][blank_column] = temp
                """Append next successor state to successor_grid"""
                successor_grid.append(convert_to_string(next_successor_state))

        return successor_grid


    def __eq__(self, other):
        return self.grid_state == other.grid_state


    """Comparision function"""
    def __lt__(self, other):
        if self.fvalue < other.fvalue:
            return True
        elif self.fvalue == other.fvalue:
            if self.gvalue == other.gvalue:
                return self.grid_state < other.grid_state
            elif self.gvalue < other.gvalue:
                return True
            else:
                return False
        else:
            return False


"""This function is used to convert the input state string into integer matrix"""
def convert_to_grid(string_format):
    matrix_format = [[0 for i in range(3)] for j in range(3)]
    grid_state = string_format
    for i in range(3):
        for j in range(3):
            matrix_format[i][j] = int(grid_state[i * 3 + j])
    return matrix_format


"""This funtion is used to convert integer matrix to string matrix"""
def convert_to_string(grid_format):
    string_format = ""
    for i in range(3):
        for j in range(3):
            string_format += str(grid_format[i][j])
    return string_format


def inversion_check(start_state):
    """
    This function is used to check whether the start state of grid is even inversion or odd inversion.
    For odd inversion it cannot be solved because on every slide we add two inversion or remove two inversions,
    So only even inversions are accepted as input

    """
    try:
        length_of_start_state = len(start_state)
        count_of_inversions = 0  # Initializing count as zero
        for start in range(0, length_of_start_state):
            for next in range(start + 1, length_of_start_state):
                # Blank 'B' is not considered for inversion check
                if (int(start_state[start]) != 'B' and int(start_state[next]) != 'B' and int(start_state[start]) > int(start_state[next])):
                    count_of_inversions = count_of_inversions + 1

        """Checking for even or odd inversion"""
        if count_of_inversions % 2 != 0:
            print("Input value failed in inversion check, please enter valid input")
            return False
        return True
    except KeyError:
        return KeyError
    except ValueError:
        return ValueError

"""displaced_tiles_heuristic evaluate the tiles that are being displaced with given goal state and current state"""
def displaced_tiles_heuristic(goal_state, state):

    """Converting the state from string format to integer format"""
    current_grid_state = convert_to_grid(state)

    """Converting the state from string format to integer format"""
    goal_grid_state = convert_to_grid(goal_state.grid_state)

    heuristic = 0
    for row in range(3):
        for column in range(3):
            if current_grid_state[row][column] != goal_grid_state[row][column]:
                heuristic += 1
            if (
                current_grid_state[row][column] == 0
                and current_grid_state[row][column] != goal_grid_state[row][column]
                and is_tile_include is False
            ):
                heuristic -= 1
    return heuristic


"""Fucntion to evaluate manhattan heuristics"""
def manhattan_heuristic(goal_state, state):

    """Converting the state from string format to integer format"""
    current_grid_state = convert_to_grid(state)
    """Converting the state from string format to integer format"""
    goal_grid_state = convert_to_grid(goal_state.grid_state)

    current_coordinate = np.arange(18).reshape((9, 2))
    for row in range(3):
        for column in range(3):
            current_coordinate[current_grid_state[row][column]][0] = row
            current_coordinate[current_grid_state[row][column]][1] = column

    heuristic = 0
    for row in range(3):
        for column in range(3):
            if goal_grid_state[row][column] != 0:
                heuristic += abs(row - current_coordinate[goal_grid_state[row][column]][0]) + abs(
                    column - current_coordinate[goal_grid_state[row][column]][1]
                )
            if goal_grid_state[row][column] == 0 and is_tile_include:
                heuristic += abs(row - current_coordinate[goal_grid_state[row][column]][0]) + abs(
                    column - current_coordinate[goal_grid_state[row][column]][1]
                )
    return heuristic


"""This function uses manhattan heuristic to find over estimated heuristic for given goal state and current state"""
def over_estimated_heuristic(goal_state, state):
    return random.randint(manhattan_heuristic(goal_state, state) ** 2, 181440)


"""This fuction is used to print grids in proper format"""
def print_grid_state(initial_state, final_state):
    print("Starting state: ")

    """Converting a initial state string input for matrix to integer matrix"""
    start_state = convert_to_grid(initial_state.grid_state)

    for row in range(3):
        for column in range(3):
            if start_state[row][column] == 0:
                print("B", end=" ")
            else:
                print("T" + str(start_state[row][column]), end=" ")
        print()
    print("Goal state: ")


    """Converting the state from string format to integer format"""    
    goal_state = convert_to_grid(final_state.grid_state)
    for row in range(3):
        for column in range(3):
            if goal_state[row][column] == 0:
                print("B", end=" ")
            else:
                print("T" + str(goal_state[row][column]), end=" ")
        print()


"""This function is used to print optimal path of matrix grid"""
def print_optimal_path(state, depth, grid_state_parent):
    if state is None:
        return depth
    else:
        """Call the function recursively if the state is not None"""
        totalState = print_optimal_path(
            grid_state_parent[state], depth + 1, grid_state_parent)
        """Converting the state from string format to integer format"""
        eight_grid_conf = convert_to_grid(state)
        for i in range(3):
            for j in range(3):
                if eight_grid_conf[i][j] == 0:
                    print("B", end=" ")
                else:
                    print("T" + str(eight_grid_conf[i][j]), end=" ")
            print()
        print("----------")
        return totalState


def print_stats(initial_state, final_state, grid_state_parent, explored_states, heuristic_choice):
    heuristic_dict = {
        1: "Zero Heuristics:-",
        2: "Tiles Displaced Heuristic:-",
        3: "Manhattan Heuristic:-",
        4: "Over Estimated Heuristic:-",
    }
    print(heuristic_dict[heuristic_choice])
    print("Valid path from start state to goal state exists: ")
    print_grid_state(final_state, initial_state)

    print("Total number of states explored")
    print(explored_states)

    print("Optimal Path for finding the goal state")
    states_on_optimal_path = print_optimal_path(
        final_state.grid_state, 0, grid_state_parent)

    print("Total number of states on optimal path.")
    print(states_on_optimal_path)

    print("Optimal Cost of the path.")
    print(states_on_optimal_path - 1)


"""This function is used when there is failure in finding goal state form current state"""
def print_failure(initial_grid_configuration, final_puzzle_configuration, explored_states):
    print("Unable to find path between start grid and goal grid")
    print_grid_state(initial_grid_configuration,
                           final_puzzle_configuration)
    print("Total number of states explored : ")
    print(explored_states)


"""This function is used to search for the goal state from the given start state"""
def puzzle_solving(initial_state, goal_state, heuristic_choice):
    priority_queue = queue.PriorityQueue()  

    if heuristic_choice == 1:
        heuristic_value = 0
    elif heuristic_choice==2:
        heuristic_value = displaced_tiles_heuristic(
            goal_state, initial_state.grid_state)
    elif heuristic_choice==3:
        heuristic_value = manhattan_heuristic(
            goal_state, initial_state.grid_state)
    elif heuristic_choice==4:
        heuristic_value = over_estimated_heuristic(
            goal_state, initial_state.grid_state)

    priority_queue.put(initial_state, 0, heuristic_value)

    """It is used to store parent grid state(node)"""
    grid_state_parent = {} 

    """Stores value of grid"""
    grid_state_g = {}  

    """Closed_list is used to keep track of nodes that are being traversed"""
    closed_list = {} 

    explored_states = 0
    grid_state_g[initial_state.grid_state] = 0
    grid_state_parent[initial_state.grid_state] = None
    closed_list_dict[initial_state.grid_state] = 1 #It saves that the initial node is traversed
    current_node = None

    while not priority_queue.empty():
        current_node = priority_queue.get()
        if current_node.grid_state in closed_list:
            continue
        if current_node == goal_state:
            return closed_list, print_stats(
                initial_state, goal_state, grid_state_parent, explored_states, heuristic_choice
            )
        """Get all successors of the current grid"""
        successor_grid = current_node.successors_of_grid()
        for successor_rep in successor_grid:
            if heuristic_choice == 1:
                h = 0
            elif heuristic_choice == 2:
                h = displaced_tiles_heuristic(
                    goal_state, successor_rep)
            elif heuristic_choice == 3:
                h = manhattan_heuristic(
                    goal_state, successor_rep)
            elif heuristic_choice == 4:
                h = over_estimated_heuristic(
                    goal_state, successor_rep)

            # It will print the unexplored part 
            # print("State : h(State) , ChildState : h(ChildState) ")
            # print(current_node.grid_state + ": " + str(current_node.hvalue), successor_rep + " " + str(h))
            
            closed_list_dict[successor_rep] = 1  # marking explored state as 1
            
            """Increasing g value by 1"""
            successor_state_gvalue = grid_state_g[current_node.grid_state] + 1

            if successor_rep in closed_list:
                if successor_state_gvalue <= grid_state_g[successor_rep]:
                    grid_state_g[successor_rep] = successor_state_gvalue
                    grid_state_parent[successor_rep] = current_node.grid_state
                    priority_queue.put(
                        State(successor_rep, successor_state_gvalue + h, h, successor_state_gvalue))
            elif successor_rep in grid_state_g:
                if successor_state_gvalue < grid_state_g[successor_rep]:
                    grid_state_g[successor_rep] = successor_state_gvalue
                    grid_state_parent[successor_rep] = current_node.grid_state
                    priority_queue.put(
                        State(successor_rep, successor_state_gvalue + h, h, successor_state_gvalue))
            else:
                grid_state_g[successor_rep] = successor_state_gvalue
                grid_state_parent[successor_rep] = current_node.grid_state
                priority_queue.put(
                    State(successor_rep, successor_state_gvalue + h, h, successor_state_gvalue))
        if current_node.grid_state not in closed_list:
            closed_list[current_node.grid_state] = 1
            explored_states += 1

    if current_node != goal_state:
        print_failure(initial_state, goal_state, explored_states)



"""Our program starts from here i.e the main() function"""
if __name__ == "__main__":
    initial_state = ""
    goal_state = ""
    is_tile_include = True
    closed_list_dict = {}  # closed list.
    
    """Take start state of grid and goal state of grid as input"""
    print("Enter Starting state of grid")
    for i in range(3): #Taking input for 3X3 matrix
        single_row = list(map(str, input().split()))
        initial_state = initial_state+"".join(single_row)
    print("Enter Goal state of grid")
    for i in range(3):  # Taking input for 3X3 matrix
        single_row = list(map(str, input().split()))
        goal_state = goal_state+"".join(single_row)

    """Replacing the T and B characters from the input value"""
    start_state = initial_state.replace("T","").replace("B","0")
    goal_state = goal_state.replace("T", "").replace("B", "0")

    """checking whether the given input is solvable or not"""
    if inversion_check(start_state):
        goal_state = State(goal_state, 0)
        exit_state = 1
        while(exit_state):
            # Options for different heuristics approaches
            print("Enter choice depending on Heuristics: ")
            print("1. h1(n) = 0")
            print("2. h2(n) = number of tiles displaced from their destined position")
            print("3. h3(n) = sum of Manhattan distance of each tiles from the goal position")
            print("4. h4(n) = devise aheuristics such that h(n) > h∗(n)")
            print("5. Exit")
            heuristic_choice = int(input("Please Enter Your Choice between 1 to 5: "))
            if heuristic_choice==5:
                exit_state=0
                continue
            start_timer = time.time()
            invalid_choice = False
            if heuristic_choice==1:
                h_initial = 0
            elif heuristic_choice==2:
                h_initial = displaced_tiles_heuristic(goal_state,start_state)
            elif heuristic_choice==3:
                h_initial = manhattan_heuristic(goal_state, start_state)    
            elif heuristic_choice==4:
                h_initial = over_estimated_heuristic(goal_state, start_state)
            else:
                print("Invalid Choice , Please rerun program")
                invalid_choice = True
            if invalid_choice is not True:   
                initial_state = State(start_state, h_initial, h_initial)
                puzzle_solving(initial_state, goal_state, heuristic_choice)
                print("Time taken by the program in seconds: ")
                execution_time = time.time() - start_timer  # stopping timer
                print("Total time taken: ", execution_time)


