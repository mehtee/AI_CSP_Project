from copy import deepcopy
import math
import State
import Cell
import heapq
from MRV_Var import MRV_Var
from LCV_Var import LCV_Var

def check_more_than_two_limit(state: State):
    # check rows
    for i in range(0, state.size):
        for j in range(0, state.size - 2):
            if (state.board[i][j].value.upper() == state.board[i][j + 1].value.upper() and
                    state.board[i][j + 1].value.upper() == state.board[i][j + 2].value.upper() and
                    state.board[i][j].value != '_' and
                    state.board[i][j + 1].value != '_' and
                    state.board[i][j + 2].value != '_'):
                return False
    # check cols
    for j in range(0, state.size):  # cols
        for i in range(0, state.size - 2):  # rows
            if (state.board[i][j].value.upper() == state.board[i + 1][j].value.upper()
                    and state.board[i + 1][j].value.upper() == state.board[i + 2][j].value.upper()
                    and state.board[i][j].value != '_'
                    and state.board[i + 1][j].value != '_'
                    and state.board[i + 2][j].value != '_'):
                return False

    return True


def check_circles_limit(state: State):  # returns false if number of white or black circles exceeds board_size/2
    # check in rows
    for i in range(0, state.size):  # rows
        no_white_row = 0
        no_black_row = 0
        for j in range(0, state.size):  # each col
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_': no_white_row += 1
            if state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_': no_black_row += 1
        if no_white_row > state.size / 2 or no_black_row > state.size / 2:
            return False
        no_black_row = 0
        no_white_row = 0

    # check in cols
    for j in range(0, state.size):  # cols
        no_white_col = 0
        no_black_col = 0
        for i in range(0, state.size):  # each row
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_': no_white_col += 1
            if state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_': no_black_col += 1
        if no_white_col > state.size / 2 or no_black_col > state.size / 2:
            return False
        no_black_col = 0
        no_white_col = 0

    return True


def is_unique(state: State):  # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0, state.size - 1):
        for j in range(i + 1, state.size):
            count = 0
            for k in range(0, state.size):
                if (state.board[i][k].value.upper() == state.board[j][k].value.upper()
                        and state.board[i][k].value != '_'
                        and state.board[j][k].value != '_'):
                    count += 1
            if count == state.size:
                return False
            count = 0

    # check cols
    for j in range(0, state.size - 1):
        for k in range(j + 1, state.size):
            count_col = 0
            for i in range(0, state.size):
                if (state.board[i][j].value.upper() == state.board[i][k].value.upper()
                        and state.board[i][j].value != '_'
                        and state.board[i][k].value != '_'):
                    count_col += 1
            if count_col == state.size:
                return False
            count_col = 0

    return True




def check_circles_limit_heuristic(state: State):
    # to check how many constraints are going to make in a row or col for the constraint of number of whites/blacks

    count = 0
    # check rows
    for i in range(0, state.size):
        for j in range(0, state.size - 2):
            if (state.board[i][j].value.upper() == state.board[i][j + 1].value.upper() and
                    state.board[i][j + 1].value.upper() == state.board[i][j + 2].value.upper() and
                    state.board[i][j].value != '_' and
                    state.board[i][j + 1].value != '_' and
                    state.board[i][j + 2].value != '_'):
                count += 1
    # check cols
    for j in range(0, state.size):  # cols
        for i in range(0, state.size - 2):  # rows
            if (state.board[i][j].value.upper() == state.board[i + 1][j].value.upper()
                    and state.board[i + 1][j].value.upper() == state.board[i + 2][j].value.upper()
                    and state.board[i][j].value != '_'
                    and state.board[i + 1][j].value != '_'
                    and state.board[i + 2][j].value != '_'):
                count += 1

    return count


def check_more_than_two_limit_heuristic(state: State):
    # to check how many constraints are going to make in a row or col for the constraint of more than 2 same circles
    count = 0
    # check in rows
    for i in range(0, state.size):  # rows
        no_white_row = 0
        no_black_row = 0
        for j in range(0, state.size):  # each col
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_': no_white_row += 1
            if state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_': no_black_row += 1
        if no_white_row > state.size / 2 or no_black_row > state.size / 2:
            count += 1
        no_black_row = 0
        no_white_row = 0

    # check in cols
    for j in range(0, state.size):  # cols
        no_white_col = 0
        no_black_col = 0
        for i in range(0, state.size):  # each row
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_': no_white_col += 1
            if state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_': no_black_col += 1
        if no_white_col > state.size / 2 or no_black_col > state.size / 2:
            count += 1
        no_black_col = 0
        no_white_col = 0

    return count


def is_unique_limit_heuristic(state: State):
    # to check how many constraints are going to make for the constraint of uniqueness of cols/rows
    const_count = 0
    # check rows
    for i in range(0, state.size - 1):
        for j in range(i + 1, state.size):
            count = 0
            for k in range(0, state.size):
                if (state.board[i][k].value.upper() == state.board[j][k].value.upper()
                        and state.board[i][k].value != '_'
                        and state.board[j][k].value != '_'):
                    count += 1
            if count == state.size:
                const_count += 1
            count = 0

    # check cols
    for j in range(0, state.size - 1):
        for k in range(j + 1, state.size):
            count_col = 0
            for i in range(0, state.size):
                if (state.board[i][j].value.upper() == state.board[i][k].value.upper()
                        and state.board[i][j].value != '_'
                        and state.board[i][k].value != '_'):
                    count_col += 1
            if count_col == state.size:
                const_count += 1
            count_col = 0

    return const_count


def get_all_variables(state: State) -> list:
    # this function gives us the variables that is not assigned or assigned
    board = state.board
    vars = []
    for i in range(0, state.size):
        for j in range(0, state.size):
            vars.append(board[i][j])

    return vars


def get_unassigned_variables(state: State) -> list:
    # this function gives us the variables that is not assigned any value (_)
    board = state.board
    vars = []
    for i in range(0, state.size):
        for j in range(0, state.size):
            if board[i][j].value == "_":
                vars.append(board[i][j])

    return vars


def most_constrained_variables(variables: list) -> list:
    # returns a list of most constrained variables
    min_domain_size = math.inf # set to infinity to use in the comparison
    most_constrained_vars = []
    for cell in variables:
        if len(cell.domain) < min_domain_size:
            min_domain_size = len(cell.domain)

    for cell in variables:
        if len(cell.domain) == min_domain_size:
            most_constrained_vars.append(cell)

    return most_constrained_vars


def most_constraining_variable(state:State, most_constrained_variables) -> Cell:
    # returns the most constraining variable
    most_constraining_variables = []
    for cell in most_constrained_variables:
        if cell.value == "_":
            count = 0
            # check for black
            cell.value = "b"
            count += check_circles_limit_heuristic(state)
            count += check_more_than_two_limit_heuristic(state)
            count += is_unique_limit_heuristic(state)
            # check for white
            cell.value = "w"
            count += check_circles_limit_heuristic(state)
            count += check_more_than_two_limit_heuristic(state)
            count += is_unique_limit_heuristic(state)
            # backup its value which was nothing
            cell.value = "_"
            # make an object of MRV_Var to use it for comparison in heapq
            mrv_var = MRV_Var(cell, count)
            heapq.heappush(most_constraining_variables, mrv_var)

    return heapq.heappop(most_constraining_variables).cell


def mrv(state: State) -> Cell:
    # This is Minimum Remaining Value algorithm
    # Which is two factors
    # 1. Most-constrained-variable heuristic
    # which is giving us a list of most constrained variables
    # 2. Most-constraining-variable heuristic
    # which gives us the most constraining variable
    vars = get_unassigned_variables(state)
    most_constrained_vars = most_constrained_variables(vars)
    most_constraining_var = most_constraining_variable(state, most_constrained_vars)
    return most_constraining_var


def lcv(cell: Cell, state: State):
    # this is the least constraining value heuristic.
    # it should choose the value in the domain of the current cell to populate
    # which removes least values from other variables' domains
    # but the constraints are not binary, so it's not exactly as LCV.
    lcv_domain = []
    if cell.value == "_":
        for domain in cell.domain:
            count = 0
            cell.value = domain
            count += check_circles_limit_heuristic(state)
            count += check_more_than_two_limit_heuristic(state)
            count += is_unique_limit_heuristic(state)
            cell.value = "_"
            lcv_var = LCV_Var(cell, count)
            heapq.heappush(lcv_domain, lcv_var)
        return lcv_domain


def AC3():
    pass


def forward_checking():
    # this function do a forward checking on the board with the new assignment.
    # it returns false if the variable's domain is completely deleted after checking / returns true if not.
    pass


def backTrack(state: State):
    if is_assignment_complete(state):
        return state
    else:
        X = mrv(state)
        D = lcv(X, state)
        while D:
            val = heapq.heappop(D)
            X.value = val

            pass


def is_assignment_complete(state: State):  # check if all variables are assigned or not
    for i in range(0, state.size):
        for j in range(0, state.size):
            if state.board[i][j].value == '_':  # exists a variable which is not assigned (empty '_')

                return False

    return True


def is_consistent(state: State):
    return check_more_than_two_limit(state) and check_circles_limit(state) and is_unique(state)


def check_termination(state: State):
    return is_consistent(state) and is_assignment_complete(state)
	