from copy import deepcopy
import math
import State
import Cell
import heapq
from MRV_Var import MRV_Var
from LCV_Var import LCV_Var
from Constraints import check_for_new_domain
from Board import Board
from Print import print_the_board
from AC3 import ACThree


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


def check_more_than_two_limit_heuristic(state: State):
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


def check_circles_limit_heuristic(state: State):
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


def new_domain(state: State):
    domains = [0 for i in state.board]
    for q in range(len(domains)):
        domains[q] = [0 for i in state.board]

    for i in range(0, state.size):
        for j in range(0, state.size):
            domains[i][j] = deepcopy(state.board[i][j].domain)

    for i in range(0, state.size):
        for j in range(0, state.size):
            if state.board[i][j].value == "_":
                flag, domain_new = check_for_new_domain(domains, (i,j), state)

                if flag:
                    domains = domain_new
                else:
                    return []
    return domains


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


def mrv(board: Board) -> tuple:
    # This is Minimum Remaining Value algorithm
    # Which is two factors
    # 1. Most-constrained-variable heuristic
    # which is giving us a list of most constrained variables
    # 2. Most-constraining-variable heuristic
    # which gives us the most constraining variable
    vars = get_unassigned_variables(board.state)
    most_constrained_vars = most_constrained_variables(vars)
    most_constraining_var = most_constraining_variable(board.state, most_constrained_vars)
    return (most_constraining_var.x, most_constraining_var.y)


def lcv(board: Board):
    # this is the least constraining value heuristic.
    # it should choose the value in the domain of the current cell to populate
    # which removes least values from other variables' domains
    # but the constraints are not binary, so it's not exactly as LCV.
    lcv_domain = []
    x, y = board.assigned_variable
    cell = board.state.board[x][y]
    if cell.value == "_":
        for domain in board.domains[x][y]:
            count = 0
            cell.value = domain
            count += check_circles_limit_heuristic(board.state)
            count += check_more_than_two_limit_heuristic(board.state)
            count += is_unique_limit_heuristic(board.state)
            lcv_var = LCV_Var(deepcopy(cell.value), count)
            cell.value = "_"
            heapq.heappush(lcv_domain, lcv_var)


    if len(board.domains[x][y]) == 0:
        return 'Failure'
    else:
        new_val_from_heap = heapq.heappop(lcv_domain).value
        board.domains[x][y].remove(new_val_from_heap)
        return new_val_from_heap



def set_var_and_value(board: Board, second_value_to_assign):
    if second_value_to_assign == True:
        pass
    else:
        board.assigned_variable = mrv(board)
        if not board.assigned_variable:
            return False

    board.assigned_value = lcv(board)
    if board.assigned_value != 'Failure':
        return True
    else:
        return False


def AC3():
    pass


def forward_checking(state: State, domains):
    # this function do a forward checking on the board with the new assignment.
    # it returns [] if the variable's domain is completely deleted after checking / returns new domain otherwise.
    flag = True
    dom = deepcopy(domains)
    for i in range(0, state.size):
        for j in range(0, state.size):
            if state.board[i][j].value == "_":
                flag, domain_new = check_for_new_domain(dom, (i,j), state)
                if flag:
                    dom = domain_new
                else:
                    break
        if not flag:
            break
    if flag:
        return True, dom
    else:
         return False, []


outer_board = None
def backTrack(b: Board, is_second_value):
    global outer_board
    if outer_board == None:
        outer_board = b
    else:
        if b.old == None:
            return

    if check_termination(b.state):
        print()
        print_the_board(b.state, outer_board.state)
        return
    else:
        not_empty = set_var_and_value(b, is_second_value)
        if not not_empty:
            backTrack(b.old, False)
        else:
            new_vars_domains = deepcopy(b.domains)
            x, y = b.assigned_variable
            new_vars_domains[x][y] = b.assigned_value
            new_state: State = deepcopy(b.state)
            new_state.board[x][y].value = b.assigned_value
            status, variables_domain = forward_checking(new_state, new_vars_domains)
            if status:
                child_board = Board(new_state, variables_domain)
                child_board.old = b
                # going with changed information
                backTrack(child_board, False)
            elif not status and len(b.domains[x][y]) == 0:
                # backtrack with old information..
                backTrack(b.old, False)
            else:
                # next value for the assigned variable
                backTrack(b.old, True)




# if while loop is done,
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
