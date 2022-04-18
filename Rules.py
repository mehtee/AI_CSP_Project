import State, Cell
from copy import deepcopy


def get_col(arr, column_index):
    col = []
    for row in arr:
        col.append(row[column_index])
    return col


def condition_gt(arr, first, second):
    return (arr.count(first) + arr.count(second)) > len(arr) / 2


def condition_eq(arr, first, second):
    return (arr.count(first) + arr.count(second)) == len(arr) / 2


def remove_from_domain(arr, first, second):
    if arr.count(first) > 0:
        arr.remove(first)
    elif arr.count(second) > 0:
        arr.remove(second)
    else:
        pass


def new_domain_after_checking_circles_limit(state: State, cell: Cell):
    x = cell.x
    y = cell.y

    row_arr = deepcopy(state.board[x][:])
    col_arr = get_col(state.board, y)

    domain_after_check = deepcopy(cell.domain)
    if condition_gt(row_arr, "w", "W") or condition_gt(row_arr, "b", "B") or condition_gt(col_arr, "w", "W") or condition_gt(col_arr, "b", "B"):
        return False, None

    if condition_eq(row_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(row_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "b", "B")

    if condition_eq(col_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(col_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    return True, domain_after_check


