from copy import deepcopy
import math
import State
import Cell
import Binairo
from Constraints import *
from collections import deque
from Board import Board


def domain_after_check_more_than_two_limit(arr, index, domain):
    new_domain = deepcopy(domain)
    flag = False
    if index >= 2 and arr[index - 1] == arr[index - 2] and (arr[index - 1] == "W") and "B" in new_domain:
        if new_domain.count("W"):
            new_domain.remove("W")

    if index >= 2 and arr[index - 1] == arr[index - 2] and (arr[index - 1] == "W") and "B" not in new_domain:
        return "Failure"

    if index >= 2 and arr[index - 1] == arr[index - 2] and (arr[index - 1] == "B") and "W" in new_domain:
        if new_domain.count("B"):
            new_domain.remove("B")

    if index >= 2 and arr[index - 1] == arr[index - 2] and (arr[index - 1] == "B") and "W" not in new_domain:
        return "Failure"

    if len(arr) - 2 >= index >= 1 and arr[index - 1] == arr[index + 1] and (arr[index - 1] == "W") and "B" in new_domain:
        if new_domain.count("W"):
            new_domain.remove("W")

    if len(arr) - 2 >= index >= 1 and arr[index - 1] == arr[index + 1] and (arr[index - 1] == "W") and "B" not in new_domain:
        return "Failure"

    if index <= len(arr) - 3 and arr[index + 1] == arr[index + 2] and (
            arr[index + 1] == "W") and "B" in new_domain:
        if new_domain.count("W"):
            new_domain.remove("W")

    if index <= len(arr) - 3 and arr[index + 1] == arr[index + 2] and (
            arr[index + 1] == "W") and "B" not in new_domain:
        return "Failure"

    return new_domain


def Revise(cell: Cell, board: Board):
    # rule 1: number of blacks and whites has to be the same in a row or a column
    x, y = cell.x, cell.y

    row = board.domains[x][:]
    column = col_of_arr_with_index(board.domains, y)
    domain_of_x_y = board.domains[x][y]

    if row.count("W") > len(row) / 2 or row.count("B") > len(row) / 2 or column.count("W") > len(
            column) / 2 or column.count("B") > len(column) / 2:
        return "Failure"

    # check for row

    flag = False
    if row.count("W") == len(row) / 2 and "B" in domain_of_x_y:
        # there's a value in domain of xy that satisfies
        pass
    elif row.count("W") == len(row) / 2 and "W" in domain_of_x_y:
        domain_of_x_y.remove("W")

        # update arrays cuz the domain has changed
        row = board.domains[x][:]
        column = col_of_arr_with_index(board.domains, y)
        domain_of_x_y = board.domains[x][y]

        if len(domain_of_x_y) == 0:
            return "Failure"

    if len(board.domains[x][y]) == 0:
        return "Failure"

    if row.count("B") == len(row) / 2 and "W" in domain_of_x_y:
        # there's a value in domain of xy that satisfies
        pass
    elif row.count("B") == len(row) / 2 and "B" in domain_of_x_y:
        domain_of_x_y.remove("B")

        # update arrays cuz the domain has changed
        row = board.domains[x][:]
        column = col_of_arr_with_index(board.domains, y)
        domain_of_x_y = board.domains[x][y]

        if len(domain_of_x_y) == 0:
            return "Failure"

    if len(board.domains[x][y]) == 0:
        return "Failure"

    # check for column

    if column.count("B") == len(column) / 2 and "W" in domain_of_x_y:
        # there's a value in domain of xy that satisfies
        pass
    elif column.count("B") == len(column) / 2 and "B" in domain_of_x_y:
        domain_of_x_y.remove("B")

        # update arrays cuz the domain has changed
        row = board.domains[x][:]
        column = col_of_arr_with_index(board.domains, y)
        domain_of_x_y = board.domains[x][y]

        if len(domain_of_x_y) == 0:
            return "Failure"

    if len(board.domains[x][y]) == 0:
        return "Failure"
    # Rule 1 done

    # Rule 2: more than 2 same circles has not to be in the same row/col

    # check for row
    new_dom = domain_after_check_more_than_two_limit(row, y, domain_of_x_y)
    if new_dom != "Failure" and new_dom != domain_of_x_y:
        flag = True
        board.domains[x][y] = new_dom
        # update arrays cuz the domain has changed
        row = board.domains[x][:]
        column = col_of_arr_with_index(board.domains, y)
        domain_of_x_y = board.domains[x][y]
    elif new_dom == "Failure":
        return "Failure"

    if len(board.domains[x][y]) == 0:
        return "Failure"

    # check for column
    new_dom = domain_after_check_more_than_two_limit(column, x, domain_of_x_y)
    if new_dom != "Failure" and new_dom != domain_of_x_y:
        flag = True
        board.domains[x][y] = new_dom
        # update arrays cuz the domain has changed
        row = board.domains[x][:]
        column = col_of_arr_with_index(board.domains, y)
        domain_of_x_y = board.domains[x][y]
    elif new_dom == "Failure":
        return "Failure"
    else:
        flag = False

    if len(board.domains[x][y]) == 0:
        return "Failure"

    # Rule 3:
    domain_list_xy = deepcopy(board.domains[x][y])
    for domain in domain_list_xy:
        old_value = deepcopy(board.state.board[x][y])
        board.state.board[x][y].value = domain
        if not Binairo.is_unique(board.state):
            board.state.board[x][y] = old_value
            board.domains[x][y].remove(domain)
            flag = True
    if len(board.domains[x][y]) == 0:
        return "Failure"

    return flag


def ACThree(board: Board):
    Queue = deque()
    unassigned_vars = Binairo.get_unassigned_variables(board.state)
    Queue.extend(unassigned_vars)
    while Queue:
        popped_queue_cell = unassigned_vars.pop()
        revised = Revise(popped_queue_cell, board)
        if revised == "Failure":
            return False
    return True