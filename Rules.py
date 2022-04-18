import State, Cell
from copy import deepcopy
from Binairo import is_unique

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
        return []

    if condition_eq(row_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(row_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "b", "B")

    if condition_eq(col_arr, "w", "W") and ("w" in domain_after_check or "W" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    if condition_eq(col_arr, "b", "B") and ("b" in domain_after_check or "B" in domain_after_check):
        remove_from_domain(domain_after_check, "w", "W")

    return domain_after_check


def conditional_two_limit(first, sign1):
    return (first.upper() == sign1.upper())


def comp_value(firstCell, secondCell):
    return firstCell.value.upper() == secondCell.value.upper()


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
    if (index >= 2) and (comp_value(arr[index - 1], arr[index - 2])) and (conditional_two_limit(arr[index - 1], "w") or conditional_two_limit(arr[index - 1], "b")) and conditional_equivalent(arr[index - 1], new_domain):
        equivalentForms = equivalent_forms(arr[index - 1])
        remove_from_domain(new_domain, equivalentForms[0], equivalentForms[1])

    if (len(arr) - 2 >= index >= 1) and (comp_value(arr[index - 1], arr[index + 1])) and (conditional_two_limit(arr[index - 1], "w") or conditional_two_limit(arr[index - 1], "b")) and conditional_equivalent(arr[index - 1], new_domain):
        equivalentForms = equivalent_forms(arr[index - 1])
        remove_from_domain(new_domain, equivalentForms[0], equivalentForms[1])

    if (index <= len(arr) - 3) and (comp_value(arr[index + 1], arr[index + 2])) and (conditional_two_limit(arr[index + 1], "w") or conditional_two_limit(arr[index + 1], "b")) and conditional_equivalent(arr[index + 1], new_domain):
        equivalentForms = equivalent_forms(arr[index + 1])
        remove_from_domain(new_domain, equivalentForms[0], equivalentForms[1])

    return new_domain


def new_domain_after_checking_more_than_two_limit(state: State, cell: Cell):
    x = cell.x
    y = cell.y

    domain = cell.domain

    row_arr = deepcopy(state.board[x][:])
    domain_after_check = check_more_than_two_limit(row_arr, y, domain)

    col_arr = get_col(state.board, y)
    domain_after_check = check_more_than_two_limit(col_arr, x, domain_after_check)

    return domain_after_check


def check_for_new_domain(state: State, cell: Cell):
    # first rule:
    new_domain = new_domain_after_checking_circles_limit(state, cell)
    if not new_domain:
        return []

    # second rule:
    if not is_unique(state):
        return []

    # third rule:
    new_domain = new_domain_after_checking_more_than_two_limit(state, cell)

    if not len(new_domain):
        return []

		return new_domain