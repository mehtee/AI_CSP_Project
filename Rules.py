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
        return (False, None)

    if condition_eq(row_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(row_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "b", "B")

    if condition_eq(col_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(col_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    return (True, domain_after_check)


def conditional_two_limit(first, sign1, sign2):
    return ((first == sign1) or (first == sign2))


def conditional_equivalent(sign, domain):
    if sign == "b" or sign == "B":
        return ("b" in domain) or ("B" in domain)
    elif sign == "w" or sign == "W":
        return ("w" in domain) or ("W" in domain)
    else:
        return None


def equivalent_forms(sign):
    if sign == "b" or sign == "B":
        return ("b", "B")
    elif sign == "w" or sign == "W":
        return ("w", "W")
    else:
        return None


def check_more_than_two_limit(arr: list, index, domain):
    new_domain = deepcopy(domain)
    if index >= 2 and (conditional_two_limit(arr[index - 1], "w", "W") or conditional_two_limit(arr[index - 1], "b", "B")) and conditional_equivalent(arr[index - 1], new_domain):
        equivalentForms = equivalent_forms(arr[index - 1])
        remove_from_domain(new_domain, equivalentForms[0], equivalentForms[1])


def new_domain_after_checking_more_than_two_limit(state: State, cell: Cell):
    x = cell.x
    y = cell.y

    domain = cell.domain

    row_arr = deepcopy(state.board[x][:])
    domain_after_check = check_more_than_two_limit(row_arr, y, domain)

    col_arr = get_col(state.board, y)
    domain_after_check = check_more_than_two_limit(col_arr, x, domain_after_check)

    return domain_after_check